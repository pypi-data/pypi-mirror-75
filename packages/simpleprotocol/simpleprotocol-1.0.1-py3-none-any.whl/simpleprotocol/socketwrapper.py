import socket, sys

ENCODING="UTF-8"

class ServerSocket():
	
	def __init__(self, ip='localhost', port=10000):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (ip, port)
		self.sock.bind(self.server_address)
		self.sock.listen(1)
	
	def accept(self):
		connection, client_address = self.sock.accept()
		return [connection, client_address]
	
	def getClientObject(self):
		return self.ServerSocketHandler(*self.accept())
	
	class ServerSocketHandler():
		
		def __init__(self, connection, client_address):
			self.connection = connection
			self.client_address = client_address
			self.buffer = ""
			self.alive = True
		
		def sendLine(self, line):
			if not line.endswith("\n"): line += "\n"
			self.connection.sendall(line.encode(ENCODING))
		
		def readLine(self):
			while not "\n" in self.buffer:
				try:
					self.buffer += self.connection.recv(64).decode(ENCODING)
				except ConnectionResetError:
					self.close(response=1)
					return None
			line = self.buffer.split("\n")[0]
			self.buffer = '\n'.join(self.buffer.split("\n")[1:])
			self.tryExecOrder(line)
			return line
		
		def tryExecOrder(self, line):
			if "\k" in line:
				self.close(response=1)
		
		def close(self, response=0):
			if not response:
				self.sendLine("\k")
			else:
				self.connection.close()
				self.alive = False

class ClientSocket():
	
	def __init__(self, ip="localhost", port=10000):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (ip, port)
		self.sock.connect(self.server_address)
		self.buffer = ""
		self.alive = True
	
	def sendLine(self, line):
		if not line.endswith("\n"): line += "\n"
		self.sock.sendall(line.encode(ENCODING))
	
	def readLine(self):
		while not "\n" in self.buffer:
			try:
				self.buffer += self.sock.recv(64).decode(ENCODING)
			except ConnectionResetError:
				self.close(response=1)
				return None
		line = self.buffer.split("\n")[0]
		self.buffer = '\n'.join(self.buffer.split("\n")[1:])
		self.tryExecOrder(line)
		return line
	
	def tryExecOrder(self, line):
		if "\k" in line:
			self.close()
	
	def close(self):
		self.sendLine("\k")
		self.sock.close()
		self.alive = False

