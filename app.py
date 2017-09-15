import re

from flask import Flask
from six import iteritems

from navcanada import parse_metars_and_tafs, get_metar_page, get_upper_winds_page, parse_upper_winds, parse_notams, get_notams_page

app = Flask(__name__)

def make_fd_row(elements):
    row = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(*elements)
    return row

@app.route('/')
def homepage():
    metars_and_tafs = parse_metars_and_tafs(get_metar_page())
    upper_winds = parse_upper_winds(get_upper_winds_page())
    notams = parse_notams(get_notams_page())

    # There's got to be a better way to construct an html response
    # than explicitly concatenating together a bunch of strings.

    result_page = """
<html>
  <head>
    <meta name="google-site-verification" content="7IP0_xtDCyu3DT0l7UCNPRZ6Uga0jK8R_UUiGZqqp4M" />
    <title>Lower Mainland Flight Planning Info</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto+Slab" rel="stylesheet">
    <style>
@media all {html body table {font-size: 18px;} .gfa {width: 500px;} .footer {margin-left: 10%; margin-right: 10%; } }
@media all and (max-width:800px){html body table {font-size: 18px;} .gfa {width: 500px;} }
@media all and (max-width:720px){html body table {font-size: 17px;} .gfa {width: 500px;} }
@media all and (max-width:640px){html body table {font-size: 16px;} .gfa {width: 100%;} .footer {margin-left: 0%; margin-right: 0%; } }
@media all and (max-width:560px){html body table {font-size: 15px;} .gfa {width: 100%;} }
@media all and (max-width:480px){html body table {font-size: 14px;} .gfa {width: 100%;} }

body {
    margin-top: 5em;
    margin-bottom: 5em;
    margin-left: 10%;
    margin-right: 10%;
    font-family: 'Roboto Slab', serif;
}
table {
    border-spacing: 0;
    border-collapse: collapse;
}
td, th {
    padding: 0.5em;
}
th {
    border-bottom: 1px solid;
}
.gfa-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
img {
    margin: 0.5em;
}
.footer {
text-align: center;
font-size: 70%;
margin-top: 5em;
}
.header {
text-align: center;
font-size: 70%;
margin-bottom: 3em;
}
.notam {
margin-top: 0.5em;
padding-top: 0.5em;
padding-bottom: 0.5em;
margin-bottom: 0.5em
}
.new-notam {
background-color:#e6f2ff;
}
.notam_content {
margin-left: 3em;
margin-right: 10%;
}
    </style>

    <!-- Global Site Tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-106550520-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments)};
    gtag('js', new Date());

    gtag('config', 'UA-106550520-1');
    </script>


  </head>
  <body>
<div class="header"><p><a href="#disclaimer">Disclaimer</a></p></div>
<div class="gfa-container">
<a href="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_000.png" target="blank_"><img class="gfa" src="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_000.png" /></a>
<a href="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_006.png" target="blank_"><img class="gfa" src="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_006.png" /></a>
<a href="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_012.png" target="blank_"><img class="gfa" src="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_012.png" /></a>
</div>
    """
    for station, data in iteritems(metars_and_tafs):
        result_page = result_page + '<h1>{}</h1>\n'.format(station)
        for metar in data['METARS']:
            result_page = result_page + '<p>{}</p>\n'.format(metar)
        # Splitting the TAF for display at every 'FM' element.
        formatted_taf = re.sub(' FM', ' <br />FM', data['TAF'])
        result_page = result_page + '<p>{}</p>\n'.format(formatted_taf)
    result_page = result_page + '<h1>Supplemental information</h1\n'
    result_page = result_page + '<p>Lower mainland ATIS: <a href="tel:1-877-517-2847">1-877-517-2847</a></p>\n'
    result_page = result_page + '<p><a href="http://atm.navcanada.ca/atm/iwv/CZBB">CZBB (Boundary Bay) current winds</a></p>\n'
    for station, winds in iteritems(upper_winds):
        result_page = result_page + '<h1>Upper winds (Vancouver)</h1>\n'
        result_page = result_page + '<table>\n'
        result_page = result_page + '<tr><th>Data from</th><th>Valid at</th><th>3000</th><th>6000</th><th>9000</th></tr>\n'
        for w in winds:
            result_page = result_page + make_fd_row((w['data_from'], w['valid_at'], w['3000'], w['6000'], w['9000']))
        result_page = result_page + '</table>\n'

    result_page = result_page + '<h1>NOTAMs</h1>\n'


    notam_stations = set()
    for notam in notams:
        notam_stations.add(notam['station_id'])
    newest_notams_per_station = {}
    for notam in notams:
        try:
            newest_notams_per_station[notam['station_id']].append(notam['sequence_id'])
        except KeyError:
            newest_notams_per_station[notam['station_id']] = [notam['sequence_id']]
    for station_id, notam_ids in iteritems(newest_notams_per_station):
        newest_notams_per_station[station_id] = sorted(notam_ids)[-10:]


    result_page = result_page + '<div class="notam new-notam">\n<p class="notam_station">Ten newest NOTAMs per file ({}) are highlighted.</p></div>\n'.format(', '.join(notam_stations))
    for notam in notams:
        if notam['sequence_id'] in newest_notams_per_station[notam['station_id']] or notam['sequence_id'] == 0:
            result_page = result_page + '<div class="notam new-notam">\n'
        else:
            result_page = result_page + '<div class="notam">\n'
        result_page = result_page + '<p class="notam_station">{}</p>\n'.format(notam['station_line'])
        result_page = result_page + '<p class="notam_content">{}</p>\n'.format(notam['content'])
        result_page = result_page + '</div>\n'

    result_page = result_page + '<div class="footer"><a name="disclaimer" /><p>This page is a good-faith attempt to reproduce a selection of flight planning information from <a href="http://flightplanning.navcanada.ca">navcanada.ca</a> that I find generally useful for VFR flying in the area. I don\'t guarantee its accuracy, completeness, relevance, or currency; <a href="http://www.navcanada.ca/en/pages/terms-of-use.aspx">neither do they</a>.</p><p>Code, feedback: <a href="https://github.com/sanchom/lower-mainland-flight-planning">github.com/sanchom/lower-mainland-flight-planning</a></p></div>\n'

    result_page = result_page + '</body>\n</html>'

    return result_page

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
