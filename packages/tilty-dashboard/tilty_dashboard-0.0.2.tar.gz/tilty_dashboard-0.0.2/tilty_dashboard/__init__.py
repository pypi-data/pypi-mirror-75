# -*- coding: utf-8 -*-
""" The main method, handles all initialization """
import logging
import os
from datetime import datetime

import sqlalchemy
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from werkzeug.contrib.fixers import ProxyFix

from tilty_dashboard.model import Tilt, db

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


app = Flask(__name__)
socketio = SocketIO(app)


def init_webapp(config):
    """ Initialize the web application. """
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['webapp']['database_uri']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'abc123')
    CORS(app, supports_credentials=True)
    Bootstrap(app)
    db.app = app
    db.init_app(app)
    db.create_all()

    return app


@app.route('/')
def index():
    """A landing page.

    Nothing too interesting here.

    """
    return render_template('index.html')


@socketio.on('refresh')
def refresh():
    """ todo """
    try:
        _data = Tilt.query.order_by(sqlalchemy.desc(Tilt.timestamp)).first()
        emit('refresh', {
            'data': {
                'color': _data.color,
                'gravity': _data.gravity,
                'mac': _data.mac,
                'temp': _data.temp,
                'timestamp': _data.timestamp.isoformat(),
            }
        })
    except AttributeError:
        emit('refresh', {
            'data': {
                'color': 'n/a',
                'gravity': 0,
                'mac': '',
                'temp': 0,
                'timestamp': datetime.now().isoformat(),
            }
        })
