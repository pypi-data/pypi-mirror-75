# -*- coding: utf-8 -*-
""" Model definitions """

import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String

db = SQLAlchemy()


class Tilt(db.Model):  # pylint:disable=too-few-public-methods
    """ the Tilt Data model """
    __tablename__ = 'data'
    id = Column(Integer(), primary_key=True)  # pylint:disable=invalid-name
    gravity = Column(Integer)
    temp = Column(Integer)
    color = Column(String(16))
    mac = Column(String(17))
    timestamp = Column(DateTime(timezone=True))

    def __repr__(self):
        return '<Tilty %r @ %r>' % (self.gravity, self.temp)


def make_conn_str():
    """Make an local database file on disk."""
    return 'sqlite:///{cwd}/database.db'.format(
        cwd=os.path.abspath(os.getcwd())
    )
