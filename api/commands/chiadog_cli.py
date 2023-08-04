#
# CLI interactions with the chiadog script.
#

import datetime
import http
import json
import os
import psutil
import requests
import signal
import shutil
import sqlite3
import time
import traceback
import yaml

from flask import Flask, jsonify, abort, request, flash, g
from subprocess import Popen, TimeoutExpired, PIPE

from api import app

def load_config(blockchain):
    return open('/root/.chia/chiadog/config.yaml'.format(blockchain),'r').read()

def save_config(config, blockchain):
    try:
        # Validate the YAML first
        yaml.safe_load(config)
        # Save a copy of the old config file
        src='/root/.chia/chiadog/config.yaml'
        dst='/root/.chia/chiadog/config.yaml'+time.strftime("%Y%m%d-%H%M%S")+".yaml"
        shutil.copy(src,dst)
        # Now save the new contents to main config file
        with open(src, 'w') as writer:
            writer.write(config)
    except Exception as ex:
        app.logger.info(traceback.format_exc())
        raise Exception('Updated config.yaml failed validation!\n' + str(ex))
    else:
        if get_chiadog_pid(blockchain):
            stop_chiadog()
            start_chiadog()

def get_chiadog_pid(blockchain):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python3' and '/root/.chia/chiadog/config.yaml' in proc.info['cmdline']:
            return proc.info['pid']
    return None

def dispatch_action(job):
    service = job['service']
    if service != 'monitoring':
        raise Exception("Only monitoring jobs handled here!")
    action = job['action']
    if action == "start":
        start_chiadog()
    elif action == "stop":
        stop_chiadog()
    elif action == "restart":
        stop_chiadog()
        time.sleep(5)
        start_chiadog()
    elif action == "test":
        test_chiadog()
    else:
        raise Exception("Unsupported action {0} for monitoring.".format(action))

def start_chiadog(chain = None):
    #app.logger.info("Starting monitoring....")
    if chain:
        blockchains = [ chain ]
    else:
        blockchains = [ b.strip() for b in os.environ['blockchains'].split(',') ]
    for blockchain in blockchains:
        try:
            workdir = "/chiadog"
            offset_file = "{0}/debug.log.offset".format(workdir)
            if os.path.exists(offset_file):
                os.remove(offset_file)
            configfile = "/root/.chia/chiadog/config.yaml"
            logfile = "/root/.chia/chiadog/logs/chiadog.log"
            proc = Popen("nohup /chia-blockchain/venv/bin/python3 -u main.py --config {0} >> {1} 2>&1 &".format(configfile, logfile), \
                shell=True, universal_newlines=True, stdout=None, stderr=None, cwd="/chiadog")
        except:
            app.logger.info('Failed to start monitoring!')
            app.logger.info(traceback.format_exc())

def stop_chiadog():
    #app.logger.info("Stopping monitoring....")
    blockchains = [ b.strip() for b in os.environ['blockchains'].split(',') ]
    for blockchain in blockchains:
        try:
            os.kill(get_chiadog_pid(blockchain), signal.SIGTERM)
        except:
            app.logger.info('Failed to stop monitoring!')
            app.logger.info(traceback.format_exc())

# If enhanced Chiadog is running within container, then its listening on http://localhost:8925
# Example: curl -X POST http://localhost:8925 -H 'Content-Type: application/json' -d '{"type":"user", "service":"farmer", "priority":"high", "message":"Hello World"}'
def test_chiadog(debug=False):
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        if debug:
            http.client.HTTPConnection.debuglevel = 1
        mode = 'full_node'
        if 'mode' in os.environ and 'harvester' in os.environ['mode']:
            mode = 'harvester'
        response = requests.post("http://localhost:8925", headers = headers, data = json.dumps(
            {
                "type": "user", 
                "service": mode, 
                "priority": "high", 
                "message": "Test alert from Machinaris!"
            }
        ))
    except Exception as ex:
        app.logger.info("Failed to notify Chiadog with test alert.")
    finally:
        http.client.HTTPConnection.debuglevel = 0