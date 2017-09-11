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
    <link href="https://fonts.googleapis.com/css?family=Roboto+Slab" rel="stylesheet">
    <style>
@media all {html {font-size: 18px;} .gfa {width: 500px;} }
@media all and (max-width:800px){html {font-size: 18px;} .gfa {width: 500px;} }
@media all and (max-width:720px){html {font-size: 17px;} .gfa {width: 500px;} }
@media all and (max-width:640px){html {font-size: 16px;} .gfa {width: 500px;} }
@media all and (max-width:560px){html {font-size: 15px;} .gfa {width: 448px;} }
@media all and (max-width:480px){html {font-size: 14px;} .gfa {width: 384px;} }

body {
    margin-top: 5em;
    margin-bottom: 5em;
    margin-left: 10%;
    margin-right: 10%;
    font-family: 'Roboto Slab', serif;
}
table {
    font-size: 100%;
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
    </style>
  </head>
  <body>
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
    for station, winds in iteritems(upper_winds):
        result_page = result_page + '<h1>Upper winds (Vancouver)</h1>\n'
        result_page = result_page + '<table>\n'
        result_page = result_page + '<tr><th>Data from</th><th>Valid at</th><th>3000</th><th>6000</th><th>9000</th></tr>\n'
        for w in winds:
            result_page = result_page + make_fd_row((w['data_from'], w['valid_at'], w['3000'], w['6000'], w['9000']))
        result_page = result_page + '</table>\n'

    result_page = result_page + '<h1>NOTAMs</h1>\n'
    result_page = result_page + '<pre>\n'
    for notam in notams:
        result_page = result_page + notam + '\n'
    result_page = result_page + '</pre>\n'

    result_page = result_page + '<div class="footer"><p><a href="https://github.com/sanchom/lower-mainland-flight-planning">github.com/sanchom/lower-mainland-flight-planning</a></p></div>\n'

    result_page = result_page + '</body>\n</html>'

    return result_page

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
