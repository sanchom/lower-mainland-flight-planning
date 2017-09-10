import re

from flask import Flask
from six import iteritems

from navcanada import parse_metars_and_tafs, get_metar_page

app = Flask(__name__)

@app.route('/')
def homepage():
    metars_and_tafs = parse_metars_and_tafs(get_metar_page())

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
.gfa-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
img {
    margin: 0.5em;
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
    result_page = result_page + '</body>\n</html>'

    return result_page

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
