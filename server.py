from flask import Flask, Response, request
from itertools import cycle
from scraper import get_radar
import time

app = Flask(__name__)

# from https://github.com/chubin/wttr.in/blob/master/bin/srv.py
PLAIN_TEXT_AGENTS = [
    "curl",
    "httpie",
    "lwp-request",
    "wget",
    "python-requests"
]

@app.route("/")
@app.route("/<string:idr>")
def hello(idr=None):
    if not idr:
        idr = "023"
    user_agent = request.headers.get('User-Agent').lower()

    if any(agent in user_agent for agent in PLAIN_TEXT_AGENTS):
        html_output = False
    else:
        html_output = True

    if(html_output):
        return("<p>Usage <pre>curl bom2ascii.herokuapp.com/<:idr></p>")
    
    try:
        radar_loop, title = get_radar(idr, (100, 50))
        radar_cycle = cycle(radar_loop)
        def generate():
            for i in range(len(radar_loop)*3):
                item = next(radar_cycle)
                time.sleep(1) # TODO:  Stop this. Get some help.
                yield '\n'*20 + title + '\n' + item
        return Response(generate())
    except Exception as e:
        return str(e) 
    
