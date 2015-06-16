# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_PLANO_CONTA_NOVO = 5001
ID_TOOLBAR_PLANO_CONTA_EDITAR = 5002
ID_TOOLBAR_PLANO_CONTA_EXCLUIR = 5003
ID_TOOLBAR_PLANO_CONTA_IMPORTAR = 504

SHEET_NAME = 'MXM'

class WindowPlanoConta(wx.MiniFrame):
    


    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Plano de Contas", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.panelPlanoConta = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_PLANO_CONTA_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo Plano de Contas')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PLANO_CONTA_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Plano de Contas selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PLANO_CONTA_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Plano de Contas selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PLANO_CONTA_IMPORTAR, "Importar", wx.Bitmap("./imagens/import.png"), shortHelp=u'Importa Plano de Contas')
        self.toolBar.AddSeparator()
        
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.planoContaListCtrl = wx.ListCtrl(self.panelPlanoConta, wx.ID_ANY, pos=(0, 5), size=(525, 230), style=wx.LC_REPORT)
        self.planoContaListCtrl.InsertColumn(0, u'Conta', width=200)
        self.planoContaListCtrl.InsertColumn(1, u'Descrição', width=300)
        self.planoContaListCtrl.InsertColumn(2, u'', width=0)
        self.planoContaListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.planoContaListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None
        self.insereInCtrList(None)

        self.hbox1.Add(self.planoContaListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoPlanoConta, id=ID_TOOLBAR_PLANO_CONTA_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaPlanoConta(event, self.idSelecionado), id=ID_TOOLBAR_PLANO_CONTA_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiPlanoConta(event, self.idSelecionado), id=ID_TOOLBAR_PLANO_CONTA_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.importaPlanoConta, id=ID_TOOLBAR_PLANO_CONTA_IMPORTAR)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, importar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_PLANO_CONTA_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_PLANO_CONTA_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_PLANO_CONTA_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_PLANO_CONTA_IMPORTAR, importar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.planoContaListCtrl.GetItem(event.GetIndex(), 2).GetText()

    def insereInCtrList(self, event):

        self.planoContaListCtrl.DeleteAllItems()

        planoContas = PlanoConta.query.all()

        for planoConta in planoContas:

            index = self.planoContaListCtrl.InsertStringItem(sys.maxint, unicode(planoConta.conta))
            self.planoContaListCtrl.SetStringItem(index, 1, unicode(planoConta.descricao))
            self.planoContaListCtrl.SetStringItem(index, 2, unicode(planoConta.id))
            

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127 or event.GetKeyCode() == 46:
                event.Skip()
        else:
            event.Skip()

    def novoPlanoConta(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoPlanoConta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(440, 200), pos=(300, 170), title=u'Novo - Plano de Contas', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoPanelConta = wx.Panel(self.windowNovoPlanoConta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoPanelConta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        wx.StaticBox(self.panelNovoPanelConta, -1, pos=(5, 5), size=(420, 120))

        self.stConta = wx.StaticText(self.panelNovoPanelConta, -1, u'Conta', pos=(10, 15))
        self.tcConta = wx.TextCtrl(self.panelNovoPanelConta, -1, pos=(10, 35), size=(160, -1), style=wx.ALIGN_LEFT)
        self.tcConta.SetMaxLength(34)
        self.tcConta.Bind(wx.EVT_CHAR, self.escapaChar)


        self.stDescricao = wx.StaticText(self.panelNovoPanelConta, -1, u'Descrição', pos=(10, 70))
        self.tcDescricao = wx.TextCtrl(self.panelNovoPanelConta, -1, pos=(10, 90), size=(300, -1), style=wx.ALIGN_LEFT)
        self.tcDescricao.SetMaxLength(50)
        
        self.btnSalvar = wx.Button(self.panelNovoPanelConta, -1, u"Salvar", pos=(130, 140))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarPlanoConta)
        self.btnCancelar = wx.Button(self.panelNovoPanelConta, -1, u"Cancelar", pos=(230, 140))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoLicitacaoAta)      

        #Bind
        self.windowNovoPlanoConta.Bind(wx.EVT_CLOSE, self.quitNovoLicitacaoAta)

        self.windowNovoPlanoConta.Centre()
        self.windowNovoPlanoConta.Show()

    def quitNovoLicitacaoAta(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoPlanoConta.Destroy()

    def vizualizaPlanoConta(self,event,idPlanoConta):
        
        if idPlanoConta is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Conta foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.planoConta = PlanoConta.query.filter_by(id=idPlanoConta).first()

        self.windowEditaPlanoConta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(440, 200), pos=(300, 170), title=u'Editar - Plano de Conta', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoPanelConta = wx.Panel(self.windowEditaPlanoConta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoPanelConta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.planoConta.id))

        wx.StaticBox(self.panelNovoPanelConta, -1, pos=(5, 50), size=(420, 120))

        self.stConta = wx.StaticText(self.panelNovoPanelConta, -1, u'Conta', pos=(10, 15))
        self.tcConta = wx.TextCtrl(self.panelNovoPanelConta, -1, pos=(10, 35), size=(160, -1), style=wx.ALIGN_LEFT)
        self.tcConta.SetMaxLength(34)
        self.tcConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcConta.SetValue(self.planoConta.conta)

        self.stDescricao = wx.StaticText(self.panelNovoPanelConta, -1, u'Descrição', pos=(10, 70))
        self.tcDescricao = wx.TextCtrl(self.panelNovoPanelConta, -1, pos=(10, 90), size=(300, -1), style=wx.ALIGN_LEFT)
        self.tcDescricao.SetMaxLength(50)
        self.tcDescricao.SetValue(self.planoConta.descricao)
        
        self.btnSalvar = wx.Button(self.panelNovoPanelConta, -1, u"Salvar", pos=(130, 140))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarPlanoConta)
        self.btnCancelar = wx.Button(self.panelNovoPanelConta, -1, u"Cancelar", pos=(230, 140))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitPlanoContaEdita)      

        #Bind
        #self.windowEditaPlanoConta.Bind(wx.EVT_CLOSE, self.quitLicitacaoAtaEdita)

        self.windowEditaPlanoConta.Centre()
        self.windowEditaPlanoConta.Show()

    def quitPlanoContaEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaPlanoConta.Destroy()

    def valida(self):

        if self.tcConta.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo conta deve ser preenchido', 'Info', wx.OK)
            self.tcConta.SetFocus()
            self.message.ShowModal()
            return 0
        else:
            
            planoConta1 = PlanoConta.query.filter(PlanoConta.conta.like(self.tcConta.GetValue())).first()
            
            if planoConta1 != None:
                
                if (planoConta1.conta.upper() == self.tcConta.GetValue().upper()) and (int(self.tcId.GetValue()) != int(planoConta1.id)):
                
                    self.message = wx.MessageDialog(None, u'Já existe uma conta com esta numeração!', 'Info', wx.OK)
                    self.tcConta.SetFocus()
                    self.message.ShowModal()
                    return 0

        if self.tcDescricao.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Descrição deve ser preenchido!', 'Info', wx.OK)
            self.tcDescricao.SetFocus()
            self.message.ShowModal()
            return 0
        
        else:
            planoConta1 = PlanoConta.query.filter(PlanoConta.descricao.like(self.tcDescricao.GetValue())).first()

            if planoConta1 != None:
            
                if (planoConta1.descricao.upper() == self.tcDescricao.GetValue().upper()) and (int(self.tcId.GetValue()) != int(planoConta1.id)):
                
                    self.message = wx.MessageDialog(None, u'Já existe uma conta com esta descrição!', 'Info', wx.OK)
                    self.tcDescricao.SetFocus()
                    self.message.ShowModal()
                    return 0
        return 1

    def salvarPlanoConta(self, event):

        if self.valida():

            try:
                PlanoConta(conta=unicode(self.tcConta.GetValue()),
                        descricao=unicode(self.tcDescricao.GetValue()),
                        )

                session.commit()
                self.message = wx.MessageDialog(None, u'Conta salva com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoPlanoConta.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoPlanoConta.Close()

    def editarPlanoConta(self, event):

        if self.valida():

            self.planoConta.conta = unicode(self.tcConta.GetValue())
            self.planoConta.descricao = unicode(self.tcDescricao.GetValue())
            
            session.commit()
            self.message = wx.MessageDialog(None, u'A conta foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.toolBarControler(True, True, True, True)
            self.insereInCtrList(None)
            self.planoConta = None
            self.windowEditaPlanoConta.Close()

    def excluiPlanoConta(self, event, idPlanoConta):

        if idPlanoConta is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Conta foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        
        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Conta?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.planoConta = PlanoConta.query.filter_by(id=idPlanoConta).first()
            self.planoConta.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Conta excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def importaPlanoConta(self,event):
        pathFile = self.onOpenFile()
        
        if pathFile !=None:
            notasInseridas = self.parserPlanilha(pathFile)
            message = u'Foram inseridas %s contas !' %(notasInseridas) 
            self.message = wx.MessageDialog(None, message, 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)

    def parserPlanilha(self,pathFile):
        from xlrd import open_workbook
        
        book = open_workbook(pathFile)
        for sheet_name in book.sheet_names():
            if sheet_name == SHEET_NAME:
                sheet = book.sheet_by_name(sheet_name)
        
        contasInseridas = 0

        dialog = wx.ProgressDialog(u"Importando Planos de Conta", u"Aguarde enquanto a operação é concluída", sheet.nrows -6 , parent=self, style = wx.PD_CAN_ABORT | wx.PD_APP_MODAL )
        
        for row_index in range(7,sheet.nrows):

            # print sheet.cell(row_index,1).value

            contaExiste = PlanoConta.query.filter(PlanoConta.conta.like(sheet.cell(row_index,2).value)).first()
            
            if contaExiste == None:
                
                PlanoConta(conta=unicode(sheet.cell(row_index,2).value),
                    descricao=unicode(sheet.cell(row_index,3).value),
                )
                session.commit()
                contasInseridas +=1
                dialog.Update(contasInseridas)
        dialog.Destroy()
        return contasInseridas    

    def onOpenFile(self):
        """
        Create and show the Open FileDialog

        """
        from os.path import expanduser
        homeDirectory = expanduser("~")
        wildcard = "Microsoft Excel (*.xls, *.xlsx)|*.xls;*.xlsx" 
 
        dlg = wx.FileDialog(
            self, message="Selecione um arquivo",
            defaultDir=homeDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if len(paths) == 1:
                
                return paths[0]
            else:
                self.message = wx.MessageDialog(None, u'Selecione somente um arquivo!', 'Info', wx.OK)
                self.message.ShowModal()
                

        dlg.Destroy()