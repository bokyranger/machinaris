#
# Util methods for api
#

import http
import json
import os
import psutil
import requests
import socket

from api import app

def send_get(worker, path, query_params={}, timeout=30, debug=False):
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.get(worker.url + path, params = query_params, timeout=timeout)
    http.client.HTTPConnection.debuglevel = 0
    return response

def send_post(path, payload, debug=False):
    controller_url = get_controller_url()
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.post(controller_url + path, headers = headers, data = json.dumps(payload))
    http.client.HTTPConnection.debuglevel = 0
    return response

def send_worker_post(worker, path, payload, debug=False):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.post(worker.url + path, headers = headers, data = json.dumps(payload))
    http.client.HTTPConnection.debuglevel = 0
    return response

def send_delete(path, debug=False):
    controller_url = get_controller_url()
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.delete(controller_url + path, headers = headers)
    http.client.HTTPConnection.debuglevel = 0
    return response

def get_controller_url():
    return "{0}://{1}:{2}".format(
        app.config['CONTROLLER_SCHEME'],
        app.config['CONTROLLER_HOST'],
        app.config['CONTROLLER_PORT']
    )

def get_worker_url():
    return "{0}://{1}:{2}".format(
        app.config['WORKER_SCHEME'],
        get_hostname(),
        app.config['WORKER_PORT']
    )

def get_hostname():
    if 'worker_address' in os.environ:
        hostname = os.environ['worker_address']
    else:
        hostname = socket.gethostname().split('.')[0]
    return hostname

def get_displayname():
    return socket.gethostname().split('.')[0]

def is_controller():
    return app.config['CONTROLLER_HOST'] == "localhost"

def is_fullnode():
    return 'fullnode' in os.environ['mode']

def convert_chia_ip_address(chia_ip_address):
    if chia_ip_address in ['127.0.0.1']:
        return get_hostname()
    return chia_ip_address  # TODO Map duplicated IPs from docker internals...

def current_memory_megabytes():
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / 1024 ** 2, 2)