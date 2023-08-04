#
# Performs a REST call to controller (possibly localhost) of latest blockchain status.
#


import datetime
import http
import json
import os
import requests
import socket
import sqlite3
import traceback

from flask import g

from common.config import globals
from api.commands import chia_cli, mmx_cli
from api import app
from api import utils

def update():
    with app.app_context():
        try:
            blockchains = globals.enabled_blockchains()
            for blockchain in blockchains:
                hostname = utils.get_hostname()
                if blockchain == 'mmx':
                    bc = mmx_cli.load_blockchain_show(blockchain)
                else:
                    bc = chia_cli.load_blockchain_show(blockchain)
                payload = {
                    "hostname": hostname,
                    "blockchain": blockchain,
                    "details": bc.text.replace('\r', ''),
                }
                utils.send_post('/blockchains/', payload, debug=False)
        except Exception as ex:
            app.logger.info("Failed to load and send blockchain status because {0}".format(str(ex)))
