from flask import Flask, Response, render_template

import os
import datetime
from flask import send_from_directory
import csv

import pandas as pd

app = Flask(__name__)

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(app.root_path, filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/')
def hello_world():
 #   content = get_file('jenkins_analytics.html')
 #   return Response(content, mimetype="text/html")
 # Aqui qeue bota as series
    return render_template('jenkins_analytics.html',  utc_dt=datetime.datetime.utcnow(), 
        vendas = [30, 40, 45, 50, 49, 60, 70, 91, 125, 100], 
        anos= [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2022] )


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':  # pragma: no cover
    app.run(port=5000)