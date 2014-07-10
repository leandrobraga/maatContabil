# -*- coding: utf-8 -*-

#Copyright 2012 Leandro Quadros Durães Braga

#Este arquivo é parte do programa Sistema de Controle de Paciente(SCP)
#Sistema de Controle de Paciente(SCP) é um software livre; você pode redistribui-lo e/ou
#modifica-lo dentro dos termos da Licença Pública Geral GNU como
#publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
#Este programa é distribuido na esperança que possa ser  util,
#mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
#Você deve ter recebido uma cópia da Licença Pública Geral GNU
#junto com este programa, se não, escreva para a Fundação do Software
#Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import wx
import wx.grid
from wx.lib import masked
from models import User
from elixir import *
import hashlib

setup_all()

#ID para toolbar da janela de administrador
ID_TOOLBAR_USER_NEW = 601
ID_TOOLBAR_USER_SAVE = 602
ID_TOOLBAR_USER_REMOVE = 603
ID_TOOLBAR_USER_FIND = 604
ID_TOOLBAR_USER_EDIT = 605
ID_TOOLBAR_USER_CANCEL = 610
ID_TOOLBAR_USER_FIRST = 606
ID_TOOLBAR_USER_LAST = 607
ID_TOOLBAR_USER_NEXT = 608
ID_TOOLBAR_USER_PREVIOUS = 609

#ID para o dialog localizar
ID_FIND_SEARCH = 5041


class WindowUser(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(790, 300), pos=(300, 170), title=u"Cadastro de Usuários", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        self.currentIndex = 0
        self.totalIndex = len(User.query.all())-1

        self.parent = parent
        self.panelUser = wx.Panel(self, wx.ID_ANY)

        self.ico = wx.Icon("./imagens/users.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_FIRST, u"Primeiro", wx.Bitmap("./imagens/first.png"), shortHelp=u'Ir para o primeiro registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_PREVIOUS, u"Anterior", wx.Bitmap("./imagens/previous.png"), shortHelp=u'Registro anterior')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_NEXT, u"Próximo", wx.Bitmap("./imagens/next.png"), shortHelp=u'Próximo registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_LAST, u"Último", wx.Bitmap("./imagens/last.png"), shortHelp=u'Ir para o último registro')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()

        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_NEW, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Novo Registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_SAVE, "Salvar", wx.Bitmap("./imagens/filesave.png"), shortHelp=u'Grava alterções no registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_REMOVE, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Remove o registro atual')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_FIND, "Localizar", wx.Bitmap("./imagens/find.png"), shortHelp=u'Localiza um Registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_EDIT, "ALterar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Altera o registro atual')
        self.toolBar.AddLabelTool(ID_TOOLBAR_USER_CANCEL, "Cancelar", wx.Bitmap("./imagens/cancel.png"), shortHelp=u'Cancela ação')

        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)

        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.vBox1 = wx.BoxSizer(wx.VERTICAL)

        self.hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.idTextCtrl = wx.TextCtrl(self.panelUser, -1, pos=(10, 15), size=(0, 0))
        self.hBox2.Add(self.idTextCtrl, 1, wx.LEFT, 8)

        self.nameStaticText = wx.StaticText(self.panelUser, -1, 'Nome', pos=(18, 30), style=wx.ALIGN_LEFT)
        self.nameTextCtrl = wx.TextCtrl(self.panelUser, -1, pos=(18, 50), size=(300, -1), style=wx.TE_READONLY)
        self.hBox1.Add(self.nameStaticText, 1, wx.LEFT, 8)
        self.hBox2.Add(self.nameTextCtrl, 1, wx.LEFT, 8)

        self.loginStaticText = wx.StaticText(self.panelUser, -1, 'Login', pos=(18, 80), style=wx.ALIGN_LEFT)
        self.loginTextCtrl = wx.TextCtrl(self.panelUser, -1, pos=(18, 100), size=(150, -1), style=wx.TE_READONLY)
        self.hBox1.Add(self.loginStaticText, 1, wx.LEFT, 8)
        self.hBox2.Add(self.loginTextCtrl, 1, wx.LEFT, 8)

        self.cb = wx.CheckBox(self.panelUser, label='Administrador', pos=(200, 105))
        self.cb.Disable()

        self.passwordStaticText = wx.StaticText(self.panelUser, -1, 'Senha', pos=(18, 140), style=wx.ALIGN_LEFT)
        self.passwordTextCtrl = wx.TextCtrl(self.panelUser, -1, pos=(18, 160), size=(100, -1), style=wx.TE_PASSWORD)
        self.passwordTextCtrl.Disable()
        self.passwordTextCtrl.SetEditable(False)
        self.hBox1.Add(self.passwordStaticText, 1, wx.LEFT, 8)
        self.hBox2.Add(self.passwordTextCtrl, 1, wx.LEFT, 8)

        self.confirmPasswordStaticText = wx.StaticText(self.panelUser, -1, 'Confirma Senha', pos=(200, 140), style=wx.ALIGN_LEFT)
        self.confirmPasswordTextCtrl = wx.TextCtrl(self.panelUser, -1, pos=(200, 160), size=(100, -1), style=wx.TE_PASSWORD)
        self.confirmPasswordTextCtrl.Disable()
        self.confirmPasswordTextCtrl.SetEditable(False)
        self.hBox1.Add(self.confirmPasswordStaticText, 1, wx.LEFT, 8)
        self.hBox2.Add(self.confirmPasswordTextCtrl, 1, wx.LEFT, 8)

        self.btnChangePassword = wx.Button(self.panelUser, label="Redefinir Senha", pos=(350, 160))
        self.btnChangePassword.Disable()

        wx.StaticBox(self.panelUser, -1, '', pos=(5, 5), size=(600, 200))

#-------------BINDS------------------------------------------------------------------------

        self.Bind(wx.EVT_MENU, self.getFirst, id=ID_TOOLBAR_USER_FIRST)
        self.Bind(wx.EVT_MENU, self.getLast, id=ID_TOOLBAR_USER_LAST)
        self.Bind(wx.EVT_MENU, self.getNext, id=ID_TOOLBAR_USER_NEXT)
        self.Bind(wx.EVT_MENU, self.getPrevious, id=ID_TOOLBAR_USER_PREVIOUS)
        self.Bind(wx.EVT_MENU, self.new, id=ID_TOOLBAR_USER_NEW)
        self.Bind(wx.EVT_MENU, self.save, id=ID_TOOLBAR_USER_SAVE)
        self.Bind(wx.EVT_MENU, self.cancel, id=ID_TOOLBAR_USER_CANCEL)
        self.Bind(wx.EVT_MENU, self.edit, id=ID_TOOLBAR_USER_EDIT)
        self.Bind(wx.EVT_MENU, self.remove, id=ID_TOOLBAR_USER_REMOVE)
        self.Bind(wx.EVT_MENU, self.find, id=ID_TOOLBAR_USER_FIND)
        self.btnChangePassword.Bind(wx.EVT_BUTTON, self.enablePasswordField)
        self.Bind(wx.EVT_CLOSE, self.quit)
#-------------END BINDS--------------------------------------------------------------------

        self.MakeModal(True)
        self.Show()

        self.getFirst(None)

    def getFirst(self, event):

        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

        self.currentIndex = 0

        user1 = User.query.order_by('name').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(user1.id))
        self.nameTextCtrl.SetValue(unicode(user1.name))
        self.loginTextCtrl.SetValue(unicode(user1.login))
        if user1.level == 0:
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)

    def getLast(self, event):

        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

        self.currentIndex = self.totalIndex

        user1 = User.query.order_by('name').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(user1.id))
        self.nameTextCtrl.SetValue(unicode(user1.name))
        self.loginTextCtrl.SetValue(unicode(user1.login))
        if user1.level == 0:
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)

    def getNext(self, event):

        if self.totalIndex == self.currentIndex:
            self.currentIndex = 0
        else:
            self.currentIndex = self.currentIndex+1

        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

        user1 = User.query.order_by('name').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(user1.id))
        self.nameTextCtrl.SetValue(unicode(user1.name))
        self.loginTextCtrl.SetValue(unicode(user1.login))
        if user1.level == 0:
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)

    def getPrevious(self, event):
        if self.currentIndex == 0:
            self.currentIndex = self.totalIndex
        else:
            self.currentIndex = self.currentIndex-1

        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

        user1 = User.query.order_by('name').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(user1.id))
        self.nameTextCtrl.SetValue(unicode(user1.name))
        self.loginTextCtrl.SetValue(unicode(user1.login))
        if user1.level == 0:
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)

    def new(self, event):

        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEW, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, True)

        self.idTextCtrl.SetValue('')
        self.idTextCtrl.SetEditable(True)
        self.nameTextCtrl.SetValue('')
        self.nameTextCtrl.SetEditable(True)
        self.loginTextCtrl.SetValue('')
        self.loginTextCtrl.SetEditable(True)
        self.cb.SetValue(False)
        self.cb.Enable()
        self.passwordTextCtrl.SetValue('')
        self.passwordTextCtrl.Enable()
        self.passwordTextCtrl.SetEditable(True)
        self.confirmPasswordTextCtrl.SetEditable(True)
        self.confirmPasswordTextCtrl.SetValue('')
        self.confirmPasswordTextCtrl.Enable()

        self.nameTextCtrl.SetFocus()

    def save(self, event):
        if self.idTextCtrl.GetValue() != '':

            if self.valida(int(self.idTextCtrl.GetValue()), self.nameTextCtrl.GetValue(), self.loginTextCtrl.GetValue()):
                user1 = User.get_by(id=self.idTextCtrl.GetValue())
                user1.name = self.nameTextCtrl.GetValue().title()
                user1.login = self.loginTextCtrl.GetValue().lower()

                if self.passwordTextCtrl.IsEditable():

                    if self.validaPassword(self.passwordTextCtrl.GetValue(), self.confirmPasswordTextCtrl.GetValue()):
                        user1.password = unicode(hashlib.sha1(self.passwordTextCtrl.GetValue()).hexdigest())
                    else:
                        return 0
                if self.cb.GetValue():
                    user1.level = 0
                else:
                    user1.level = 1

                session.commit()
                self.refreshIndex(self.idTextCtrl.GetValue())
                self.message = wx.MessageDialog(None, u'Usuário alterado com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()

                self.idTextCtrl.SetEditable(False)
                self.nameTextCtrl.SetEditable(False)
                self.loginTextCtrl.SetEditable(False)
                self.cb.Disable()
                self.passwordTextCtrl.SetValue('')
                self.passwordTextCtrl.SetEditable(False)
                self.passwordTextCtrl.Disable()
                self.confirmPasswordTextCtrl.SetValue('')
                self.confirmPasswordTextCtrl.SetEditable(False)
                self.confirmPasswordTextCtrl.Disable()

                self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_NEW, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

        else:

            if self.valida(self.idTextCtrl.GetValue(), self.nameTextCtrl.GetValue(), self.loginTextCtrl.GetValue()) and self.validaPassword(self.passwordTextCtrl.GetValue(), self.confirmPasswordTextCtrl.GetValue()):
                if self.cb.GetValue():
                    level = 0
                else:
                    level = 1

                user1 = User(name=self.nameTextCtrl.GetValue().title(), login=self.loginTextCtrl.GetValue().lower(), level=level, password=unicode(hashlib.sha1(self.passwordTextCtrl.GetValue()).hexdigest()))
                session.commit()

                self.refreshIndex(user1.id)
                self.idTextCtrl.SetValue(unicode(user1.id))
                self.message = wx.MessageDialog(None, u'Usuário cadastrado com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()

                self.idTextCtrl.SetEditable(False)
                self.nameTextCtrl.SetEditable(False)
                self.loginTextCtrl.SetEditable(False)
                self.cb.Disable()
                self.passwordTextCtrl.SetValue('')
                self.passwordTextCtrl.Disable()
                self.passwordTextCtrl.SetEditable(False)
                self.confirmPasswordTextCtrl.SetValue('')
                self.confirmPasswordTextCtrl.Disable()
                self.confirmPasswordTextCtrl.SetEditable(False)

                self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_NEW, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
                self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

    def valida(self, id, name, login):
        if name == '':
            self.message = wx.MessageDialog(None, u'O campo nome deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        user1 = User.query.filter(User.name.like(name)).first()
        if user1 != None:
            if (user1.name.upper() == name.upper()) and (user1.id == id):
                return 1
            else:
                self.message = wx.MessageDialog(None, u'Já existe um usuário cadastrado com este nome!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0

        if login == '':
            self.message = wx.MessageDialog(None, u'O campo login deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        user1 = User.query.filter(User.login.like(login)).first()
        if user1 != None:
            if (user1.login.upper() == login.upper()) and (user1.id == id):
                return 1
            else:
                self.message = wx.MessageDialog(None, u'Já existe um usuário cadastrado com este login!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0

        return 1

    def validaPassword(self, password, confirmPassword):
        if len(password) < 6:
            self.message = wx.MessageDialog(None, u'A senha deve ter no mínimo 6 caracteres!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if password != confirmPassword:
            self.message = wx.MessageDialog(None, u'O campo Senha e Confirma Senha devem ser iguais!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        return 1

    def refreshIndex(self, id):
        users = User.query.order_by('name').all()
        if id != None:
            for index, user in enumerate(users):
                if user.id == id:
                    self.currentIndex = index
                    self.totalIndex = len(users)-1
                    break
        else:
            self.currentIndex = self.currentIndex-1
            self.totalIndex = len(users)-1

    def cancel(self, event):
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEW, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, False)

        self.idTextCtrl.SetEditable(False)
        self.nameTextCtrl.SetEditable(False)
        self.loginTextCtrl.SetEditable(False)
        self.cb.Disable()
        self.passwordTextCtrl.SetEditable(False)
        self.passwordTextCtrl.SetValue('')
        self.passwordTextCtrl.Disable()
        self.confirmPasswordTextCtrl.SetEditable(False)
        self.confirmPasswordTextCtrl.SetValue('')
        self.confirmPasswordTextCtrl.Disable()
        self.btnChangePassword.Disable()

        self.getFirst(None)

    def edit(self, event):

        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIRST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_LAST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_PREVIOUS, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEXT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_NEW, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_SAVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_REMOVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_EDIT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_FIND, False)
        self.toolBar.EnableTool(ID_TOOLBAR_USER_CANCEL, True)

        self.idTextCtrl.SetEditable(True)
        self.nameTextCtrl.SetEditable(True)
        self.loginTextCtrl.SetEditable(True)
        self.cb.Enable()
        self.btnChangePassword.Enable()

    def enablePasswordField(self, event):
        self.passwordTextCtrl.Enable()
        self.passwordTextCtrl.SetEditable(True)
        self.confirmPasswordTextCtrl.SetEditable(True)
        self.confirmPasswordTextCtrl.Enable()

    def remove(self, event):
        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir o usuário?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            user1 = User.get_by(id=int(self.idTextCtrl.GetValue()))
            user1.delete()
            session.commit()
            remove_dial.Destroy()
            self.refreshIndex(None)
            self.getNext(None)

        else:
            event.Veto()

    def find(self, event):

        import sys
        self.findDialog = wx.Dialog(parent=None, id=wx.ID_ANY, pos=(10, 30), size=(430, 700), title=u'Localizar Usuário')
        self.findDialog.Centre(wx.BOTH)

        self.vUserBox1 = wx.BoxSizer(wx.VERTICAL)

        self.hUserBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.listUser = wx.ListCtrl(self.findDialog, -1, size=(430, 280), style=wx.LC_REPORT)
        self.listUser.InsertColumn(0, 'Nome', width=150)
        self.listUser.InsertColumn(1, 'Login', width=200)
        self.listUser.InsertColumn(2, 'Administrador', width=75)
        self.listUser.InsertColumn(3, '', width=0)

        self.hUserBox1.Add(self.listUser, 1, wx.EXPAND)
        self.vUserBox1.Add(self.hUserBox1, 0, wx.ALL | wx.EXPAND, 5)
        self.vUserBox1.Add((-1, 10))

        users = User.query.order_by('name').all()

        for user in users:
            index = self.listUser.InsertStringItem(sys.maxint, user.name)
            self.listUser.SetStringItem(index, 1, user.login)
            if user.level == 0:
                self.listUser.SetStringItem(index, 2, "Sim")
            else:
                self.listUser.SetStringItem(index, 2, "Não")
            self.listUser.SetStringItem(index, 3, str(user.id))

        self.listUser.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.getSelectedItem, id=-1)

        self.hUserBox2 = wx.BoxSizer(wx.HORIZONTAL)
        findOptions = ["Nome"]
        self.findRadioBox = wx.RadioBox(self.findDialog, -1, "Localizar por:", (10, 300), wx.DefaultSize, findOptions, 2, wx.RA_SPECIFY_COLS)
        self.hUserBox2.Add(self.findRadioBox, 0, wx.RIGHT, 8)
        self.vUserBox1.Add(self.hUserBox2, 0, wx.ALL | wx.EXPAND, 5)

        self.hUserBox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.findTextCtrl = wx.TextCtrl(self.findDialog, -1, pos=(-1, -1), size=(140, -1))

        self.searchBtn = wx.BitmapButton(self.findDialog, ID_FIND_SEARCH, wx.Bitmap('./imagens/search.png'))

        self.hUserBox3.Add(self.findTextCtrl, 1, wx.LEFT, 0)
        self.hUserBox3.Add(self.searchBtn, 0, 5)
        self.vUserBox1.Add(self.hUserBox3, 0, wx.ALL | wx.EXPAND, 5)

        self.findDialog.Bind(wx.EVT_BUTTON, self.search, self.searchBtn)
        self.findDialog.SetSizerAndFit(self.vUserBox1)

        self.findDialog.ShowModal()
        self.findDialog.SetFocus()
        self.findDialog.Destroy()

    def getSelectedItem(self, event):
        id = self.listUser.GetItem(event.GetIndex(), 3).GetText()
        userSelected = User.query.filter_by(id=id).first()

        self.idTextCtrl.SetValue(unicode(userSelected.id))
        self.nameTextCtrl.SetValue(unicode(userSelected.name))
        self.loginTextCtrl.SetValue(unicode(userSelected.login))
        if userSelected.level == 0:
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)

        self.refreshIndex(userSelected.id)
        self.findDialog.Destroy()

    def search(self, event):
        import sys
        self.findTextCtrl.SetFocus()
        self.findTextCtrl.SelectAll()
        self.listUser.DeleteAllItems()
        self.finderUser = self.findTextCtrl.GetValue().strip()

        searchFor = self.findRadioBox.GetStringSelection()
        users = User.query.order_by('name').all()

        if self.finderUser == '':
            for user in users:
                index = self.listUser.InsertStringItem(sys.maxint, user.name)
                self.listUser.SetStringItem(index, 1, user.login)
                if user.level == 0:
                    self.listUser.SetStringItem(index, 2, "Sim")
                else:
                    self.listUser.SetStringItem(index, 2, "Não")
                self.listUser.SetStringItem(index, 3, str(user.id))
        else:
            for user in users:
                if user.name.upper().find(self.finderUser.upper(), 0, len(self.finderUser)) != -1:
                    index = self.listUser.InsertStringItem(sys.maxint, user.name)
                    self.listUser.SetStringItem(index, 1, user.login)
                    if user.level == 0:
                        self.listUser.SetStringItem(index, 2, "Sim")
                    else:
                        self.listUser.SetStringItem(index, 2, "Não")
                    self.listUser.SetStringItem(index, 3, str(user.id))

    def quit(self, event):
        self.MakeModal(False)
        self.Destroy()
