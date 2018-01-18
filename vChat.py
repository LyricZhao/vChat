# @ vChat by Lyric, 2018.01

import wx
import socket

version = "1.0"

default_server = "45.77.121.14"
default_port = 12333

default_timeout = 4

class User: # User Setting

    def __init__(self, id, username, nickname, pw):
        self.id = id
        self.username = username
        self.nickname = nickname

class Func: # Functions
    pass

class network: # network layer

    current_connection = None

    def build_connection(self, serverIP): # test the connection with an IP address
        socket.setdefaulttimeout(default_timeout)
        self.current_connection = socket.socket()
        flag = True
        try:
            self.current_connection.connect(serverIP)
        except socket.timeout:
            flag = False
        return flag

class MainWindow(wx.Frame):

    server_connect = None # network

    connectButton = None # button
    disconnectButton = None # button
    sendButton = None # Button

    statusbar = None # Statusbar

    menu_item_connect = None # Menu Item
    menu_item_disconnect = None # Menu Item
    menu_item_ccc = None # Menu Item
    menu_item_about = None # Menu Item

    def throw_message_box(self, title = '', msg = ''):
        dlg = wx.MessageDialog(self, msg, title)
        dlg.ShowModal()
        dlg.Destroy()

    def login(self, serverIP):
        pass

    def getIP(self):
        serverIP_str = self.server_address.GetValue()
        serverIP = serverIP_str.split(':')
        if len(serverIP) == 1:
            serverIP.append(default_port)
        return (serverIP[0], int(serverIP[1]))

    def connect(self, event): # id = 2300, connect of GUI layer
        serverIP = self.getIP()
        self.statusbar.SetStatusText('Connecting to %s:%d' % serverIP)
        self.server_connect = network()
        if self.server_connect.build_connection(serverIP) == False:
            self.throw_message_box("Unable to connect to %s:%d" % serverIP)
        else:
            self.login(serverIP)

    def disconnect(self, event): # id = 2301, diconnect of GUI layer
        pass

    def clear_chat_context(self, event): # id = 2400, ccc of GUI layer
        self.chat_context.SetValue('')

    def about(self, event): # id = 2500, about of GUI layer
        self.throw_message_box("vChat %s" % version, "@ vChat by Lyric Zhao, 2018.01")

    def send(self, event):
        pass

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
        self.chat_context = wx.TextCtrl(bkg, style = wx.TE_MULTILINE | wx.HSCROLL)

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
    app.MainLoop()
