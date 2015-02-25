# -*- coding: utf-8 -*-
# !/bin/env python
import wx

import pyScoliosisUI as ui


if "2.8" in wx.version():
    import wx.lib.pubsub.setupkwargs
    from wx.lib.pubsub import pub
else:
    from wx.lib.pubsub import pub


class LoginDialog():
    def __init__(self, parent):
        ui.LoginDialogBase.__init__(self, parent)

    def login(self, event):
        stupid_password = "password"
        user_password = self.txt_password.GetValue()
        if user_password == stupid_password:
            print "You are now logged in!"
            pub.sendMessage("frameListener", message="show")
            self.Destroy()
        else:
            print "Username or password is incorrect!"
            self.Destroy()

    def cancel(self, event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = ui.mainForm(None)
    frame.Show(True)
    app.MainLoop()
