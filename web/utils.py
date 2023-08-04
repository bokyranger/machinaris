#
# Util methods for web
#

import http
import json
import os
import requests
import socket

from web import app

def send_get(worker, path, query_params={}, timeout=30, debug=False, lang=None):
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    headers = {}
    if lang:
        headers['Accept-Language'] = lang
    response = requests.get(worker.url + path, headers = headers, params = query_params, timeout=timeout)
    http.client.HTTPConnection.debuglevel = 0
    return response

def send_post(worker, path, payload, debug=False, lang=None, timeout=None):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if lang:
        headers['Accept-Language'] = lang
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.post(worker.url + path, headers = headers, data = json.dumps(payload), timeout=timeout)
    http.client.HTTPConnection.debuglevel = 0
    return response

def send_put(worker, path, payload, debug=False, lang=None, timeout=None):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if lang:
        headers['Accept-Language'] = lang
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.put(worker.url + path, headers = headers, data = json.dumps(payload), timeout=timeout)
    http.client.HTTPConnection.debuglevel = 0
    return response

def send_delete(worker, path, debug=False, lang=None, timeout=None):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    if lang:
        headers['Accept-Language'] = lang
    if debug:
        http.client.HTTPConnection.debuglevel = 1
    response = requests.delete(worker.url + path, headers = headers, timeout=timeout)
    http.client.HTTPConnection.debuglevel = 0
    return response

def get_controller_url():
    return "{0}://{1}:{2}".format(
        app.config['CONTROLLER_SCHEME'],
        app.config['CONTROLLER_HOST'],
        app.config['CONTROLLER_PORT']
    )

def get_controller_web():
    return "http://{0}:8926".format(
        app.config['CONTROLLER_HOST']
    )

def get_hostname():
    if 'worker_address' in os.environ:
        hostname = os.environ['worker_address']
    else:
        hostname = socket.gethostname().split('.')[0]
    return hostname

def is_controller():
    return app.config['CONTROLLER_HOST'] == "localhost"

def convert_chia_ip_address(chia_ip_address):
    if chia_ip_address in ['127.0.0.1']:
        return get_hostname()
    return chia_ip_address  # TODO Map duplicated IPs from docker internals...