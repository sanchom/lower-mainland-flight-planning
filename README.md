[![Build Status](https://travis-ci.org/sanchom/lower-mainland-flight-planning.svg?branch=master)](https://travis-ci.org/sanchom/lower-mainland-flight-planning)

A Heroku app using Python that serves a simple webpage with flight
planning information for the BC Lower Mainland.

# Please send feedback

Send me suggestions, feature requests, or bugs by [filling out an
issue](https://github.com/sanchom/lower-mainland-flight-planning/issues).

# Setup for local development

* [Install heroku command line interface](https://devcenter.heroku.com/articles/getting-started-with-python#set-up
* `git clone git@github.com:sanchom/lower-mainland-flight-planning.git`
* `cd lower-mainland-flight-planning`
* Install `python-pip` and `python3-pip` packages
* `pip install -r requirements.txt`
* `pip3 install -r requirements.txt`
* `heroku local web`

You should see something like this:

    [WARN] No ENV file found
    17:12:00 web.1   |  [2017-09-01 18:12:00 +0000] [7874] [INFO] Starting gunicorn 19.7.1
    17:12:00 web.1   |  [2017-09-01 18:12:00 +0000] [7874] [INFO] Listening at: http://0.0.0.0:5000 (7874)
    17:12:00 web.1   |  [2017-09-01 18:12:00 +0000] [7874] [INFO] Using worker: sync
    17:12:00 web.1   |  [2017-09-01 18:12:00 +0000] [7879] [INFO] Booting worker with pid: 7879
