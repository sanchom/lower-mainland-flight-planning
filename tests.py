import unittest

import navcanada

class TestMetarParser(unittest.TestCase):
    def test_extracts_multiple_stations(self):
        with open('test_data/metars_and_tafs.html', 'r') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            self.assertTrue('CYVR' in result)
            self.assertTrue('CYXX' in result)

if __name__ == '__main__':
    unittest.main()
