mport socket 
import threading 
import sys
import time
from random import randint
from music import *
import fileIO

BYTE_SIZE = 1024
HOST = '127.0.0.1'
PORT = 5000

class Node:

	def __init__(self, port):

		try:

			self.s = socket.socket()

			self.connections = []

			self.peers = []

			self.s.bind((HOST,PORT))

			self.listen(1)

			print("-" * 12 + "Node online" + "_" * 12)

			self.run()

		except Exception as e:
			sys.exit()