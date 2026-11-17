"""Public Chile economic monitor. Credentials belong only to the downloader."""
import json
import os
from pathlib import Path
from urllib.request import urlopen
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Vitals Chile',page_icon='🇨🇱',layout='wide')


@st.cache_data(ttl=300)
def load_data():
    url = os.environ.get('VITALS_DATA_URL','https://raw.githubusercontent.com/greg-at-k/vitals-chile/main/data/dashboard.json')
    if os.environ.get('VITALS_LOCAL_DATA') == '1':
        return json.loads((ROOT/'data/dashboard.json').read_text(encoding='utf-8')),False
    try:
        with urlopen(url,timeout=20) as response:
            return json.load(response),False
    except Exception:
        return json.loads((ROOT/'data/dashboard.json').read_text(encoding='utf-8')),True


def observation(date, quarterly=False, monthly=False):
    d = pd.Timestamp(date)
    return f'Q{d.quarter} {d.year}' if quarterly else d.strftime('%b %Y' if monthly else '%d %b %Y')


st.title('Vitals Chile')
st.caption('Chile economic dashboard')
if st.button('Reload published data',help='Read the latest saved dataset from GitHub. This does not request new data from statistical agencies.'):
    load_data.clear()
data,fallback = load_data()
st.caption('Last successful source refresh: '+data['retrieved_at_utc']+' (UTC)')
if fallback:
    st.warning('The published dataset could not be reached. Showing the saved copy bundled with this app.')
for col,card in zip(st.columns(4),data['cards']):
    with col:
        st.metric(card['title'],f"{card['value']:,.1f}"+(' CLP/USD' if card['format']=='clp' else '%'))
        st.caption(observation(card['date'],quarterly=card['title']=='GDP growth',monthly=card['title']=='Headline inflation'))

section = st.radio('Section',['Economy','Rates and risk','Public finances','External sector','Sources'],horizontal=True)
window = st.selectbox('Viewing window',['Since 2010','Last 10 years','Last 5 years','Full available history'])
latest = pd.Timestamp(max(c['date'] for c in data['cards']))
cutoff = pd.Timestamp('2010-01-01') if window == 'Since 2010' else latest-pd.DateOffset(years=10 if window=='Last 10 years' else 5) if window!='Full available history' else pd.Timestamp('1900-01-01')


def chart(key):
    item = data['charts'][key]
    config = item['config']
    spec = config['spec']
    frame = pd.DataFrame(config['rows'],columns=config['columns'])
    curve = key == 'curve'
    st.subheader(config['title'])
    x = spec['x']
    if not curve:
        frame[x] = pd.to_datetime(frame[x])
        valid = frame[spec['y']].notna().any(axis=1) if isinstance(spec['y'],list) else frame[spec['y']].notna()
        date = frame.loc[valid,x].max()
        st.caption(item['metadata']+' | Latest observation: '+observation(date,quarterly=key in ['gdp','general_government_balance','general_government_debt'],monthly=key not in ['policy_rate','inflation_compensation_5y']))
        frame = frame[frame[x]>=cutoff]
    else:
        st.caption('BCCh BCP/BTP | percent per year | Daily | '+observation(data['curve_date']))
    fig = go.Figure()
    if spec.get('series'):
        groups = [(name,part,spec['y']) for name,part in frame.groupby(spec['series'])]
    else:
        groups = [(name,frame,name) for name in (spec['y'] if isinstance(spec['y'],list) else [spec['y']])]
    for i,(label,part,y) in enumerate(groups):
        label = label if label != 'value' else config['title']
        if key in ['trade','general_government_balance']:
            fig.add_bar(x=part[x],y=part[y],name=label,marker_color='#a96036')
        else:
            fig.add_trace(go.Scatter(x=part[x],y=part[y],name=label,connectgaps=False,
                                    mode='lines+markers' if curve else 'lines',
                                    line=dict(color=['#a96036','#218382'][i%2],dash='dash' if i else 'solid',shape='hv' if key=='policy_rate' else 'linear')))
    for ref in spec.get('referenceLines',[]):
        fig.add_hline(y=ref['value'],line_color='#8c969c',line_width=1)
    fig.update_layout(height=330,margin=dict(l=10,r=10,t=20,b=10),yaxis_title=spec.get('yLabel'),xaxis_title='Years to maturity' if curve else None,legend=dict(orientation='h'),hovermode='x unified',showlegend=len(groups)>1)
    if curve:
        fig.update_xaxes(tickvals=[2,5,10],range=[1.7,10.3])
    st.plotly_chart(fig,width='stretch',key=key)
    if curve:
        st.caption(f"10-year minus 2-year spread: {data['curve_spread_bps']:+.0f} basis points")
    if key == 'fx':
        b = data['benchmark']
        st.caption(f"Implied rate holds the bilateral real rate at its {b['start']}–{b['end']} average ({b['valid_months']} valid months). Both lines use CLP per USD.")
    if key.startswith('general_government'):
        st.caption('General government; trailing-year GDP denominator. Ratios are calculated from DIPRES amounts distributed by BCCh. Original-release comparisons remain pending.')
    if key == 'inflation_compensation_5y':
        st.caption('Bond inflation compensation includes inflation expectations and risk/liquidity premiums.')
    with st.expander('Values and method'):
        st.dataframe(frame,hide_index=True)
        st.download_button('Download chart CSV',frame.to_csv(index=False),key+'.csv','text/csv',key='download-'+key)


if section == 'Economy':
    left,right = st.columns(2)
    with left: chart('gdp')
    with right: chart('inflation')
    chart('policy_rate')
elif section == 'Rates and risk':
    left,right = st.columns(2)
    with left: chart('curve')
    with right:
        st.subheader('Sovereign risk')
        st.info('A reliable public automated CDS or sovereign-spread source is still being investigated.')
    chart('inflation_compensation_5y')
elif section == 'Public finances':
    left,right = st.columns(2)
    with left: chart('general_government_balance')
    with right: chart('general_government_debt')
elif section == 'External sector':
    chart('fx')
    left,right = st.columns(2)
    with left:
        chart('real_fx')
        chart('trade')
    with right:
        chart('copper')
        chart('shares')
else:
    st.subheader('Source and refresh details')
    st.link_button('Request a source refresh on GitHub','https://github.com/greg-at-k/vitals-chile/actions/workflows/refresh.yml')
    st.caption('Repository maintainers can run the workflow manually. App visits read stored data and do not call source APIs.')
    st.json(data['refresh'])
    st.download_button('Download complete dataset',json.dumps(data,allow_nan=False),'vitals-chile.json','application/json')
    st.markdown((ROOT/'docs/data-catalog.md').read_text(encoding='utf-8'))
    st.subheader('Verification status')
    st.warning('Trade workbook comparisons and calculation tests are available. Original-release spot checks for every series are not yet complete. Sovereign risk is unavailable.')
    st.json(json.loads((ROOT/'research/results/trade-source-check.json').read_text(encoding='utf-8')))
