# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
# DESAFIO LUIZALABS
autor: @LaercioPatricio <br />
project: @luizalabs
<br>
>Abstracao para o acesso ao banco, afim de manter uma inteface unica acima do sqlalchemy, diminuindo a visibilidade de consumidor final, para caso seja necessario alterar o acesso aos dados o código final não seja alterado
"""

import logging
import tornado.web
from sqlalchemy import Column, Integer
from sqlalchemy import func

import sys
import inspect

class AbstractModel( object ):
	pass

class Model( AbstractModel ):
	pk = Column(Integer, primary_key=True)
	_model_classname= ""

	@classmethod
	def all (cls, instance_database, *args, **kwargs):
		return instance_database.query(cls).filter_by(**kwargs).all()

	@classmethod
	def one (cls, instance_database, *args, **kwargs):
		return instance_database.query(cls).filter_by(**kwargs).one()

	@classmethod
	def count(cls, instance_database, *args, **kwargs):
		return instance_database.query(func.count(cls.pk)).scalar()

	@classmethod
	def get_page(cls, instance_database, limit, offset, *args, **kwargs):
		return instance_database.query(cls).limit(limit).offset(offset)

	def save(self, instance_database):
		indentity=0
		try:
			instance_database.add(self)
			instance_database.commit()

		except Exception as e:
			logging.error('call PersonHandler::_on_finishcall falha ao tentar incluir um registro no banco de dados:' + str(e))
			instance_database.rollback()

		finally:
			indentity = self.pk
			instance_database.close()

		return indentity

	def delete(self, instance_database):
		deleted=False
		try:
			instance_database.delete(self)
			instance_database.commit()
			deleted =True
		except Exception as e:
			logging.error('call PersonHandler::_on_finishcall falha ao tentar incluir um registro no banco de dados:' + str(e))
			instance_database.rollback()

		finally:
			indentity = self.pk
			instance_database.close()

		return deleted

	def as_dict(self):
		return {col.name: getattr(self, col.name) for col in self.__table__.columns}

	def __init__(self, *args, **kwargs):
		for key in kwargs:
			if hasattr(self, key):
				setattr(self, key, kwargs[key])