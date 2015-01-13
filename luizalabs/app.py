# -*- coding: utf-8 -*-
"""
# DESAFIO LUIZALABS
autor: @LaercioPatricio <br />
project: @luizalabs
<br>
>Esta breve api foi produzida utilizando python[#is_life] e tornadoweb.<br>
>Desafio sugerido por Renato Pedigoni.<br>
>A solicitacao é que fosse produzido um codigo simples para validar minha
forma de programar.<br>
>Para este teste foi utilizado o banco de dados SQLite por ser altamente
portavel e de facil manuseio para realizacao de testes.<br>
>Para abstracao da execução das querys junto ao banco de dados foi utilizado
o SQLAlchemy, é facil de ser utilizado e atende muito bem ao padrao ORM.<br>
"""
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


class Application(tornado.web.Application):
    def __init__(self):
        urlpatterns = [
            url(r'/person/$', PersonHandler,
                name='person_route_list'),
            url(r'/person/([\d]+)?', PersonHandler,
                name='person_route_access')]

        tornado.web.Application.__init__(self, urlpatterns, **settings.config)
        engine = create_engine(
            settings.config['database_path'],
            convert_unicode=True,
            echo=settings.config['debug'])

        pmodel.init_db(engine)
        self.data_access = scoped_session(sessionmaker(bind=engine))


def main():
    log_path = os.path.join(settings.ROOT_PATH, '_log')
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s')
    logging.info(' call: __app_init__')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(settings.config['port'])
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
