from flask import Flask
from datetime import datetime

import navcanada

app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    metars = navcanada.get_metars()

    return """
    <h1>Hello heroku. Testing the auto deployment.</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
