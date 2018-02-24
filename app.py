import re
from flask import Flask, render_template
from six import iteritems
from six.moves import urllib
import ssl
import io
import logging
from PIL import Image

from navcanada import parse_metars_and_tafs, get_metar_page, get_upper_winds_page, parse_upper_winds, parse_notams, get_notams_page

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

@app.route('/custom-gfa/<path:path>')
def custom_gfa(path):
    expected_size = (758,608)
    map_box = (0,0,544,608)
    title_box = (544,0,758,86)
    time_box = (544,92,758,137)
    legend_box = (544,160,758,204)
    abbrev_box = (544,240,758,283)
    comments_box = (544,283,758,501)

    remote_path = 'https://flightplanning.navcanada.ca/Latest/gfa/anglais/produits/uprair/gfa/gfacn31/Latest-gfacn31_cldwx_{}'.format(path)
    nav_canada_response = urllib.request.urlopen(remote_path, context=ssl._create_unverified_context())

    image_data = nav_canada_response.read()
    image = Image.open(io.BytesIO(image_data))

    if (image.size != expected_size):
        app.logger.warning(
            'Got an image of size {}; expected {}. Returning the {} image unaltered.'.format(
                image.size, expected_size, image.size))
        response = app.make_response(image_data)
        response.content_type = "image/png"
        return response
    else:
        app.logger.info('Transforming gfa {}...'.format(remote_path))
        map_crop = image.crop(map_box)
        title_crop = image.crop(title_box)
        time_crop = image.crop(time_box)
        legend_crop = image.crop(legend_box)
        abbrev_crop = image.crop(abbrev_box)
        comments_crop = image.crop(comments_box)

        footer_offset = (map_crop.size[0] - legend_crop.size[0] - comments_crop.size[0]) // 2

        transformed_image = Image.new('RGB',
                                      (map_crop.size[0],
                                       map_crop.size[1] + comments_crop.size[1]),
                                      (255,255,255))
        transformed_image.paste(map_crop, (0,0))
        transformed_image.paste(title_crop, (footer_offset, map_crop.size[1]))
        transformed_image.paste(time_crop, (footer_offset, title_crop.size[1] + map_crop.size[1]))
        transformed_image.paste(legend_crop, (footer_offset, title_crop.size[1] + map_crop.size[1] + time_crop.size[1]))
        transformed_image.paste(abbrev_crop, (footer_offset, title_crop.size[1] + map_crop.size[1] + time_crop.size[1] + legend_crop.size[1]))
        transformed_image.paste(comments_crop, (footer_offset + time_crop.size[0], map_crop.size[1]))

        response_bytes = io.BytesIO()
        transformed_image.save(response_bytes, format='PNG')
        response_bytes = response_bytes.getvalue()

        response = app.make_response(response_bytes)
        response.content_type = "image/png"
        return response

@app.route('/')
def homepage():
    metars_and_tafs = parse_metars_and_tafs(get_metar_page())
    upper_winds = parse_upper_winds(get_upper_winds_page())
    notams = parse_notams(get_notams_page())

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
    for notam in notams:
        if notam['sequence_id'] in newest_notams_per_station[notam['station_id']] or notam['sequence_id'] == 0:
            notam['highlight'] = True
        else:
            notam['highlight'] = False

    return render_template(
        'main.html',
        metars_and_tafs=metars_and_tafs,
        upper_winds=upper_winds['YVR'],
        notam_stations=notam_stations,
        notams=notams)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
