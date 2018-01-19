# @ vChat by Lyric, 2018.01
# It's the code of chatting server

from asyncore import dispatcher
from asynchat import async_chat

import socket
import sqlite3
import asyncore

server_port = 12333
server_name = 'vChat'

class endSession(Expection):
    pass

class Room: # a chatting room

    server = None
    sessions = None

    def __init__(self, server): # initialization
        self.server = server
        self.sessions = []

    def add(self, user): # add an user to the room
        self.sessions.append(user)

    def remove(self, user): # remove an user from a room
        self.sessions.remove(user)

    def broadcast(self, line): # send a message to everyone
        for user in self.sessions:
            user.push(line)

class loginRoom(Room):
    pass

class chatSession(asynchat): # communicate with a single user

    server = None
    data = None
    room = None

    def __init__(self, server, sock):
        asynchat_chat.__init__(self, sock)
        self.server = server
        self.set_terminator('\r\n')
        self.data = []
        self.enter(loginRoom(server)) # login

    def enter(self, room): # remove and put in a new room
        cur = self.room
        if cur == None:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        

class ClassServer(dispatcher):

    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = chatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        chatSession(self, conn)

if __name__ == '__main__': # main
    server = ChatServer(server_port, server_name)
    # running
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print
