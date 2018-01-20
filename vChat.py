# @ vChat by Lyric, 2018.01
# It's the code of chatting client

import wx
import time
import socket
import thread
import telnetlib

version = "1.0"

default_server = "45.77.42.36"
default_port = 12333

default_timeout = 4

def debug_loop():
    while True:
        pass

def throw_message_box(wd, title = '', msg = ''):
    dlg = wx.MessageDialog(wd, msg, title)
    dlg.ShowModal()
    dlg.Destroy()

def ck_un(username):
    return len(username) > 0 and (not ' ' in username)

def ck_pw(password):
    return len(password) > 0

def lstC(text, username):
    arr = text.split(' ', 1)
    text_type = arr[0]
    context = arr[1]
    context = context.strip("\r\n")
    if text_type == "sys_message":
        return "[System]: " + context + "\n"
    elif text_type == "message":
        arr = context.split(' ', 1)
        usr = arr[0]
        context = arr[1]
        if username == usr:
            usr += '(Me)'
        return "[%s]: %s\n" % (usr, context)

class network: # network layer

    cc = None

    def build_connection(self, serverIP): # test the connection with an IP address
        self.cc = telnetlib.Telnet()
        flag = True
        try:
            self.cc.open(serverIP[0], serverIP[1], default_timeout)
        except socket.error:
            flag = False
        return flag

    def send_msg(self, command):
        self.cc.write(str(command) + "\r\n")

    def read(self):
        try:
            info = self.cc.read_eager()
        except EOFError:
            info = ""
        return info

    def read_ow(self):
        try:
            info = self.cc.read_until("\r\n")
        except EOFError:
            info = ""
        return info

    def close_connection(self, flag = False):
        if flag:
            self.send_msg("logout")
        self.cc.close()

class login_dialog(wx.Dialog): # the login dialog

    nc = None # network
    username = None # info

    upperIP = None # incoming ip address
    login_ok = False # status

    ID_StaticText = None # StaticText
    ID_Text = None # Text

    PW_StaticText = None # StaticText
    PW_Text = None # Text

    loginButton = None # Button
    cancelButton = None # Button

    def __init__(self, *args, **kw):
        super(login_dialog, self).__init__(*args, **kw)
        self.myCreatePanel()
        self.FunctionLinker()
        self.SetSize((250, 100))
        self.SetTitle("Login or Register")

    def FunctionLinker(self):
        self.loginButton.Bind(wx.EVT_BUTTON, self.on_login)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_login(self, event):
        username = self.ID_Text.GetValue()
        password = self.PW_Text.GetValue()

        if (not ck_un(username)) or (not ck_pw(password)):
            throw_message_box(self, "Error", "Illegal username or password.")
            return

        self.nc = network()
        flag = self.nc.build_connection(self.upperIP)

        if not flag:
            throw_message_box(self, "Error", "Unable to connect to the server.")
        else:
            self.username = username
            self.nc.send_msg("login " + username + ' ' + password)
            login_feedback = self.nc.read_ow()
            if login_feedback == "ok login\r\n":
                self.login_ok = True
                self.Close()
            else:
                throw_message_box(self, "Error", "Wrong username or password.")

    def on_cancel(self, event):
        self.Close()

    def myCreatePanel(self):

        bkg = wx.Panel(self)

        # StaticTexts
        self.ID_StaticText = wx.StaticText(bkg, label = 'Username')
        self.PW_StaticText = wx.StaticText(bkg, label = 'Password')
        vbox_static = wx.BoxSizer(wx.VERTICAL)
        vbox_static.Add(self.ID_StaticText, proportion = 0, flag = wx.EXPAND | wx.UP, border = 3)
        vbox_static.Add(self.PW_StaticText, proportion = 0, flag = wx.EXPAND | wx.UP, border = 5)

        # TextBox
        self.ID_Text = wx.TextCtrl(bkg)
        self.PW_Text = wx.TextCtrl(bkg, style = wx.TE_PASSWORD)
        vbox_text = wx.BoxSizer(wx.VERTICAL)
        vbox_text.Add(self.ID_Text, proportion = 0, flag = wx.EXPAND, border = 5)
        vbox_text.Add(self.PW_Text, proportion = 0, flag = wx.EXPAND, border = 5)

        # infoBox
        hbox_info = wx.BoxSizer()
        hbox_info.Add(vbox_static, proportion = 0, flag = wx.EXPAND, border = 5)
        hbox_info.Add(vbox_text, proportion = 1, flag = wx.EXPAND, border = 5)

        # Login Button
        self.loginButton = wx.Button(bkg, label = "Login")
        self.cancelButton = wx.Button(bkg, label = "Cancel")
        hbox_button = wx.BoxSizer()
        hbox_button.Add(self.loginButton, proportion = 1, flag = wx.EXPAND, border = 5)
        hbox_button.Add(self.cancelButton, proportion = 1, flag = wx.EXPAND, border = 5)

        # VBox
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox_info, proportion = 1, flag = wx.EXPAND, border = 5)
        vbox.Add(hbox_button, proportion = 1, flag = wx.EXPAND, border = 5)

        bkg.SetSizer(vbox)

class MainWindow(wx.Frame):

    login_ok = False # status
    username = None # info

    nc = None # network

    connectButton = None # button
    disconnectButton = None # button
    sendButton = None # Button

    statusbar = None # Statusbar

    menu_item_connect = None # Menu Item
    menu_item_disconnect = None # Menu Item
    menu_item_ccc = None # Menu Item
    menu_item_about = None # Menu Item

    server_address = None # textctrl
    chat_context = None # textctrl
    send_context = None # textctrl

    def ccAppend(self, context):
        self.chat_context.AppendText(lstC(context, self.username))

    def data_recv(self):
        while True:
            '''
            time.sleep(0.3)
            try:
                self.nc.send_msg("test")
            except socket.error:
                self.login_ok = False
                self.nc.close_connection(False)
                self.statusbar.SetStatusText('Disconnected')
                return
            '''
            try:
                msg = self.nc.read_ow()
                if msg != "":
                    self.ccAppend(msg)
            except:
                self.login_ok = False
                self.nc.close_connection(False)
                self.statusbar.SetStatusText('Disconnected')
                return

    def login(self, serverIP):
        login_dlg = login_dialog(None, title = "Login or Register")
        login_dlg.upperIP = serverIP
        login_dlg.ShowModal()
        login_dlg.Destroy()

        self.login_ok = login_dlg.login_ok
        self.nc = login_dlg.nc
        self.username = login_dlg.username
        if self.login_ok:
            self.statusbar.SetStatusText('Connected')
            thread.start_new_thread(self.data_recv, ())

    def getIP(self):
        serverIP_str = self.server_address.GetValue()
        serverIP = serverIP_str.split(':')
        if len(serverIP) == 1:
            serverIP.append(default_port)
        return (serverIP[0], int(serverIP[1]))

    def connect(self, event): # id = 2300, connect of GUI layer
        if self.login_ok:
            throw_message_box(self, "Error", "You have already logged in a server.")
            return
        serverIP = self.getIP()
        self.statusbar.SetStatusText('Connecting to %s:%d' % serverIP)
        self.server_connect = network()
        self.login(serverIP)

    def disconnect(self, event): # id = 2301, diconnect of GUI layer
        if self.login_ok:
            self.login_ok = False
            self.nc.close_connection()
            self.statusbar.SetStatusText('Disconnected')

    def clear_chat_context(self, event): # id = 2400, ccc of GUI layer
        self.chat_context.SetValue('')

    def about(self, event): # id = 2500, about of GUI layer
        throw_message_box("vChat %s" % version, "@ vChat by Lyric Zhao, 2018.01")

    def send(self, event):
        send_str = str(self.send_context.GetValue())
        if (not len(send_str)) or (not self.login_ok):
            return
        self.nc.send_msg("say " + send_str)
        self.send_context.SetValue("")
        self.statusbar.SetStatusText("You said something just now")

    def FunctionLinker(self):

        # Buttons
        self.connectButton.Bind(wx.EVT_BUTTON, self.connect)
        self.disconnectButton.Bind(wx.EVT_BUTTON, self.disconnect)
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)

        # Menu Items
        self.Bind(wx.EVT_MENU, self.connect, self.menu_item_connect)
        self.Bind(wx.EVT_MENU, self.disconnect, self.menu_item_disconnect)
        self.Bind(wx.EVT_MENU, self.clear_chat_context, self.menu_item_ccc)
        self.Bind(wx.EVT_MENU, self.about, self.menu_item_about)

    def myCreateMenu(self): # Menu Creating

        # Setting up the menu
        serverMenu = wx.Menu()
        self.menu_item_connect = serverMenu.Append(2300, "Connect", "Connect to a chat server")
        self.menu_item_disconnect = serverMenu.Append(2301, "Disconnect", "Disconnect with a chat server")

        editMenu = wx.Menu()
        self.menu_item_ccc = editMenu.Append(2400, "Clear", "Clear the chat context")

        aboutMenu = wx.Menu()
        self.menu_item_about = aboutMenu.Append(2500, "About", "About this software")

        # Setting up the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(serverMenu, "Server")
        menuBar.Append(editMenu, "Edit")
        menuBar.Append(aboutMenu, "About")
        self.SetMenuBar(menuBar)

    def myCreatePanel(self): # Panel Creating

        bkg = wx.Panel(self)

        # hbox_server
        self.server_address = wx.TextCtrl(bkg)
        self.server_address.SetValue(default_server + (":%s" % default_port))
        self.connectButton = wx.Button(bkg, label = "Connect")
        self.disconnectButton = wx.Button(bkg, label = "Disconnect")

        hbox_server = wx.BoxSizer()
        hbox_server.Add(self.server_address, proportion = 1, flag = wx.EXPAND, border = 5)
        hbox_server.Add(self.connectButton, proportion = 0, flag = wx.LEFT, border = 5)
        hbox_server.Add(self.disconnectButton, proportion = 0, flag = wx.LEFT, border = 5)

        # chat_context
        self.chat_context = wx.TextCtrl(bkg, style = wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH)

        # hbox_send
        self.send_context = wx.TextCtrl(bkg)
        self.sendButton = wx.Button(bkg, label = "Send")

        hbox_send = wx.BoxSizer()
        hbox_send.Add(self.send_context, proportion = 1, flag = wx.EXPAND)
        hbox_send.Add(self.sendButton, proportion = 0, flag = wx.LEFT, border = 10)

        # vbox
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox_server, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.UP, border = 5)
        vbox.Add(self.chat_context, proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 5)
        vbox.Add(hbox_send, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border = 5)

        bkg.SetSizer(vbox)

    def __init__(self, parent, title, size): # Window Initialization

        # Frame initialization
        wx.Frame.__init__(self, parent, title = title, size = size)

        # Components
        self.statusbar = self.CreateStatusBar()
        self.myCreateMenu()
        self.myCreatePanel()
        self.FunctionLinker()

        # Show
        self.Show(True)

if __name__ == "__main__": # main
    app = wx.App(False)
    frame = MainWindow(None, "vChat", size = (500, 400))
    try:
        app.MainLoop()
    except KeyboardInterrupt:
        print
