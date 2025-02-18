import wx
from controllers.user_controller import UserController

class MainFrame(wx.Frame):
    def __init__(self, login_frame):  # Recibe la referencia de LoginFrame
        super().__init__(parent=None, title='Gestión de Usuarios', size=(350, 400))
        self.panel = wx.Panel(self)
        self.controller = UserController()
        self.login_frame = login_frame  # Guarda la referencia de LoginFrame
        self.password_visible = False  # Estado de visibilidad de la contraseña

        # Elementos de la interfaz
        self.username_label = wx.StaticText(self.panel, label='Usuario:')
        self.username_text = wx.TextCtrl(self.panel)
        self.password_label = wx.StaticText(self.panel, label='Contraseña:')
        self.password_text = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        self.show_password_button = wx.Button(self.panel, label='👁')
        self.add_button = wx.Button(self.panel, label='Agregar Usuario')
        self.logout_button = wx.Button(self.panel, label='Cerrar Sesión')
        self.user_list = wx.ListBox(self.panel)

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

        sizer.Add(self.add_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.logout_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.user_list, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(sizer)

        # Eventos
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_user)
        self.logout_button.Bind(wx.EVT_BUTTON, self.on_logout)
        self.show_password_button.Bind(wx.EVT_BUTTON, self.toggle_password_visibility)
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Manejar el evento de cierre

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
        self.login_frame.clear_inputs()  # Limpiar los inputs de LoginFrame
        self.Close()  # Cierra la MainFrame
        self.login_frame.Show()  # Muestra la LoginFrame nuevamente

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
        # Cerrar la aplicación completamente
        self.Destroy()
