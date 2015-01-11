import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
import re
import json
import logging

from core.utils import Pagination
from core.handlers import BaseHandler
from person.models import Person
import settings
import core.utils as utils

class PersonHandler(BaseHandler):
	def validate_facebookid(self, facebookId):
		match_validate = re.match(r'^[0-9]+$', facebookId)
		if not match_validate:
			self.clear()
			logging.error("call PersonHandler::post - facebookid invalido")
			raise tornado.web.HTTPError(self.HTTP_STATUS_CODE_BAD_REQUEST, 'facebookId invalido')

	def render_strategy_unique(self, facebookId):
		try:
			person = Person.one(self._data_access, facebookId=facebookId)
		except:
			logging.error("call PersonHandler::render_strategy_unique - facebookid invalido")
			raise tornado.web.HTTPError(self.HTTP_STATUS_CODE_NOT_FOUND, 'facebookId invalido')

		return json.dumps(person.as_dict())

	def render_strategy_list(self, limit):
		page = self.get_argument("page", 1, True)
		start = -1
		if limit is None:
			limit = utils.MAX_UNLIMITED_PAGE
			start = 0

		pagination = utils.Pagination(page=int(page), limit=int(limit), total_count=Person.count(self._data_access))
		
		if start == -1:
			start = int(pagination['page']*pagination['limit'])-1

		try:
			persons = Person.get_page(self._data_access, 
									limit=pagination['limit'], 
									offset=start).all()

			response = {'data': [item.as_dict() for item in persons],
						'pagination': pagination }

		except Exception as e:
			logging.error("call PersonHandler::render_strategy_list - database invalid error")
			raise tornado.web.HTTPError(self.HTTP_STATUS_CODE_INTERNAL_ERROR, 'por favor, contate um administrador')
			

		return json.dumps(response)

	def render_response(self, facebookId, limit):
		if facebookId is not None:
			return self.render_strategy_unique(facebookId)
		else :
			return self.render_strategy_list(limit)

	def get(self, facebookId=None):
		self.write(self.render_response(facebookId, self.get_argument("limit", None, True)))
		self.set_header("Content-Type", "application/json")
		self.finish()

	@tornado.web.asynchronous
	def post (self):
		raiseErrorIfNull = True
		facebookId = self.post_data('facebookId', raiseErrorIfNull)
		self.validate_facebookid(facebookId)

		response = ""
		person = Person.all(self._data_access, facebookId=facebookId)
		returns_count = len(person)

		if returns_count > 0:
			self.clear()
			logging.error("call PersonHandler::post - registro de usuario duplicado, ou tentativa de duplicacao na base {0}".format(facebookId))
			raise tornado.web.HTTPError(self.HTTP_STATUS_CODE_INTERNAL_ERROR, 'duplicacao de registro, por favor utilize o verbo put para editar o registro ou contate o adminstrados levando facebookid')
				
		http = AsyncHTTPClient()
		http.fetch(settings.FACEBOOK_GRAPH_URL.format(facebookId), self._on_finishcall)
		
	def _on_finishcall(self, response):
		facebookData = json.loads(response.body)

		if facebookData.has_key('error'):
			logging.error("call PersonHandler::_on_finishcall - usuario nao encontrado no facebook ")
			self.clear()
			raise tornado.web.HTTPError(self.HTTP_STATUS_CODE_BAD_REQUEST, 'facebookId inexistente')
		
		person = Person(**facebookData)
		person.facebookId = facebookData['id']
		inserted_pk = person.save(self._data_access)

		self.write({'pk': inserted_pk})
		self.set_header("Content-Type", "application/json")
		self.finish()

	def put(self):
		logging.warning('call: PersonHandler::put - metodo nao implementado sendo chamado.')
		raise NotImplementedError

	def delete(self, facebookId):
		self.validate_facebookid(facebookId) # redundante pela validacao da url, porem outras urls podem utiliza o mesmo metodo
		deleted = False
		try:
			person = Person.one(self._data_access, facebookId=facebookId)
		except:
			logging.error("call PersonHandler::delete - facebookid invalido")
			raise tornado.web.HTTPError(self.HTTP_STATUS_CODE_BAD_REQUEST, 'facebookId invalido')

		try:
			deleted = person.delete(self._data_access)
			self.set_status(self.HTTP_STATUS_CODE_NO_CONTENT)

		except Exception, e:
			logging.error("call PersonHandler::delete error: {0}".format(str(e)))
			logging.error("call PersonHandler::post - registro de usuario duplicado, ou tentativa de duplicacao na base {0}".format(facebookId))
			raise e

		self.write({'facebookId': facebookId, 'deleted': deleted})
		self.set_header("Content-Type", "application/json")
		self.finish()	
		