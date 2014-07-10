#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx
import hashlib
from models import User
from elixir import *
setup_all()


class Login(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title='Maat - Login', style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.Centre(wx.BOTH)

        self.ico = wx.Icon("./imagens/pena.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        panelLogin = wx.Panel(self, 1)

        self.vBox1 = wx.BoxSizer(wx.VERTICAL)
        self.hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.labelUser = wx.StaticText(panelLogin, -1, u'Usuário: ', pos=(5, 34), style=wx.ALIGN_LEFT)
        self.inputUser = wx.TextCtrl(panelLogin, -1, pos=(60, 30), size=(180, -1), style=wx.ALIGN_LEFT)

        
        self.labelPass = wx.StaticText(panelLogin, -1, u'Senha:', pos=(5, 65), style=wx.ALIGN_LEFT)
        self.inputPass = wx.TextCtrl(panelLogin, -1, pos=(60, 61), size=(180, -1), style=wx.ALIGN_LEFT | wx.TE_PASSWORD)
        
        self.btnEntrar = wx.Button(panelLogin, wx.ID_OK, label=u"Entrar", pos=(40, 100))
        self.btnSair = wx.Button(panelLogin, wx.ID_EXIT, label=u"Sair", pos=(130, 100))
        self.Bind(wx.EVT_BUTTON, self.valida, self.btnEntrar)
        self.Bind(wx.EVT_BUTTON, self.quit, self.btnSair)

        self.Bind(wx.EVT_CLOSE, self.closeWindow)

        self.SetSize((250, 170))
        self.Show()

        
    def closeWindow(self, event):
        self.Destroy()

    def valida(self, event):
        user = User.query.filter(User.login.like(self.inputUser.GetValue())).first()

        if user != None:
            if user.password == hashlib.sha1(self.inputPass.GetValue()).hexdigest():
                if user.level == 0:
                    self.Destroy()
                    import WindowMain
                    WindowMain.WindowMain(user)
                else:
                    self.Destroy()
                    import WindowNormal
                    WindowNormal.WindowNormal(user)

            else:
                self.errorLogin()
        else:
            self.errorLogin()

    def quit(self, event):
        self.Close(True)

    def errorLogin(self):
        self.dialog = wx.MessageDialog(self, u"Nome do usuário ou senha inválidos.\nDigite-os novamente.", u"Acesso Negado", wx.YES_DEFAULT | wx.ICON_INFORMATION)
        self.dialog.ShowModal()
        self.inputUser.SetValue('')
        self.inputPass.SetValue('')
        self.inputUser.SetFocus()
