import os
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest


class AppChecks(unittest.TestCase):
    def test_all_sections_and_windows(self):
        os.environ['VITALS_LOCAL_DATA'] = '1'
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'streamlit_app.py'),default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric),4)
        for section in ['Rates and risk','Public finances','External sector','Sources','Economy']:
            app.radio[0].set_value(section).run()
            self.assertFalse(app.exception)
        for window in ['Last 10 years','Last 5 years','Full available history']:
            app.selectbox[0].set_value(window).run()
            self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertFalse(app.exception)
