# -*- coding: utf-8 -*-
# autor: @LaercioPatricio <br />
# project: @luizalabs

import logging
import re
from core.models import Model
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# #Person: ValueObject #
# __class__: persiste dados da pessoa. Incluidos por cópia de registro no facebook
class Person(Model, Base):
	__tablename__ = 'Person'
	
	facebookId = Column(String(30), nullable=False)
	username = Column(String(200), nullable=False)
	name = Column(String(200), nullable=False)
	gender = Column(String(20), nullable=False)
		
	def __repr__(self):
	    return "<Person('%s')>" % (self.username)

def init_db(engine):
    Base.metadata.create_all(bind=engine)