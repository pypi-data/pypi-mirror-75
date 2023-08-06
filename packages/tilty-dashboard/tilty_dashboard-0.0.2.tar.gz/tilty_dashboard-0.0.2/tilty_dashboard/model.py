# -*- coding: utf-8 -*-
""" Model definitions """

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
