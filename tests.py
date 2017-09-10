import unittest

from six import iteritems

import navcanada

class TestMetarParser(unittest.TestCase):
    def test_extracts_three_stations(self):
        with open('test_data/metars_and_tafs.html', 'r') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            self.assertTrue('CYVR' in result)
            self.assertTrue('CYXX' in result)
            self.assertTrue('CYCD' in result)

    def test_extracts_specis(self):
        with open('test_data/metars_and_tafs.html', 'r') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            is_speci = False
            for station, data in iteritems(result):
                for m in data['METARS']:
                    if m.count('SPECI'):
                        is_speci = True
            self.assertTrue(is_speci)

    def test_extracts_tafs(self):
        with open('test_data/metars_and_tafs.html', 'r') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            for station, data in iteritems(result):
                self.assertTrue('TAF' in data)

if __name__ == '__main__':
    unittest.main()
