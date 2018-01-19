# @ vChat by Lyric, 2018.01
# It's the code of chatting server

from asyncore import dispatcher
from asynchat import async_chat

import socket
import sqlite3
import asyncore

server_port = 12333
server_name = 'vChat'

class EndSession(Expection): pass
class UnknownError(Expection): pass

class commandHandler:

    def handle(self, session, line): # handle a command received from a session
        if not line:
            return
        parts = line.split('', 1)
        instruction = parts[0]
        if len(parts) > 1:
            line = parts[1]
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
        return (self.database[username] == password)

    def add(self, session): # add an user to the room
        self.sessions.append(session)

    def remove(self, session): # remove an user from a room
        self.sessions.remove(session)

    def broadcast(self, line): # send a message to everyone
        for session in self.sessions:
            session.push("message " + line)

    def m_logout(self, line): # logout
        raise EndSession

class loginRoom(Room):

    def m_login(self, session, line):
        if self.server.main_room.check_in_db(line) == True:
            session.push("message " + ("Welcome to %s" % self.name))
            session.enter(self.server.main_room)
        else:
            session.push("error login")
            raise EndSession

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
        self.data = []
        try:
            self.room.handle(self, line)
        except:
            self.handle_close()

    def close(self):
        async_chat.close(self)
        self.room.remove(self)

class ChatServer(dispatcher):

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
