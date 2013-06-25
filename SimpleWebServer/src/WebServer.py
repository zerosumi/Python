'''
Created on Oct 1, 2012

@author: ElliottRen
'''
# Import socket module
import socket
import sys
import threading    
#import socket
class Server:
	def __init__(self):
		self.hostname = '127.0.0.1'
		self.port = 9000
		self.backlog = 5
		self.threadnumber = 5
		self.server = None
		self.threads = []
	def open_socket(self):
		try:
			# Create a TCP server socket
			#(AF_INET is used for IPv4 protocols)
			#(SOCK_STREAM is used for TCP)
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# Bind the socket to server address and server port
			self.server.bind((self.hostname, self.port))
			# Listen to connections
			self.server.listen(self.backlog)
		except socket.error, (value,message):
			if self.server:
				self.server.close()
			print 'Could not open socket: ' + message
			sys.exit(1)
	def run(self):
		self.open_socket()
		print 'Ready to serve...'
		# Server should be up and running and listening to the incoming connections
		while True:
			# Set up a new connection from the client
			ct = Client(self.server.accept())
			ct.start()
			self.threads.append(ct)
		self.server.close()
		for ct in self.threads:
			ct.join()
			
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
class Client(threading.Thread):
	def __init__(self,(client,address)):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
	def run(self):
		try:
			# Receives the request message from the client using the recv method
			data = self.client.recv(1024)
			print self.getName()
			print repr(data)
			# Extract the path of the requested object from the message. The path is the second part of HTTP header
			linktype = data.split()[0]
			print 'Link Type:', linktype
			filename = data.split()[1]
			print 'Path:', filename
			# Open and read the corresponding file 
			if (filename == '/'):
				filename = '/index.html'
			f = open(filename[1:])
			# Store the entire content of the requested file in a temporary buffer
			outputdata = f.read()
			# Send the HTTP response header line to the connection socket
			self.client.send('HTTP/1.1 200 OK\r\n\r\n')
			# Send the content of the requested file to the connection socket
			for i in range(0, len(outputdata)):
				self.client.send(outputdata[i])
			# Close the client connection socket
			self.client.close()
		except IOError:
			# Send HTTP response message for file not found
			self.client.send('HTTP/1.1 404 NOT FOUND\r\n\r\n')
			# Close the client connection socket
			self.client.close()
			
if __name__ == "__main__":
	s = Server()
	s.run()