# @ vChat by Lyric, 2018.01
# It's the code of chatting server

from asyncore import dispatcher
from asynchat import async_chat

import socket
import sqlite3
import asyncore

server_port = 12333
server_name = 'vChat'

class EndSession(Exception): pass
class UnknownError(Exception): pass

def debug_loop():
    while True:
        pass

class commandHandler:

    def handle(self, session, line): # handle a command received from a session
        print "got request: " + line
        if not line:
            return
        parts = line.split(' ', 1)
        instruction = parts[0]
        if len(parts) > 1:
            line = parts[1]
        else:
            line = ''
        if instruction == 'login': # login
            self.m_login(session, line)
        elif instruction == 'logout': # logout
            self.m_logout()
        elif instruction == 'say': # say
            self.m_say(session, line)
        else: # unknown command
            raise UnknownError

class Room(commandHandler): # a chatting room

    server = None
    sessions = None
    database = None
    name = None

    def __init__(self, server, name = 'vChat'): # initialization
        self.server = server
        self.sessions = []
        self.database = {}
        self.name = name

    def check_in_db(self, line):
        parts = line.split(' ', 1)
        username = parts[0]
        password = parts[1]
        if not self.database.has_key(username):
            self.database[username] = password
        flag = (self.database[username] == password)
        for session in self.sessions:
            if session.name == username:
                flag = False
        return flag

    def add(self, session): # add an user to the room
        self.sessions.append(session)

    def remove(self, session): # remove an user from a room
        self.sessions.remove(session)

    def m_say(self, session, line): # say something
        self.broadcast(session.name + " " + line)

    def broadcast(self, line): # send a message to everyone
        if not len(self.sessions):
            return
        for session in self.sessions:
            session.push("message " + line + "\r\n")

    def m_logout(self): # logout
        raise EndSession

class loginRoom(Room):

    def m_login(self, session, line):
        session.name = (line.split(' '))[0]
        if self.server.main_room.check_in_db(line) == True:
            print("ok login")
            session.push("ok login" + "\r\n")
            session.push("message " + ("Welcome to %s" % self.server.main_room.name) + "\r\n")
            session.push_all(self.server.main_room.sessions)
            self.server.main_room.broadcast("sys_message " + session.name + " joins the chat.")
            session.enter(self.server.main_room)
        else:
            print("error login")
            session.push("error login" + "\r\n")
            raise EndSession

class chatSession(async_chat): # communicate with a single user

    server = None
    data = None
    room = None
    name = None

    def __init__(self, server, sock):

        print("coming connection")

        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator('\r\n')
        self.data = []

        self.enter(loginRoom(server)) # login

    def push_all(self, sarr):
        if len(sarr):
            arr = []
            for session in sarr:
                arr.append(session.name)
            users = ", ".join(arr)
            self.push("sys_message " + "online users in this room: " + users + "\r\n")
        else:
            self.push("sys_message " + "nobody online now" + "\r\n")

    def enter(self, room): # remove and put in a new room
        cur = self.room
        if cur == None:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.close(self)
        print "Connection is interrupted"
        tmp = self.room
        tmp.remove(self)
        if self.name != None:
            tmp.broadcast("sys_message " + self.name + " leaves the chat.")

class ChatServer(dispatcher):

    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = Room(self, "305B")

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
