"""Fetches flight planning information from navcanada.
"""

import urllib2

def get_metars():
    """Gets the METARs and TAFs from NavCanada.
    
    - returns: A dictionary keyed by location identifier (CYVR), where
               the values are another deictionary with keys 'TAF'
               (having a single string as the value), and 'METARS'
               (having a list of strings as the value)
    """
    metar_uri = "https://flightplanning.navcanada.ca/cgi-bin/route.cgi?Langue=anglais&Depart=CYVR&Destination=CYXX&cw_metar=raw_metar#METAR/TAF"
    request = urllib2.Request(metar_uri)
    response = urllib2.urlopen(request)
    page = response.read()

    # TODO: extract the station identifiers, TAFs, METARs, and
    # construct the response. Look at the 're' package.

    dummy_return_value = {'CYVR': {'TAF': 'dummy TAF', 'METARS': ['dummy_metar_1', 'dummy_metar_2'] } }
    
    return dummy_return_value
