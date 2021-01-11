#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

from gevent import monkey; monkey.patch_all()

import os, socket, sys
from bottle import ServerAdapter, get, view, static_file, run

from gevent.pywsgi import WSGIServer

class CustomServer(ServerAdapter):
	def __init__(self, unixsocket, **options):
		super().__init__(**options)
		self.unixsocket = unixsocket
		
	def run(self, handler):
		# create listener for unix socket
		if os.path.exists(self.unixsocket):
			os.remove(self.unixsocket)
		listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		listener.bind(self.unixsocket)
		listener.listen(1)
		# create server
		server = WSGIServer(listener, handler, **self.options)
		server.serve_forever()

@get('/')
@view('demo')
def test():
	return dict()

@get('/static/<fname>')
def static_files(fname):
	return static_file(fname, root='files')

if '--socket' in sys.argv:
	run(unixsocket='/tmp/demo.sock', server=CustomServer)
else:
	run(host='localhost', port=8000)
