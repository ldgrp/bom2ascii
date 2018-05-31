from flask import Flask, Response
from itertools import cycle
from scraper import get_radar
import time

app = Flask(__name__)

@app.route("/")
@app.route("/<string:idr>")
def hello(idr=None):
    if not idr:
        idr = "023"
    try:
        radar_loop, title = get_radar(idr, (100, 50))
        radar_cycle = cycle(radar_loop)
        def generate():
            while True:
                item = next(radar_cycle)
                time.sleep(1) # TODO:  Stop this. Get some help.
                yield '\n'*20 + title + '\n' + item
        return Response(generate())
    except Exception as e:
        return str(e) 
    
