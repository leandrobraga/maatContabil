# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_MOVCONINICIAL_NOVO = 5001
ID_TOOLBAR_MOVCONINICIAL_EDITAR = 5002
ID_TOOLBAR_MOVCONINICIAL_EXCLUIR = 5003
ID_TOOLBAR_MOVCONINICIAL_CRIAR_ARQUIVO = 504
ID_TOOLBAR_MOVCONINICIAL_IMPORTAR = 505

SHEET_NAME = 'MXM'

class WindowMovConFinal(wx.MiniFrame):
    


    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Movimentação Contábil Final", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.panelMovConInicial = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_MOVCONINICIAL_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo Movimento Contábil Final')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_MOVCONINICIAL_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Movimento Contábil Final selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_MOVCONINICIAL_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Movimento Contábil Final selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_MOVCONINICIAL_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de Movimento Contábil Final')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_MOVCONINICIAL_IMPORTAR, "Importar", wx.Bitmap("./imagens/import.png"), shortHelp=u'Importa Plano de Contas')
        self.toolBar.AddSeparator()
        
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        planoContas = PlanoConta.query.all()
        
        self.codigosConta = []
        
        for planoConta in planoContas:
            self.codigosConta.append(planoConta.conta)
            

        self.cbCompetenciaForView = wx.ComboBox(self.panelMovConInicial, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.movConIniListCtrl = wx.ListCtrl(self.panelMovConInicial, wx.ID_ANY, pos=(0, 30), size=(525, 230), style=wx.LC_REPORT)
        self.movConIniListCtrl.InsertColumn(0, u'Conta', width=120)
        self.movConIniListCtrl.InsertColumn(1, u'Débito', width=200)
        self.movConIniListCtrl.InsertColumn(2, u'Crédito', width=200)
        self.movConIniListCtrl.InsertColumn(3, u'', width=0)
        self.movConIniListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.movConIniListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None
        #self.insereInCtrList(None)

        self.hbox1.Add(self.movConIniListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoMovConIni, id=ID_TOOLBAR_MOVCONINICIAL_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaMovConIni(event, self.idSelecionado), id=ID_TOOLBAR_MOVCONINICIAL_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiMovConIni(event, self.idSelecionado), id=ID_TOOLBAR_MOVCONINICIAL_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_MOVCONINICIAL_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_MENU, self.importaMovConFinal, id=ID_TOOLBAR_MOVCONINICIAL_IMPORTAR)

        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, importar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_MOVCONINICIAL_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_MOVCONINICIAL_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_MOVCONINICIAL_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_MOVCONINICIAL_CRIAR_ARQUIVO, importar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.movConIniListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def insereInCtrList(self, event):

        self.movConIniListCtrl.DeleteAllItems()

        movimentos = MovConFinal.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

        for movimento in movimentos:

            index = self.movConIniListCtrl.InsertStringItem(sys.maxint, unicode(movimento.codigoConta))
            self.movConIniListCtrl.SetStringItem(index, 1, unicode(movimento.debito))
            self.movConIniListCtrl.SetStringItem(index, 2, unicode(movimento.credito))
            self.movConIniListCtrl.SetStringItem(index, 3, unicode(movimento.id))
    
    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127 or event.GetKeyCode() == 46:
                event.Skip()
        else:
            event.Skip()

    def novoMovConIni(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoMovConIni = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(300, 280), pos=(300, 170), title=u'Novo - Movimetação Contábil Final', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoMovConIni = wx.Panel(self.windowNovoMovConIni, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoMovConIni, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        wx.StaticBox(self.panelNovoMovConIni, -1, pos=(5, 45), size=(280, 130))

        self.stCompetencia = wx.StaticText(self.panelNovoMovConIni, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoMovConIni, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
                
        self.stCodigoConta = wx.StaticText(self.panelNovoMovConIni, -1, u'Código da Conta', pos=(10, 60))
        self.cbCodigoConta = wx.ComboBox(self.panelNovoMovConIni, -1, pos=(10, 80), size=(110, -1), choices=self.codigosConta, style=wx.CB_READONLY)
        
        self.stAnoConta = wx.StaticText(self.panelNovoMovConIni, -1, u'Ano de Criação da Conta', pos=(150, 60))
        self.tcAnoConta = wx.TextCtrl(self.panelNovoMovConIni, -1, pos=(150, 80), size=(122, -1), style=wx.ALIGN_LEFT)
        self.tcAnoConta.SetMaxLength(4)
        self.tcAnoConta.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stDebito = wx.StaticText(self.panelNovoMovConIni, -1, u'Débito Informado', pos=(10, 120), style=wx.ALIGN_LEFT)
        self.tcDebito = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoMovConIni, pos=wx.Point(10, 140), style=0, value=0)
        self.tcDebito.SetFractionWidth(2)
        self.tcDebito.SetGroupChar(u"#")
        self.tcDebito.SetDecimalChar(u",")
        self.tcDebito.SetGroupChar(u".")
        self.tcDebito.SetAllowNegative(False)

        self.stCredito = wx.StaticText(self.panelNovoMovConIni, -1, u'Crédito Informado', pos=(150, 120), style=wx.ALIGN_LEFT)
        self.tcCredito = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoMovConIni, pos=wx.Point(150, 140), style=0, value=0)
        self.tcCredito.SetFractionWidth(2)
        self.tcCredito.SetGroupChar(u"#")
        self.tcCredito.SetDecimalChar(u",")
        self.tcCredito.SetGroupChar(u".")
        self.tcCredito.SetAllowNegative(False)
        
        self.btnSalvar = wx.Button(self.panelNovoMovConIni, -1, u"Salvar", pos=(50, 200))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarMovConIni)
        self.btnCancelar = wx.Button(self.panelNovoMovConIni, -1, u"Cancelar", pos=(150, 200))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitMovConIni)      

        #Bind
        self.windowNovoMovConIni.Bind(wx.EVT_CLOSE, self.quitMovConIni)

        self.windowNovoMovConIni.Centre()
        self.windowNovoMovConIni.Show()

    def quitMovConIni(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoMovConIni.Destroy()

    def valida(self):

        if self.cbCompetencia.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Competência!', 'Info', wx.OK)
            self.cbCompetencia.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbCodigoConta.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Código da Conta!', 'Info', wx.OK)
            self.cbCodigoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcAnoConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Ano de Criação da Conta deve ser preenchido!', 'Info', wx.OK)
            self.tcAnoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if len(self.tcAnoConta.GetValue()) < 4:
            self.message = wx.MessageDialog(None, u'O campo Ano de Criação da Conta deve possuir 4 dígitos!', 'Info', wx.OK)
            self.tcAnoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcDebito.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Débito Informado deve ser preenchido!', 'Info', wx.OK)
            self.tcDebito.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCredito.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Crédito Informado deve ser preenchido!', 'Info', wx.OK)
            self.tcCredito.SetFocus()
            self.message.ShowModal()
            return 0

        return 1

    def salvarMovConIni(self, event):

        if self.valida():
            
            try:
                MovConFinal(

                    anoConta = unicode(self.tcAnoConta.GetValue()),
                    codigoConta = unicode(self.cbCodigoConta.GetValue()),
                    tipoMovimento = unicode(2),
                    debito = unicode(self.tcDebito.GetValue()),
                    credito = unicode(self.tcCredito.GetValue()),
                    competencia = unicode(self.cbCompetencia.GetValue()),                     

                    )
            
                session.commit()
                self.message = wx.MessageDialog(None, u'Movimentação Contábil Final salva com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoMovConIni.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoMovConIni.Close()


    def vizualizaMovConIni(self, event, idMovCon):

        if idMovCon is None:
            self.message = wx.MessageDialog(None, u'Nenhum Movimento Contábil foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.movConIni = MovConFinal.query.filter_by(id=idMovCon).first()

        self.windowEditaMovConIni = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(300, 280), pos=(300, 170), title=u'Editar - Movimetação Contábil Final', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoMovConIni = wx.Panel(self.windowEditaMovConIni, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoMovConIni, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.movConIni.id))

        wx.StaticBox(self.panelNovoMovConIni, -1, pos=(5, 45), size=(280, 130))

        self.stCompetencia = wx.StaticText(self.panelNovoMovConIni, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoMovConIni, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.movConIni.competencia)

        self.stCodigoConta = wx.StaticText(self.panelNovoMovConIni, -1, u'Código da Conta', pos=(10, 60))
        self.cbCodigoConta = wx.ComboBox(self.panelNovoMovConIni, -1, pos=(10, 80), size=(110, -1), choices=self.codigosConta, style=wx.CB_READONLY)
        self.cbCodigoConta.SetValue(self.movConIni.codigoConta)

        self.stAnoConta = wx.StaticText(self.panelNovoMovConIni, -1, u'Ano de Criação da Conta', pos=(150, 60))
        self.tcAnoConta = wx.TextCtrl(self.panelNovoMovConIni, -1, pos=(150, 80), size=(122, -1), style=wx.ALIGN_LEFT)
        self.tcAnoConta.SetMaxLength(4)
        self.tcAnoConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAnoConta.SetValue(self.movConIni.anoConta)

        self.stDebito = wx.StaticText(self.panelNovoMovConIni, -1, u'Débito Informado', pos=(10, 120), style=wx.ALIGN_LEFT)
        self.tcDebito = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoMovConIni, pos=wx.Point(10, 140), style=0, value=0)
        self.tcDebito.SetFractionWidth(2)
        self.tcDebito.SetGroupChar(u"#")
        self.tcDebito.SetDecimalChar(u",")
        self.tcDebito.SetGroupChar(u".")
        self.tcDebito.SetAllowNegative(False)
        self.tcDebito.SetValue(float(self.movConIni.debito))

        self.stCredito = wx.StaticText(self.panelNovoMovConIni, -1, u'Crédito Informado', pos=(150, 120), style=wx.ALIGN_LEFT)
        self.tcCredito = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoMovConIni, pos=wx.Point(150, 140), style=0, value=0)
        self.tcCredito.SetFractionWidth(2)
        self.tcCredito.SetGroupChar(u"#")
        self.tcCredito.SetDecimalChar(u",")
        self.tcCredito.SetGroupChar(u".")
        self.tcCredito.SetAllowNegative(False)
        self.tcCredito.SetValue(float(self.movConIni.credito))
        
        self.btnSalvar = wx.Button(self.panelNovoMovConIni, -1, u"Salvar", pos=(50, 200))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarMovConIni)
        self.btnCancelar = wx.Button(self.panelNovoMovConIni, -1, u"Cancelar", pos=(150, 200))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEditaMovConIni)
        
        #Bind
        self.windowEditaMovConIni.Bind(wx.EVT_CLOSE, self.quitEditaMovConIni)

        self.windowEditaMovConIni.Centre()
        self.windowEditaMovConIni.Show()

    def quitEditaMovConIni(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaMovConIni.Destroy()

    def editarMovConIni(self, event):
        
        if self.valida():

            self.movConIni.anoConta = unicode(self.tcAnoConta.GetValue())
            self.movConIni.codigoConta = unicode(self.cbCodigoConta.GetValue())
            self.movConIni.tipoMovimento = unicode(2)
            self.movConIni.debito = unicode(self.tcDebito.GetValue())
            self.movConIni.credito = unicode(self.tcCredito.GetValue())
            self.movConIni.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'O Movimento Contábil foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.movConIni = None
            self.windowEditaMovConIni.Close()

    def excluiMovConIni(self, event, idMovCon):

        if idMovCon is None:
            self.message = wx.MessageDialog(None, u'Nenhum Movimento Contábil foi selecionada! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        
        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este Movimento Contábil?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()

        if ret == wx.ID_YES:
            self.movConIni = MovConFinal.query.filter_by(id=idMovCon).first()
            self.movConIni.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Movimento Contábil excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()


    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Contas", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereContaPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.movConIniGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.movConIniGeraArquivoListCtrl.InsertColumn(0, u'Conta', width=130)
        self.movConIniGeraArquivoListCtrl.InsertColumn(1, u'Débito', width=120)
        self.movConIniGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.movConIniGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoGeraArquivos)

        self.btnGerarComTudo = wx.Button(self.panelGeraArquivo, -1, u">|", pos=(290, 150))
        self.btnGerarComTudo.Bind(wx.EVT_BUTTON, self.insereTudo)
        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.movConIniParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.movConIniParaArquivoListCtrl.InsertColumn(0, u'Conta', width=130)
        self.movConIniParaArquivoListCtrl.InsertColumn(1, u'Débito', width=120)
        self.movConIniParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.movConIniParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()


    def selecionaItensLicitacaoGeraArquivos(self, event):

        item = self.movConIniGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.movConIniGeraArquivoListCtrl.GetNextSelected(item)

    def insereContaPorCompetencia(self, event):

        movimentos = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            movimentos = MovConFinal.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            movimentos = MovConFinal.query.all()

        self.movConIniGeraArquivoListCtrl.DeleteAllItems()

        if not movimentos:
            self.message = wx.MessageDialog(None, u'Não existe Contas para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(movimentos) == self.movConIniParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for movimento in movimentos:
                    igual = False
                    if self.movConIniParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.movConIniGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(movimento.codigoConta))
                        self.movConIniGeraArquivoListCtrl.SetStringItem(index, 1, unicode(movimento.debito))
                        self.movConIniGeraArquivoListCtrl.SetStringItem(index, 2, unicode(movimento.id))
                        igual = True

                    else:

                        for x in range(self.movConIniParaArquivoListCtrl.GetItemCount()):

                            if movimento.codigoConta == unicode(self.movConIniParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.movConIniGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(movimento.codigoConta))
                        self.movConIniGeraArquivoListCtrl.SetStringItem(index, 1, unicode(movimento.nomeConta))
                        self.movConIniGeraArquivoListCtrl.SetStringItem(index, 2, unicode(movimento.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def insereTudo(self, event):
        
        self.movConIniGeraArquivoListCtrl.SetItemState(-1, wx.LIST_STATE_SELECTED , wx.LIST_STATE_SELECTED)
        item = self.movConIniGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.movConIniGeraArquivoListCtrl.GetNextSelected(item)

        self.insereGeraArquivo(None)


    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os Movimentos a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.movConIniParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.movConIniGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.movConIniParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.movConIniGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.movConIniParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.movConIniGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.movConIniGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []


    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os Movimentos Contábeis a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.movConIniGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.movConIniParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.movConIniGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.movConIniParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.movConIniGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.movConIniParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.movConIniParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []


    def selecionaItensLicitacaoParaArquivo(self, event):

        item = self.movConIniParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.movConIniParaArquivoListCtrl.GetNextSelected(item)

    def geraArquivoDialog(self, event):

        if self.movConIniParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Movimentos para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="MOVCONFINAL.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Movimentos Contábeis gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Movimento Contábil gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def geraArquivo(self):
        
        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.movConIniParaArquivoListCtrl.GetItemCount()):

            try:

                idConta = int(self.movConIniParaArquivoListCtrl.GetItem(x, 2).GetText())
                movConIni = MovConFinal.query.filter_by(id=idConta).first()

                f.write(unicode('000000'))
                f.write(unicode(movConIni.anoConta.zfill(4)))
                f.write(unicode(movConIni.codigoConta.replace("'", "").replace("\"", "").replace(".", "").ljust(34)))
                f.write(unicode(movConIni.tipoMovimento))
                movConIni.debito = float(movConIni.debito)
                movConIni.debito = unicode(movConIni.debito)
                partes = movConIni.debito.split('.')
                
                if len(partes[1])> 1:
                    f.write(unicode((movConIni.debito).zfill(16).replace(".", ",")))
                
                else:
                    f.write(unicode((movConIni.debito+'0').zfill(16).replace(".", ",")))

                movConIni.credito = float(movConIni.credito)
                movConIni.credito = unicode(movConIni.credito)
                partes = movConIni.credito.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((movConIni.credito).zfill(16).replace(".", ",")))
                
                else:
                    f.write(unicode((movConIni.credito+'0').zfill(16).replace(".", ",")))
                
                f.write(u'\n')
                    

            except:
                return 0

        return 1


    def importaMovConFinal(self,event):
        pathFile = self.onOpenFile()
        
        if pathFile !=None:
            notasInseridas = self.parserPlanilha(pathFile)
            message = u'Foram inseridos %s Movimentos Contábeis!' %(notasInseridas) 
            self.message = wx.MessageDialog(None, message, 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)


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

    def getMounthOnSheet(self, sheet):

        stringWithMounth = sheet.cell(1, 1).value

        for mounth in self.choicesCompetencias:

            if stringWithMounth.upper().startswith(mounth.upper()):

                return mounth

    def parserPlanilha(self, pathFile):
        from xlrd import open_workbook

        book = open_workbook(pathFile)
        for sheet_name in book.sheet_names():
            if sheet_name == SHEET_NAME:
                sheet = book.sheet_by_name(sheet_name)

        contasInseridas = 0

        year = sheet.cell(1, 1).value.split(" ")[2]

        dialog = wx.ProgressDialog(u"Importando Movimentos Contábeis", u"Aguarde enquanto a operação é concluída", sheet.nrows -6 , parent=self, style = wx.PD_CAN_ABORT | wx.PD_APP_MODAL )

        for row_index in range(4,sheet.nrows-6):
            contaExiste = MovConFinal.query.filter_by(competencia=unicode(self.getMounthOnSheet(sheet))).filter_by(codigoConta=sheet.cell(row_index,0).value).first()
            if contaExiste == None:

                if sheet.cell(row_index,0).value[0] == '1':
            
                    MovConFinal(anoConta=unicode(year),
                        codigoConta=unicode(sheet.cell(row_index,0).value),
                        tipoMovimento=unicode("3"),
                        debito=unicode(sheet.cell(row_index,5).value),
                        credito=unicode(0),
                        competencia=unicode(self.getMounthOnSheet(sheet))
                    )
                    session.commit()
                    contasInseridas +=1
                    dialog.Update(contasInseridas)

                elif sheet.cell(row_index,0).value[0] == '2':
            
                    MovConFinal(anoConta=unicode(year),
                        codigoConta=unicode(sheet.cell(row_index,0).value),
                        tipoMovimento=unicode("3"),
                        debito=unicode(0),
                        credito=unicode(sheet.cell(row_index,5).value),
                        competencia=unicode(self.getMounthOnSheet(sheet))
                    )
                    session.commit()
                    contasInseridas +=1
                    dialog.Update(contasInseridas)

                else:

                    MovConFinal(anoConta=unicode(year),
                        codigoConta=unicode(sheet.cell(row_index,0).value),
                        tipoMovimento=unicode("3"),
                        debito=unicode(0),
                        credito=unicode(0),
                        competencia=unicode(self.getMounthOnSheet(sheet))
                    )
                    session.commit()
                    contasInseridas +=1
                    dialog.Update(contasInseridas)
        
        
        dialog.Destroy()

        return contasInseridas    
