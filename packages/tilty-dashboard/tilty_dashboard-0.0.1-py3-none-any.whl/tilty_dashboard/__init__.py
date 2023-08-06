# -*- coding: utf-8 -*-
""" The main method, handles all initialization """
import logging
import os

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


def init_webapp(config, test=False):
    """Initialize the web application.

    Initializes and configures the Flask web application. Call this method to
    make the web application and respective database engine usable.

    If initialized with `test=True` the application will use an in-memory
    SQLite database, and should be used for unit testing, but not much else.

    """

    # Make app work with proxies (like nginx) that set proxy headers.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # logging.getLogger('flask_cors').level = logging.DEBUG

    # Initialize Flask configuration
    if test:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    else:
        _db_uri = config['webapp']['database_uri']
        app.config['SQLALCHEMY_DATABASE_URI'] = _db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'abc123')

    # Initialize Flask-CORS
    CORS(app, supports_credentials=True)
    # CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    # Initialize Flask-Bootstrap
    Bootstrap(app)

    # Initialize Flask-SQLAlchemy
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


@socketio.on('connect', namespace='/')
def connect():
    """ todo """
    emit('refresh', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/')
def disconnect():
    """ todo """
    print('Client disconnected')


@socketio.on('refresh', namespace='/')
def message():
    """ todo """
    _gravity = 'n/a'
    try:
        _data = Tilt.query.order_by(sqlalchemy.desc(Tilt.timestamp)).first()
        _gravity = _data.gravity
    except AttributeError:
        pass
    emit('refresh', {'data': _gravity})
