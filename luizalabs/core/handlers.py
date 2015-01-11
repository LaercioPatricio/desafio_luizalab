import tornado.web
import urllib
import logging


class BaseHandler(tornado.web.RequestHandler):
	SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
	HTTP_STATUS_CODE_INTERNAL_ERROR = 500
	HTTP_STATUS_CODE_NOT_FOUND = 404
	HTTP_STATUS_CODE_CREATED = 201
	HTTP_STATUS_CODE_NO_CONTENT = 204
	HTTP_STATUS_CODE_NOT_MODIFIED = 304
	HTTP_STATUS_CODE_BAD_REQUEST = 400

	@property
	def _data_access(self):
		return self.application.data_access

	def getJsonData(self):
		try:
			import simplejson as json
		except ImportError:
			import json

		try:
			return json.loads(self.request.body)
		except:
			try:
				return json.loads(urllib.unquote_plus(self.request.body))
			except:
				raise NameError('InvalidData')


	def post_data(self, key, raise_ifnull=False):
		if self.request.body_arguments.has_key(key):
			item = self.request.body_arguments[key]
			if len(item) == 1:
				return item[0]
			else:
				return item

		else:
			if raise_ifnull:
				logging.error('call: basehandler::post_data - error_to_name_request: %s' % (key))
				raise NameError('InvalidBodyParamn')
			else:
				return ''