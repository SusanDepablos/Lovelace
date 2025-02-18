from models.database import init_db
import wx
from views.login_view import LoginFrame

if __name__ == "__main__":
    init_db()
    app = wx.App(False)
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()