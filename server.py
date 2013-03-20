import sys
import json

from twisted.internet import reactor
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

class SyncServerProtocol(WebSocketServerProtocol):

	def onMessage(self, msg, binary):
		msg = json.dumps({'url': msg})
		print "sending echo:", msg
		self.sendMessage(msg, False)

if __name__ == '__main__':

	log.startLogging(sys.stdout)

	factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
	factory.protocol = SyncServerProtocol
	listenWS(factory)

	reactor.run()