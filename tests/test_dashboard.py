import copy
import json
from pathlib import Path
import unittest

import pandas as pd
from refresh import calculate


class EconomicChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(Path('data/dashboard.json').read_text(encoding='utf-8'))

    def test_actual_implied_real_identity(self):
        charts = self.data['charts']
        real = {r[0]:r[1] for r in charts['real_fx']['config']['rows']}
        for date,actual,implied in charts['fx']['config']['rows']:
            if implied is not None:
                self.assertAlmostEqual(100*actual/implied,real[date],places=8)

    def test_common_curve_date_and_spread(self):
        date = self.data['curve_date']
        points = dict(self.data['charts']['curve']['config']['rows'])
        for tenor,value in points.items():
            self.assertEqual(value,self.data['raw']['bcch'][f'nominal_bond_{tenor}y'][date])
        self.assertAlmostEqual(self.data['curve_spread_bps'],100*(points[10]-points[2]))

    def test_export_shares_from_twelve_original_months(self):
        raw = self.data['raw']['trade']
        for date,country,share,numerator,denominator in self.data['charts']['shares']['config']['rows'][-2:]:
            month = pd.Timestamp(date).to_period('M')
            months = [str(month-i) for i in range(12)]
            key = 'china' if country == 'China' else 'us'
            n = sum(raw[key][m] for m in months)
            d = sum(raw['total'][m] for m in months)
            self.assertAlmostEqual(share,100*n/d)

    def test_missing_quarter_prevents_trailing_fiscal_total(self):
        raw = copy.deepcopy(self.data['raw'])
        values = raw['bcch']['general_government_balance']
        date = max(d for d,v in values.items() if v is not None)
        values[date] = None
        result = calculate(raw)
        self.assertIsNone(result['charts']['general_government_balance']['config']['rows'][-1][1])


if __name__ == '__main__':
    unittest.main()
