import os
from tornado.options import define, options

FACEBOOK_GRAPH_URL = "https://graph.facebook.com/{0}"
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_STRING = os.path.join(ROOT_PATH, 'database/luizalabs.sqlite')

define("port", default=5000, help="run on the given port", type=int)
define("debug", default=True, type=bool)
define("db_path", default=('sqlite:///%s' % DATABASE_STRING), type=str)

config = dict(
    debug=options.debug,
    port=options.port,
    database_path=options.db_path,
    static_path=os.path.join(ROOT_PATH, 'static')
    )
