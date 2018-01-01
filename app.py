import re
from flask import Flask, render_template
from six import iteritems

from navcanada import parse_metars_and_tafs, get_metar_page, get_upper_winds_page, parse_upper_winds, parse_notams, get_notams_page

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

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
