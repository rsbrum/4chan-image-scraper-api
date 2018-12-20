from flask import (
    Flask, send_file, request, abort
)
from flask_cors import CORS
from app import Scraper
import os
# Create the application instance
app = Flask(__name__)
CORS(app)
# Create a URL route in our application for "/"


@app.route('/downloadImages')
def getImages():
    url = request.args.get('url')

    try:
        scraper = Scraper(url)
    except:
        abort(500)

    dir = scraper.getDirectory()

    response = send_file(dir + '.zip', mimetype='application/zip')
    return response


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
