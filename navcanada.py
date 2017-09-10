"""Fetches flight planning information from navcanada.
"""

import re
from six.moves import urllib

def get_metar_page():
    """Gets the METAR/TAF page from navcanada.ca.
    """

    metar_uri = "https://flightplanning.navcanada.ca/cgi-bin/route.cgi?Langue=anglais&Depart=CYVR&Destination=CYXX&cw_metar=raw_metar"
    response = urllib.request.urlopen(metar_uri)
    page = response.read().decode('latin-1')

    return page

def parse_metars_and_tafs(page):
    """Extracts the METARs and TAFs from the page.

    - returns: A dictionary keyed by location identifier (CYVR), where
               the values are another deictionary with keys 'TAF'
               (having a single string as the value), and 'METARS'
               (having a list of strings as the value)
    """
    metars = re.findall('(?:METAR|SPECI|LWIS) [A-Z]{4}.*?=', page, flags=re.DOTALL)
    tafs = re.findall('(?:TAF|TAF AMD) [A-Z]{4}.*?=', page, flags=re.DOTALL)
    metars = [re.sub('\s{2,}', ' ', re.sub('(?:<br>|\\n)', '', metar)) for metar in metars]
    tafs = [re.sub('\s{2,}', ' ', re.sub('(?:<br>|\\n)', '', taf)) for taf in tafs]

    return_structure = {}
    for metar in metars:
        m = re.match('^(?:METAR|SPECI|LWIS) ([A-Z]{4}).*?=$', metar)
        station = m.group(1)
        try:
            return_structure[station]['METARS'].append(metar)
        except KeyError:
            return_structure[station] = {'METARS':[metar]}
    for taf in tafs:
        m = re.match('^(?:TAF|TAF AMD) ([A-Z]{4}).*?=$', taf)
        station = m.group(1)
        return_structure[station]['TAF'] = taf

    return return_structure
