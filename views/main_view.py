import wx
from controllers.user_controller import UserController

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Gestión de Usuarios', size=(350, 400))
        self.panel = wx.Panel(self)
        self.controller = UserController()

        # Elementos de la interfaz
        self.username_label = wx.StaticText(self.panel, label='Usuario:')
        self.username_text = wx.TextCtrl(self.panel)
        self.password_label = wx.StaticText(self.panel, label='Contraseña:')
        self.password_text = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        self.add_button = wx.Button(self.panel, label='Agregar Usuario')
        self.logout_button = wx.Button(self.panel, label='Cerrar Sesión')
        self.user_list = wx.ListBox(self.panel)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.username_label, 0, wx.ALL, 5)
        sizer.Add(self.username_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.password_label, 0, wx.ALL, 5)
        sizer.Add(self.password_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.add_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.logout_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.user_list, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(sizer)

        # Eventos
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_user)
        self.logout_button.Bind(wx.EVT_BUTTON, self.on_logout)

        # Cargar usuarios
        self.load_users()

    def load_users(self):
        self.user_list.Clear()
        users = self.controller.get_users()
        for user in users:
            self.user_list.Append(f"{user.username} (ID: {user.id})")

    def on_add_user(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        success, message = self.controller.add_user(username, password)
        wx.MessageBox(message, "Información", wx.OK | (wx.ICON_INFORMATION if success else wx.ICON_ERROR))

        if success:
            self.load_users()
            self.username_text.Clear()
            self.password_text.Clear()

    def on_logout(self, event):
        self.Close()