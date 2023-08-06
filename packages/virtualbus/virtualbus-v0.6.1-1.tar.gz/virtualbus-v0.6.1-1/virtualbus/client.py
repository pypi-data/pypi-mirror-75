#!/usr/bin/env python3

import socket
import time

class Client():
	def __init__(self, host, port, logging=False, timeout_msec=1000):
		"""
		Initializes the virtual bus client
		host:    The ip address or the domain name of the server.
		port:    The port of the server.
		logging: {En/dis)able the debugging printing.
		timeout: The time to wait after an unsuccessfull connection [in sec].
		"""
		self.host = host
		self.port = port

		self.logging = logging
		self.timeout_msec = timeout_msec

		self.sock = None
		self._open()

	def __del__(self):
		"""Deinitialises the virtual bus client"""
		self._close()

	def log(self, msg):
		if self.logging is True:
			print(str(msg))

	def _open(self):
		"""Opens a connection if not already open"""
		if self.sock is not None:
			# Connection is already closed
			#self.log("Already open")
			return

		# Connection was not open so we will keep trying connecting
		numOfTries=0
		while self.sock is None:
			self.log("Trying to reconnect...[{}]".format(numOfTries))
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			#self.sock.settimeout( 10 ) #sec

			try:
				self.sock.connect((self.host, self.port))
			except Exception as e:
				#self.log("Could not connect to {}:{}".format(self.host,self.port))
				self.sock = None
				time.sleep((int)(self.timeout_msec/1000))
			finally:
				numOfTries = numOfTries + 1
		print("Connected to {}:{}".format(self.host, self.port))

	def _close(self):
		"""Closes a connection"""
		if self.sock is None:
			# Connection is already closed
			#self.log("Already closed")
			return

		# Connection is open so We need to close it
		time.sleep( 0.1 )
		try:
			self.sock.shutdown(1)
			self.sock.close()
		except Exception as e:
			self.log("Could not close socket")
		finally:
			self.sock = None
			#self.log("Closed")

	def sent(self, msg):
		"""Sents a message"""

		isSent = False
		while isSent is False:
			if self.sock is not None:
				try:
					isSent = True
					self.sock.sendall(str.encode(msg, 'utf-8'))
				except Exception as e:
					isSent = False
					self.log("Could not sent msg")
					self._close()
					self._open()

	def receive(self, chars=1024, block=True):
		"""Receives a message"""

		try:
			data = self.sock.recv(chars)
			data = data.decode()
		except Exception as e:
			self.log("Could not receive msg")
			data = None

		if data is None or data is "":
			self._close()
			self._open()

		return data

def main():
	try:
		b = Client(host="127.0.0.1", port=8888, logging=True)
		while True:
			b.sent("Hello from Virtual Bus Client!")

			m = b.receive()

			if m is not None:
				print(m)

			time.sleep( 0.5 )
	except KeyboardInterrupt:
		pass


if __name__ == "__main__":
	main()
