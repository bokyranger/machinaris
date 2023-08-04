#
# CLI interactions with the chiadog script.
#

import datetime
import json
import os
import psutil
import signal
import shutil
import sqlite3
import time
import traceback
import yaml

from flask_babel import _, lazy_gettext as _l
from flask import Flask, jsonify, abort, request, flash, g
from subprocess import Popen, TimeoutExpired, PIPE

from common.models import alerts as a
from web import app, db, utils
from web.models.chiadog import Alerts
from . import worker as wk

def load_config(farmer, blockchain):
    return utils.send_get(farmer, "/configs/alerts/"+ blockchain, debug=False).content

def load_farmers():
    return wk.load_worker_summary().farmers_harvesters(exclude_blockchains=['mmx'])

def save_config(farmer, blockchain, config):
    try: # Validate the YAML first
        yaml.safe_load(config)
    except Exception as ex:
        app.logger.info(traceback.format_exc())
        flash(_('Updated config.yaml failed validation! Fix and save or refresh page.'), 'danger')
        flash(str(ex), 'warning')
    try:
        utils.send_put(farmer, "/configs/alerts/" + blockchain, config, debug=False)
    except Exception as ex:
        flash(_('Failed to save config to farmer.  Please check log files.'), 'danger')
        flash(str(ex), 'warning')
    else:
        flash(_("Nice! Chiadog's config.yaml validated and saved successfully."), 'success')

def get_notifications():
    try: # Due to defect in date formatting around January 2023, if get a Value
        alerts = db.session.query(a.Alert).order_by(a.Alert.created_at.desc()).all()
        return Alerts(alerts)
    except ValueError:
        app.logger.error("Found likely malformeed alert timestamp.  Now clearing bad alerts.")
        remove_all_alerts()
        return Alerts([])

def remove_alerts(unique_ids):
    app.logger.info("Removing {0} alerts: {1}".format(len(unique_ids), unique_ids))
    db.session.query(a.Alert).filter(a.Alert.unique_id.in_(unique_ids)).delete()
    db.session.commit()

def remove_all_alerts():
    app.logger.info("Removing all alerts!")
    db.session.query(a.Alert).delete()
    db.session.commit()

def start_chiadog(farmer):
    app.logger.info("Starting Chiadog monitoring...")
    try:
        utils.send_post(farmer, "/actions/", {"service": "monitoring","action": "start"}, debug=False)
    except:
        app.logger.info(traceback.format_exc())
        flash(_('Failed to start Chiadog monitoring! Please see log files.'), 'danger')
    else:
        flash(_('Chiadog monitoring started.  Notifications will be sent.'), 'success')

def stop_chiadog(farmer):
    app.logger.info("Stopping Chiadog monitoring...")
    try:
        utils.send_post(farmer, "/actions/", payload={"service": "monitoring","action": "stop"}, debug=False)
    except:
        app.logger.info(traceback.format_exc())
        flash(_('Failed to stop Chiadog monitoring! Please see log files.'), 'danger')
    else:
        flash(_('Chiadog monitoring stopped successfully.  No notifications will be sent!'), 'success')

def send_test_alert(farmer):
    try:
        utils.send_post(farmer, "/actions/", payload={"service": "monitoring","action": "test"}, debug=False)
    except Exception as ex:
        flash(_('Failed to contact farmer to send test alert.  Please ensure the worker is running and check it\'s logs.'), 'danger')
        flash(str(ex), 'warning')
    else:
        flash(_("Test alert has been sent. Please check your configured notification target(s) for receipt of the test alert."), 'success')