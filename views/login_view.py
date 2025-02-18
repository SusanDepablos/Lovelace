import wx
from controllers.user_controller import UserController
from views.main_view import MainFrame

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Inicio de Sesión', size=(300, 250))
        self.panel = wx.Panel(self)
        self.controller = UserController()
        self.password_visible = False  # Estado de visibilidad de la contraseña

        # Elementos de la interfaz
        self.username_label = wx.StaticText(self.panel, label='Usuario:')
        self.username_text = wx.TextCtrl(self.panel)
        self.password_label = wx.StaticText(self.panel, label='Contraseña:')
        self.password_text = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        self.show_password_button = wx.Button(self.panel, label='👁')
        self.login_button = wx.Button(self.panel, label='Iniciar Sesión')

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.username_label, 0, wx.ALL, 5)
        sizer.Add(self.username_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.password_label, 0, wx.ALL, 5)

        # Contenedor para el campo de contraseña y el botón de mostrar/ocultar
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_sizer.Add(self.password_text, 1, wx.EXPAND)
        password_sizer.Add(self.show_password_button, 0, wx.LEFT, 5)
        sizer.Add(password_sizer, 0, wx.ALL | wx.EXPAND, 5)

        sizer.Add(self.login_button, 0, wx.ALL | wx.CENTER, 5)
        self.panel.SetSizer(sizer)

        # Eventos
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)
        self.show_password_button.Bind(wx.EVT_BUTTON, self.toggle_password_visibility)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_login(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        user = self.controller.authenticate_user(username, password)
        if user:
            wx.MessageBox("Inicio de sesión exitoso.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.Hide()
            self.main_frame = MainFrame(self)
            self.main_frame.Show()
        else:
            wx.MessageBox("Usuario o contraseña incorrectos.", "Error", wx.OK | wx.ICON_ERROR)

    def toggle_password_visibility(self, event):
        """ Alternar la visibilidad de la contraseña sin afectar el diseño """
        self.password_visible = not self.password_visible
        current_value = self.password_text.GetValue()

        # Cambiar el campo de texto con el nuevo estilo
        self.password_text.Destroy()
        style = 0 if self.password_visible else wx.TE_PASSWORD
        self.password_text = wx.TextCtrl(self.panel, style=style)
        self.password_text.SetValue(current_value)

        # Actualizar el botón de mostrar contraseña
        self.show_password_button.SetLabel('🙈' if self.password_visible else '👁')

        # Reasignar el evento y el diseño
        self.show_password_button.Bind(wx.EVT_BUTTON, self.toggle_password_visibility)
        self.panel.GetSizer().GetItem(3).GetSizer().Insert(0, self.password_text, 1, wx.EXPAND)
        self.panel.Layout()

    def on_close(self, event):
        self.Destroy()

    def clear_inputs(self):
        self.username_text.Clear()
        self.password_text.Clear()
