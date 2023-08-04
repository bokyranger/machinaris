#
# Performs a REST call to controller (possibly localhost) of latest farm status.
#


import datetime
import http
import json
import os
import pytz
import requests
import socket
import sqlite3
import traceback

from flask import g

from common.config import globals
from common.models import workers as w
from common.extensions.database import db
from api.commands import chia_cli, chiadog_cli, plotman_cli
from api import app
from api import utils

def update():
    with app.app_context():
        try:
            workers = db.session.query(w.Worker).order_by(w.Worker.hostname).all()
            ping_workers(workers)
            db.session.commit()
        except Exception as ex:
            app.logger.info("Failed to load and send worker's connection status because {0}".format(str(ex)))

def ping_workers(workers):
    for worker in workers:
        try:
            #app.logger.info("Pinging worker api endpoint: {0}".format(worker.hostname))
            utils.send_get(worker, "/ping/", timeout=3, debug=False)
            worker.latest_ping_result = "Responding"
            worker.updated_at = datetime.datetime.now()
            worker.ping_success_at = datetime.datetime.now()
        except requests.exceptions.ConnectTimeout as ex:
            app.logger.info('Received connection timeout from {0}'.format(worker.url + '/ping'))
            worker.latest_ping_result = "Connection Timeout"
        except requests.exceptions.ConnectionError as ex:
            app.logger.info('Received connection refused from {0}'.format(worker.url + '/ping'))
            worker.latest_ping_result = "Connection Refused"
        except Exception as ex:
            app.logger.info('Received general error from {0}'.format(worker.url + '/ping'))
            worker.latest_ping_result = "Connection Error"
