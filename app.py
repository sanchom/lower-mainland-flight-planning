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
<p>
<a href="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_000.png" target="blank_"><img src="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_000.png" width="31%" /></a>
<a href="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_006.png" target="blank_"><img src="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_006.png" width="31%" /></a>
<a href="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_012.png" target="blank_"><img src="https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_012.png" width="31%" /></a>
</p>
    """
    for station, data in iteritems(metars_and_tafs):
        result_page = result_page + '<h1>{}</h1>\n'.format(station)
        for metar in data['METARS']:
            result_page = result_page + '<p>{}</p>\n'.format(metar)
        # Splitting the TAF for display at every 'FM' element.
        formatted_taf = re.sub(' FM', ' <br />FM', data['TAF'])
        result_page = result_page + '<p>{}</p>\n'.format(formatted_taf)



    return result_page

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
