import sys
import json

from twisted.internet import reactor
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

class SyncServerProtocol(WebSocketServerProtocol):

	def onOpen(self):
		self.factory.register(self)

	def onMessage(self, msg, binary):
		msg = json.dumps({'url': msg})
		print "sending echo:", msg
		self.factory.broadcast(msg)

	def connectionLost(self, reason):
		WebSocketServerProtocol.connectionLost(self,reason)
		self.factory.unregister(self)

class SyncServerFactory(WebSocketServerFactory):

	def __init__(self, url, debug = False, debugCodePaths = False):
		WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
		self.clients = []

	def register(self, client):
		if not client in self.clients:
			print "registered client " + client.peerstr
			self.clients.append(client)

	def unregister(self, client):
		if client in self.clients:
			print "unregistered client " + client.peerstr
			self.clients.remove(client)

	def broadcast(self, msg):
		print "broadcasting message '%s' to all clients..." % msg
		for c in self.clients:
			c.sendMessage(msg)
			print "message sent to " + c.peerstr

if __name__ == '__main__':

	log.startLogging(sys.stdout)

	factory = SyncServerFactory("ws://localhost:9000", debug = False, debugCodePaths = False)
	factory.protocol = SyncServerProtocol
	listenWS(factory)

	reactor.run()