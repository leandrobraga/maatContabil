#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import access


if __name__ == '__main__':
    
    app = wx.App(redirect=False)
    access = access.Login()
    app.MainLoop()
