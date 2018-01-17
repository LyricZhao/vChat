# @ vChat by Lyric, 2018.01

import wx

version = "1.0"

class Func: # Functions
    pass

class MainWindow(wx.Frame):

    def connect(self, event): # id = 2300, connect of GUI layer
        pass

    def disconnect(self, event): # id = 2301, diconnect of GUI layer
        pass

    def clear_chat_context(self, event): # id = 2400, ccc of GUI layer
        self.chat_context.SetValue('')

    def about(self, event): # id = 2500, about of GUI layer
    
        about_dialog = wx.MessageDialog(self, "@ vChat by Lyric Zhao, 2018.01", "vChat %s" % version)
        about_dialog.ShowModal()
        about_dialog.Destroy()
        pass

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
        self.server_address.SetValue("45.77.121.14:12333")
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
        self.CreateStatusBar()
        self.myCreateMenu()
        self.myCreatePanel()
        self.FunctionLinker()

        # Show
        self.Show(True)

if __name__ == "__main__": # main
    app = wx.App(False)
    frame = MainWindow(None, "vChat", size = (500, 400))
    app.MainLoop()
