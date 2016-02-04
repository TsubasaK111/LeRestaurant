from flask import Flask

import pprint, pdb, logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.from_pyfile('default_config.py')
app.config.from_envvar('LERESTAURANT_SETTINGS', silent=True)

logging.basicConfig( filename='log.log',
                     level=logging.DEBUG,
                     format='%(levelname)s: %(message)s [%(asctime)s]',
                     datefmt='%m/%d/%Y %I:%M:%S %p' )

# create console handler, set level to debug and add to logger
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)


from leRestaurant.views import *
# pdb.set_trace()
