import os
import logging
import tornado.ioloop
import tornado.httpserver
import tornado.options

from tornado.web import url
from person.handlers import PersonHandler
import person.models.personmodel as pmodel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import settings
"""
Create and manage a new sqlite database.
"""

class Application(tornado.web.Application):

    def __init__(self):
        urlpatterns = [
            url(r'/person/$', PersonHandler, name='person_route_list'),
            url(r'/person/([\d]+)?', PersonHandler, name='person_route_access'),
        ]

        tornado.web.Application.__init__(self, urlpatterns, **settings.config)
        engine = create_engine(settings.config['database_path'], convert_unicode=True, echo=settings.config['debug'])
        pmodel.init_db(engine)
        self.data_access = scoped_session(sessionmaker(bind=engine))

def main():
    """This function translates foo into bar

    :param foo: A string to be converted
    :returns: A bar formatted string
    """    
    log_path = os.path.join(settings.ROOT_PATH, '_log')
    logging.basicConfig(filename=log_path, 
                        format='%(asctime)s %(message)s')
    logging.info(' call: __app_init__')
    
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(settings.config['port'])
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
