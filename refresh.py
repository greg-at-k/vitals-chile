"""Fetch primary sources and atomically publish a complete public dataset."""
import io
import json
import math
import os
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlencode

import pandas as pd
from dotenv import dotenv_values
from openpyxl import load_workbook
from research.check_bcch_sources import CANDIDATES, request_json

ROOT = Path(__file__).resolve().parent
TRADE = 'https://si3.bcentral.cl/estadisticas/Principal1/excel/SE/COMEX/Excel/Mensual/02_Balanza_comercial_mensual_por_paises.xlsx'


def read_url(url, accept=None):
    with urlopen(Request(url, headers={'Accept': accept or '*/*'}), timeout=90) as response:
        return response.read()


def bcch(token, key, end):
    identifier = CANDIDATES[key]
    body = request_json(token, dict(function='GetSeries', timeseries=identifier,
                                  firstdate='2009-01-01', lastdate=end))['Series']
    if body['seriesId'] != identifier:
        raise ValueError('Unexpected source identifier')
    values = {}
    for row in body['Obs']:
        date = datetime.strptime(row['indexDateString'], '%d-%m-%Y').date().isoformat()
        if date in values:
            raise ValueError('Duplicate source date')
        value = float(row['value']) if row['statusCode'] == 'OK' else None
        values[date] = value if value is None or math.isfinite(value) else None
    if not any(v is not None for v in values.values()):
        raise ValueError('Empty source series')
    return values


def imf(flow, key):
    url = f'https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/{flow}/+/{key}?' + urlencode({'c[TIME_PERIOD]':'ge:1976-01'})
    frame = pd.read_csv(io.BytesIO(read_url(url, 'text/csv')))
    result = {}
    for country, part in frame.groupby('COUNTRY'):
        values = {}
        for _, row in part.iterrows():
            if pd.notna(row['OBS_VALUE']):
                month = row['TIME_PERIOD'].replace('-M', '-')
                if month in values:
                    raise ValueError('Duplicate IMF period')
                scale = row.get('SCALE', 0)
                scale = float(scale) if pd.notna(scale) else 0
                values[month] = float(row['OBS_VALUE']) * 10 ** scale
        result[country] = values
    return result


def trade():
    book = load_workbook(io.BytesIO(read_url(TRADE)), read_only=True, data_only=True)
    sheet = book['X_por_país']
    rows = list(sheet.values)
    dates, year = {}, None
    months = {'Ene':1,'Feb':2,'Mar':3,'Abr':4,'May':5,'Jun':6,'Jul':7,'Ago':8,'Sep':9,'Oct':10,'Nov':11,'Dic':12}
    for col in range(4, len(rows[4])):
        anchor = rows[3][col] if col < len(rows[3]) else None
        if isinstance(anchor, (int, float)) and 2000 <= anchor <= 2100:
            year = int(anchor)
        name = str(rows[4][col] or '').strip()[:3].title()
        if year and name in months:
            dates[col] = f'{year}-{months[name]:02d}'
    result = {}
    for row in rows:
        label = ' '.join(str(v or '') for v in row[:4]).strip()
        labels = {str(v).strip() for v in row[:4] if v is not None}
        key = 'china' if 'China' in labels else 'us' if 'Estados Unidos' in labels else 'total' if 'Total' in labels else None
        if key:
            result[key] = {date:float(row[col]) for col,date in dates.items() if col < len(row) and isinstance(row[col], (int,float))}
    if set(result) != {'china','us','total'}:
        raise ValueError('Country workbook labels changed')
    return result


def series(values, frequency='MS'):
    s = pd.Series(values, dtype=float)
    s.index = pd.to_datetime(s.index)
    return s.sort_index().resample(frequency).last()


def calculate(raw):
    template = json.loads((ROOT/'design/preview-data.json').read_text(encoding='utf-8'))
    b = raw['bcch']
    charts = template['charts']
    def put(key, frame):
        if isinstance(frame, pd.Series):
            frame = frame.to_frame('value')
        frame = frame.loc[frame.index >= '2010-01-01']
        charts[key]['config']['rows'] = [[date.strftime('%Y-%m-%d'), *[None if pd.isna(v) else float(v) for v in row]] for date,row in frame.iterrows()]
    gdp = series(b['real_gdp'], 'QS')
    put('gdp', pd.DataFrame({'value':100*(gdp/gdp.shift(4)-1),'current_gdp':gdp,'year_ago_gdp':gdp.shift(4)}))
    put('inflation', pd.DataFrame({'Headline':series(b['headline_inflation']), 'Core':series(b['core_inflation'])}))
    for key in ('policy_rate','inflation_compensation_5y','copper'):
        # Keep native daily history for market series.
        put(key, series(b[key], 'MS' if key == 'copper' else 'D'))
        if key != 'copper':
            charts[key]['metadata'] = 'Daily | BCCh | percent per year'
    yields = pd.DataFrame({tenor:series(b[f'nominal_bond_{tenor}y'], 'D') for tenor in (2,5,10)}).dropna()
    if yields.empty:
        raise ValueError('No common curve observation')
    template['curve_date'] = yields.index[-1].strftime('%Y-%m-%d')
    template['curve_spread_bps'] = float(100*(yields.iloc[-1][10]-yields.iloc[-1][2]))
    charts['curve']['config']['rows'] = [[tenor,float(yields.iloc[-1][tenor])] for tenor in (2,5,10)]
    cpi = raw['cpi']
    fx = series(raw['fx']['CHL'])
    cl, us = series(cpi['CHL']), series(cpi['USA'])
    aligned = pd.DataFrame({'e':fx,'cl':cl,'us':us})
    q = aligned.e*aligned.us/aligned.cl
    end = q.last_valid_index()
    start = end-pd.DateOffset(months=359)
    benchmark = q.loc[start:end].mean()
    if not math.isfinite(benchmark) or benchmark <= 0:
        raise ValueError('Invalid FX benchmark')
    template['benchmark'] = dict(start=start.strftime('%Y-%m'),end=end.strftime('%Y-%m'),valid_months=int(q.loc[start:end].count()))
    put('fx',pd.DataFrame({'Actual':fx,'Implied':benchmark*cl/us}))
    put('real_fx',100*q/benchmark)
    denominator = 1000*series(b['nominal_gdp'],'QS').rolling(4,min_periods=4).sum()
    for key in ('general_government_balance','general_government_debt'):
        numerator = series(b[key],'QS')
        if key.endswith('balance'):
            numerator = numerator.rolling(4,min_periods=4).sum()
        put(key,pd.DataFrame({'value':100*numerator/denominator,'numerator':numerator,'denominator':denominator}))
    put('trade',series(b['trade_balance_candidate']))
    totals = series(raw['trade']['total']).rolling(12,min_periods=12).sum()
    share_rows = []
    for key,label in [('china','China'),('us','United States')]:
        exports = series(raw['trade'][key]).rolling(12,min_periods=12).sum()
        for date in totals.index[totals.index >= '2010-01-01']:
            n,d = exports.get(date),totals[date]
            share_rows.append([date.strftime('%Y-%m-%d'),label,None if pd.isna(n) or pd.isna(d) or d<=0 else float(100*n/d),None if pd.isna(n) else float(n),None if pd.isna(d) else float(d)])
    charts['shares']['config']['rows'] = sorted(share_rows)
    for card,key in zip(template['cards'],['real_gdp','headline_inflation','policy_rate','observed_usd']):
        if key == 'real_gdp':
            row = pd.Series({r[0]:r[1] for r in charts['gdp']['config']['rows']}).dropna()
            card['date'],card['value'] = row.index[-1],float(row.iloc[-1])
        else:
            valid = {k:v for k,v in b[key].items() if v is not None}
            card['date'] = max(valid)
            card['value'] = valid[card['date']]
    template['purpose'] = 'Published dashboard dataset'
    return template


def main():
    started = datetime.now(timezone.utc).isoformat(timespec='seconds')
    token = os.environ.get('BCCH_API_TOKEN') or dotenv_values(ROOT/'.env',interpolate=False).get('BCCH_API_TOKEN')
    if not token:
        raise ValueError('BCCH_API_TOKEN is required')
    excluded = {'exports_china','exports_us','exports_total','general_government_balance_ratio'}
    raw = {'bcch':{key:bcch(token,key,started[:10]) for key in CANDIDATES if key not in excluded}}
    raw['cpi'] = imf('CPI','CHL+USA.CPI._T.IX.M')
    raw['fx'] = imf('ER','CHL.XDC_USD.PA_RT.M')
    raw['trade'] = trade()
    dataset = calculate(raw)
    completed = datetime.now(timezone.utc).isoformat(timespec='seconds')
    dataset['retrieved_at_utc'] = completed
    dataset['sources'] = {'bcch':CANDIDATES,'trade':TRADE,'imf':'https://data.imf.org/en/Resource-Pages/IMF-API'}
    dataset['refresh'] = dict(started_at_utc=started,completed_at_utc=completed,status='success',run_url=os.environ.get('REFRESH_RUN_URL'))
    dataset['raw'] = raw
    encoded = json.dumps(dataset,allow_nan=False,ensure_ascii=True,separators=(',',':'))
    if token in encoded:
        raise ValueError('Credential found in public output')
    target = ROOT/'data/dashboard.json'
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(encoded,encoding='utf-8')
    temporary.replace(target)
    print(json.dumps(dataset['refresh']))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Source exceptions may contain authenticated URLs: emit only the type.
        print(json.dumps({'status':'failed','error_type':type(error).__name__}))
        raise SystemExit(1)
