import wx
from controllers.user_controller import UserController
from views.main_view import MainFrame

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Inicio de Sesión', size=(300, 200))
        self.panel = wx.Panel(self)
        self.controller = UserController()

        # Elementos de la interfaz
        self.username_label = wx.StaticText(self.panel, label='Usuario:')
        self.username_text = wx.TextCtrl(self.panel)
        self.password_label = wx.StaticText(self.panel, label='Contraseña:')
        self.password_text = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        self.login_button = wx.Button(self.panel, label='Iniciar Sesión')

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.username_label, 0, wx.ALL, 5)
        sizer.Add(self.username_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.password_label, 0, wx.ALL, 5)
        sizer.Add(self.password_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.login_button, 0, wx.ALL | wx.CENTER, 5)
        self.panel.SetSizer(sizer)

        # Eventos
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)

    def on_login(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        user = self.controller.authenticate_user(username, password)
        if user:
            wx.MessageBox("Inicio de sesión exitoso.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.Hide()
            self.main_frame = MainFrame()
            self.main_frame.Show()
        else:
            wx.MessageBox("Usuario o contraseña incorrectos.", "Error", wx.OK | wx.ICON_ERROR)