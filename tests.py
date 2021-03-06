import unittest

from six import iteritems

import io
import navcanada

class TestMetarParser(unittest.TestCase):
    def test_extracts_three_stations(self):
        with io.open('test_data/metars_and_tafs.html', 'r', encoding='latin-1') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            self.assertTrue('CYVR' in result)
            self.assertTrue('CYXX' in result)
            self.assertTrue('CYCD' in result)

    def test_extracts_specis(self):
        with io.open('test_data/metars_and_tafs.html', 'r', encoding='latin-1') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            is_speci = False
            for station, data in iteritems(result):
                for m in data['METARS']:
                    if m.count('SPECI'):
                        is_speci = True
            self.assertTrue(is_speci)

    def test_extracts_lwiss(self):
        with io.open('test_data/metars_and_tafs.html', 'r', encoding='latin-1') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            is_lwis = False
            for station, data in iteritems(result):
                for m in data['METARS']:
                    if m.count('LWIS'):
                        is_lwis = True
            self.assertTrue(is_lwis)

    def test_extracts_tafs(self):
        with io.open('test_data/metars_and_tafs.html', 'r', encoding='latin-1') as f:
            page = f.read()
            result = navcanada.parse_metars_and_tafs(page)
            for station, data in iteritems(result):
                self.assertTrue('TAF' in data)

    def test_extract_upper_winds(self):
        with io.open('test_data/fds.html', 'r', encoding='latin-1') as f:
            page = f.read()
            result = navcanada.parse_upper_winds(page)
            self.assertTrue('YVR' in result)

    def test_extracts_notams(self):
        with io.open('test_data/notams.html', 'r', encoding='latin-1') as f:
            page = f.read()
            result = navcanada.parse_notams(page)
            self.assertTrue(len(result) > 10)
            self.assertTrue('sequence_id' in result[0])

if __name__ == '__main__':
    unittest.main()
