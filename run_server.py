activate_this = 'venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from gevent.wsgi import WSGIServer
from main import app

http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
