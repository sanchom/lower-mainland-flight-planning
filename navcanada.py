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

def get_upper_winds_page():
    """Gets the FDs (upper winds) from navcanada.ca.
    """

    fd_uri = "https://flightplanning.navcanada.ca/cgi-bin/Fore-obs/fd.cgi?fd_text=fdcn0&Region=31&Langue=anglais"
    response = urllib.request.urlopen(fd_uri)
    page = response.read().decode('latin-1')

    return page

def get_notams_page():
    """Gets the NOTAMs from navcanada.ca
    """

    notam_uri = "https://flightplanning.navcanada.ca/cgi-bin/Fore-obs/notam.cgi?Langue=anglais&TypeBrief=N&Stations=CZBB%20CYVR%20CYPK%20CYNJ%20CYXX&ni_File=File&ni_FIR=fir&ni_HQ=cyhq"
    response = urllib.request.urlopen(notam_uri)
    page = response.read().decode('latin-1')

    return page

def parse_metars_and_tafs(page):
    """Extracts the METARs and TAFs from the page.

    - returns: A dictionary keyed by location identifier (CYVR), where
               the values are another dictionary with keys 'TAF'
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

def parse_upper_winds(page):
    """Extracts the YVR upper winds from the page.

    - returns: A dictionary keyed by location identifier, where
               the values are another dictionary keyed by forecast
               period and altitude.
    """
    yvr_match = re.findall('YVR - VANCOUVER.*?</table>', page, flags=re.DOTALL)[0]
    periods = re.findall('FDCN0[1-3].*?</tr>', yvr_match, flags=re.DOTALL)
    results = {}
    results['YVR'] = []
    for p in periods:
        m = re.match('^FDCN0[1-3] CWAO FCST BASED ON ([0-9]{6}) DATA.*?VALID ([0-9]{6}).*$', p, flags=re.DOTALL)
        data_from = m.group(1)
        valid_at = m.group(2)
        winds = re.findall('>([0-9]{4}(?:.[0-9][0-9])?)', p, flags=re.DOTALL)
        row = {}
        row['data_from'] = data_from
        row['valid_at'] = valid_at
        row['3000'] = winds[0]
        row['6000'] = winds[1]
        row['9000'] = winds[2]
        row['12000'] = winds[3]
        row['18000'] = winds[4]
        results['YVR'].append(row)
    return results

def parse_notams(page):
    notam_match = re.findall('([0-9]{6} C[0-9A-Z]{3}.*?)</pre>', page, flags=re.DOTALL)
    return notam_match
