import socket
import random
import sys
import time
from _thread import *
from queue import Queue



#create a socket
def create_socket():

  try:
    global host
    global port
    global s

    host = ''
    port= 5554
    s = socket.socket()

  except socket.error as err:
    print("socket creation error: " + str(err))

#binding the socket and listening for connections

def bind_socket():

  try:
    global host
    global port
    global s

    print ("binding the Port: " + str(port))

    s.bind((host,port))
    s.listen(5) #number of connections it tolerates before throwing error
    print("waiting for the player to get connected..") 

  except socket.error as err:
    print("socket binding error " + str(err) + "\n" + "Retrying...")
    bind_socket()

#converts '[5,5]' -> [5,5]
def parse_dataa(data):
  temp = data.split(",")
  reply = [int(temp[0].strip("[]")),int(temp[1].strip("[]"))]
  return reply

#send commands to client
def send_command(conn, player):

  #head1 = [random.randrange(1,10),random.randrange(1,10)] # random starting postion of player snake
  #body1 = [head1[:]]*5

  global pos
  conn.send(str.encode(str(pos[player])))
  print("sending: ", pos[player])

  while 1:

    if player ==1:
        reply = pos[0]
    else:
        reply = pos[1]

    try:
        print("recieving data")
        data = conn.recv(2048)
        client_response = parse_dataa(str(data,"utf-8"))
        pos[player] = client_response

        if not data:
          print("disconnected")
          break
        else:
          if player ==1:
            reply = pos[0]
          else:
            reply = pos[1]
          print("Received: ",client_response)
          print("Sending: ", reply)
        conn.send(str.encode(str(reply)))
          
          

    except:
        break

  print("connection closed")
  conn.close()



def main():


  n_of_players = int(sys.argv[1])
  print("-------THIS IS A " + str(n_of_players)+" PLAYER GAME------ ")
  start = [random.randrange(1,10),random.randrange(1,10)] # starting position
  global pos
  pos = [start[:]]*n_of_players # number of clients postions to store
  current_player = 0 #

  print("look ", pos)
  


  create_socket()
  bind_socket()

  while current_player<= n_of_players:
    conn, address = s.accept() # establish connection with a client (socket must be listening)

    print("connection has been established! " + "IP " + address[0] + "| Port " + str(address[1]))
    print("player" + str(current_player+1)+ " got connected. :) ")
    start_new_thread(send_command,(conn,current_player))
    current_player +=1



main()
