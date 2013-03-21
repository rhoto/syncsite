import sys
import json

from time import time

from twisted.internet import reactor
from twisted.python import log

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

from gdata.youtube import service

USERNAME = 'sinktubrtv@gmail.com'
PASSWORD = 'notasecret'

class SyncServerProtocol(WebSocketServerProtocol):

	def onOpen(self):
		self.factory.register(self)

	def onMessage(self, msg, binary):
		factory.vid.getVideoLength(msg)
		jsonMsg = {'status':'setVideo', 'video_id':msg}
		msg = json.dumps(jsonMsg)
		print "sending echo:", msg
		self.factory.broadcast(msg)

	def connectionLost(self, reason):
		WebSocketServerProtocol.connectionLost(self,reason)
		self.factory.unregister(self)

class SyncServerFactory(WebSocketServerFactory):

	def __init__(self, url, debug = False, debugCodePaths = False):
		WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
		self.vid = VideoHandler()
		self.clients = []
		self.tick()

	def tick(self):
		self.vid.tick()
		reactor.callLater(1, self.tick)

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

class VideoHandler:
	def __init__(self):
		self.client = service.YouTubeService()
		self.client.email = USERNAME
		self.client.password = PASSWORD
		self.client.source = 'sinktub'
		self.client.ProgrammaticLogin()

		self.setCurrentVideo(video_id='Fln69C4_Ld0')

	def setCurrentVideo(self, video_id):
		self.currentVideoID = video_id
		self.currentVideoDuration = self.getVideoLength(video_id)
		self.ticks = 0

	def tick(self):
		self.ticks += 1
		#if self.ticks > self.currentVideoDuration:
			# next


	def getVideoLength(self, video_id):
		print "Getting video information for " + video_id + "..."
		videoEntry = self.client.GetYouTubeVideoEntry(video_id=video_id)
		print videoEntry.media.title.text
		print videoEntry.media.duration.seconds
		return videoEntry.title.duration.seconds


if __name__ == '__main__':

	log.startLogging(sys.stdout)



	factory = SyncServerFactory("ws://localhost:64100", debug = False, debugCodePaths = False)
	factory.protocol = SyncServerProtocol
	listenWS(factory)

	reactor.run()