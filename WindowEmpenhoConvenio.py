# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_EMPENHO_CONVENIO_NOVO = 5001
ID_TOOLBAR_EMPENHO_CONVENIO_EDITAR = 5002
ID_TOOLBAR_EMPENHO_CONVENIO_EXCLUIR = 5003
ID_TOOLBAR_EMPENHO_CONVENIO_CRIAR_ARQUIVO = 5004


class WindowEmpenhoConvenio(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Informações de Empenho Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEmpenhoConvenio = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_CONVENIO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo empenho')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_CONVENIO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita empenho selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_CONVENIO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui empenho selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_CONVENIO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de empenho')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelEmpenhoConvenio, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.empenhoListCtrl = wx.ListCtrl(self.panelEmpenhoConvenio, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.empenhoListCtrl.InsertColumn(0, u'Número Convênio', width=150)
        self.empenhoListCtrl.InsertColumn(1, u'Nota Empenho', width=200)
        self.empenhoListCtrl.InsertColumn(2, u'Unidade Orçamentária', width=170)
        self.empenhoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.empenhoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.empenhoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoEmpenho, id=ID_TOOLBAR_EMPENHO_CONVENIO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaEmpenho(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHO_CONVENIO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiEmpenho(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHO_CONVENIO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_EMPENHO_CONVENIO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.empenhoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_CONVENIO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_CONVENIO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_CONVENIO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_CONVENIO_CRIAR_ARQUIVO, gerar)

    def insereInCtrList(self, event):

        self.empenhoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            empenhos = ConvenioEmpenho.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for empenho in empenhos:

                index = self.empenhoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.numeroConvenio))
                self.empenhoListCtrl.SetStringItem(index, 1, empenho.notaEmpenho)
                self.empenhoListCtrl.SetStringItem(index, 2, empenho.unidadeOrcamentaria)
                self.empenhoListCtrl.SetStringItem(index, 3, unicode(empenho.id))

    def novoEmpenho(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoEmpenho = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 270), pos=(300, 170), title=u'Novo - Empenho Contrato', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoEmpenho = wx.Panel(self.windowNovoEmpenho, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoEmpenho, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoEmpenho, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoEmpenho, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroConvenio)

        wx.StaticBox(self.panelNovoEmpenho, -1, pos=(5, 50), size=(480, 140))

        self.stNumeroConvenio = wx.StaticText(self.panelNovoEmpenho, -1, u'Número Convênio', pos=(10, 70))
        self.cbNumeroConvenio = wx.ComboBox(self.panelNovoEmpenho, -1, pos=(10, 90), size=(150, -1), choices=[], style=wx.CB_READONLY)

        self.stNotaEmpenho = wx.StaticText(self.panelNovoEmpenho, -1, u'Nota de Empenho', pos=(10, 130))
        self.tcNotaEmpenho = wx.TextCtrl(self.panelNovoEmpenho, -1, pos=(10, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcNotaEmpenho.SetMaxLength(10)

        self.stAnoEmpenho = wx.StaticText(self.panelNovoEmpenho, -1, u'Ano Empenho', pos=(190, 130))
        self.tcAnoEmpenho = wx.TextCtrl(self.panelNovoEmpenho, -1, pos=(190, 150), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcAnoEmpenho.SetMaxLength(4)
        self.tcAnoEmpenho.Bind(wx.EVT_CHAR, self.escapaChar)
        
        self.stUnidadeOrcamentaria = wx.StaticText(self.panelNovoEmpenho, -1, u'Unidade Orçamentaria', pos=(340, 130))
        self.tcUnidadeOrcamentaria = wx.TextCtrl(self.panelNovoEmpenho, -1, pos=(340, 150), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcUnidadeOrcamentaria.SetMaxLength(6)

        self.btnSalvar = wx.Button(self.panelNovoEmpenho, -1, u"Salvar", pos=(150, 210))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarEmpenho)
        self.btnCancelar = wx.Button(self.panelNovoEmpenho, -1, u"Cancelar", pos=(250, 210))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoEmpenho)


        #Bind
        self.windowNovoEmpenho.Bind(wx.EVT_CLOSE, self.quitNovoEmpenho)

        self.windowNovoEmpenho.Centre()
        self.windowNovoEmpenho.Show()

    def quitNovoEmpenho(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoEmpenho.Destroy()

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()


    def insereNumeroConvenio(self, event):

        self.cbNumeroConvenio.Clear()

        convenios = Convenio.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()

        if not convenios:
            self.message = wx.MessageDialog(None, u'Não existe convênios para a competência selecionada!', 'Info', wx.OK)
            self.message.ShowModal()
            self.cbNumeroConvenio.Disable()

        else:
            for convenio in convenios:

                self.cbNumeroConvenio.Append(unicode(convenio.numeroConvenio))

            self.cbNumeroConvenio.Enable()

    
    def valida(self):

        if self.cbCompetencia.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Competência', 'Info', wx.OK)
            self.cbCompetencia.SetFocus()
            self.message.ShowModal()
            return 0


        if self.cbNumeroConvenio.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Número Convênio', 'Info', wx.OK)
            self.cbNumeroConvenio.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNotaEmpenho.GetValue() == u'':

            self.message = wx.MessageDialog(None, u'O campo Nota de Empenho deve ser preenchido', 'Info', wx.OK)
            self.tcNotaEmpenho.SetFocus()
            self.message.ShowModal()
            return 0

        
        if self.tcAnoEmpenho.GetValue() == u'':

            self.message = wx.MessageDialog(None, u'O campo Ano Empenho deve ser preenchido', 'Info', wx.OK)
            self.tcAnoEmpenho.SetFocus()
            self.message.ShowModal()
            return 0

        if len(self.tcAnoEmpenho.GetValue()) < 4:

            self.message = wx.MessageDialog(None, u'O campo Ano Empenho deve ser preenchido com 4 dígitos', 'Info', wx.OK)
            self.tcAnoEmpenho.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcUnidadeOrcamentaria.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Unidade Orçamentaria deve ser preenchido', 'Info', wx.OK)
            self.tcUnidadeOrcamentaria.SetFocus()
            self.message.ShowModal()
            return 0

        empenhos = ConvenioEmpenho.query.filter_by(numeroConvenio=self.cbNumeroConvenio.GetValue()).all()

        if empenhos:
            for empenho in empenhos:

                if empenho.numeroConvenio == self.cbNumeroConvenio.GetValue() and empenho.id != self.tcId.GetValue() and empenho.anoEmpenho == self.tcAnoEmpenho.GetValue() and empenho.notaEmpenho == self.tcNotaEmpenho.GetValue() and empenho.unidadeOrcamentaria == self.tcUnidadeOrcamentaria.GetValue():
                    self.message = wx.MessageDialog(None, u'Este empenho já está cadastrado!', 'Info', wx.OK)
                    self.tcNotaEmpenho.SetFocus()
                    self.message.ShowModal()
                    return 0

        return 1 

    def salvarEmpenho(self, event):
        
        if self.valida():
            
            ConvenioEmpenho(
                numeroConvenio = unicode(self.cbNumeroConvenio.GetValue()),
                notaEmpenho = unicode(self.tcNotaEmpenho.GetValue()),
                anoEmpenho = unicode(self.tcAnoEmpenho.GetValue()),
                unidadeOrcamentaria = unicode(self.tcUnidadeOrcamentaria.GetValue()),
                competencia = unicode(self.cbCompetencia.GetValue())
            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Empenho salvo com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitNovoEmpenho(None) 

    def vizualizaEmpenho(self, event, idEmpenho):

        if idEmpenho is None:
            self.message = wx.MessageDialog(None, u'Nenhum empenho foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.empenho = ConvenioEmpenho.query.filter_by(id=idEmpenho).first()

        self.toolBarControler(False, False, False, False)

        self.windowVizualizaEmpenho = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 270), pos=(300, 170), title=u'Editar - Empenho Convênio', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelVizualizaEmpenho = wx.Panel(self.windowVizualizaEmpenho, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelVizualizaEmpenho, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.empenho.id))

        self.stCompetencia = wx.StaticText(self.panelVizualizaEmpenho, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelVizualizaEmpenho, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroConvenio)
        self.cbCompetencia.SetValue(self.empenho.competencia)

        wx.StaticBox(self.panelVizualizaEmpenho, -1, pos=(5, 50), size=(480, 140))

        self.stNumeroconvenio = wx.StaticText(self.panelVizualizaEmpenho, -1, u'Número Convênio', pos=(10, 70))
        self.cbNumeroConvenio = wx.ComboBox(self.panelVizualizaEmpenho, -1, pos=(10, 90), size=(150, -1), choices=[], style=wx.CB_READONLY)
        self.insereNumeroConvenio(None)
        self.cbNumeroConvenio.SetValue(self.empenho.numeroConvenio)

        self.stNotaEmpenho = wx.StaticText(self.panelVizualizaEmpenho, -1, u'Nota de Empenho', pos=(10, 130))
        self.tcNotaEmpenho = wx.TextCtrl(self.panelVizualizaEmpenho, -1, pos=(10, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcNotaEmpenho.SetMaxLength(10)
        self.tcNotaEmpenho.SetValue(self.empenho.notaEmpenho)

        self.stAnoEmpenho = wx.StaticText(self.panelVizualizaEmpenho, -1, u'Ano Empenho', pos=(190, 130))
        self.tcAnoEmpenho = wx.TextCtrl(self.panelVizualizaEmpenho, -1, pos=(190, 150), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcAnoEmpenho.SetMaxLength(4)
        self.tcAnoEmpenho.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAnoEmpenho.SetValue(self.empenho.anoEmpenho)
        
        self.stUnidadeOrcamentaria = wx.StaticText(self.panelVizualizaEmpenho, -1, u'Unidade Orçamentaria', pos=(340, 130))
        self.tcUnidadeOrcamentaria = wx.TextCtrl(self.panelVizualizaEmpenho, -1, pos=(340, 150), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcUnidadeOrcamentaria.SetMaxLength(6)
        self.tcUnidadeOrcamentaria.SetValue(self.empenho.unidadeOrcamentaria)

        self.btnSalvar = wx.Button(self.panelVizualizaEmpenho, -1, u"Alterar", pos=(150, 210))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarEmpenho)
        self.btnCancelar = wx.Button(self.panelVizualizaEmpenho, -1, u"Cancelar", pos=(250, 210))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaEmpenho)


        #Bind
        self.windowVizualizaEmpenho.Bind(wx.EVT_CLOSE, self.quitNovoEmpenho)

        self.windowVizualizaEmpenho.Centre()
        self.windowVizualizaEmpenho.Show()


    def quitVizualizaEmpenho(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowVizualizaEmpenho.Destroy()

    def editarEmpenho(self, event):

        if self.valida():
            
            self.empenho.numeroConvenio = unicode(self.cbNumeroConvenio.GetValue())
            self.empenho.notaEmpenho = unicode(self.tcNotaEmpenho.GetValue())
            self.empenho.anoEmpenho = unicode(self.tcAnoEmpenho.GetValue())
            self.empenho.unidadeOrcamentaria = unicode(self.tcUnidadeOrcamentaria.GetValue())
            self.empenho.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'O empenho foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.empenho = None
            self.quitVizualizaEmpenho(None)

    def excluiEmpenho(self, event, idEmpenho):

        if idEmpenho is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este empenho?', 'Excluir - Empenho Convênio', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.empenho = ConvenioEmpenho.query.filter_by(id=idEmpenho).first()
            self.empenho.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Empenho excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal() 


    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)
        
        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereEmpenhoPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.empenhoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.empenhoGeraArquivoListCtrl.InsertColumn(0, u'Num. Convênio', width=100)
        self.empenhoGeraArquivoListCtrl.InsertColumn(1, u'Nota Empenho', width=80)
        self.empenhoGeraArquivoListCtrl.InsertColumn(2, u'Uni. Orçament.', width=70)
        self.empenhoGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoGeraArquivoListCtrl.InsertColumn(4, u'', width=0)
        self.empenhoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensEmpenhoGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.empenhoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.empenhoParaArquivoListCtrl.InsertColumn(0, u'Num. Convênio', width=100)
        self.empenhoParaArquivoListCtrl.InsertColumn(1, u'Nota Empenho', width=80)
        self.empenhoParaArquivoListCtrl.InsertColumn(2, u'Uni. Orçament.', width=70)
        self.empenhoParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoParaArquivoListCtrl.InsertColumn(4, u'', width=0)
        self.empenhoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensEmpenhoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereEmpenhoPorCompetencia(self, event):

        empenhos = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            empenhos = ConvenioEmpenho.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            empenhos = Cotacao.query.all()

        self.empenhoGeraArquivoListCtrl.DeleteAllItems()

        if not empenhos:
            self.message = wx.MessageDialog(None, u'Não existe empenhos para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(empenhos) == self.empenhoParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for empenho in empenhos:
                    igual = False
                    if self.empenhoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.empenhoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.numeroConvenio))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(empenho.notaEmpenho))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(empenho.unidadeOrcamentaria))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(empenho.anoEmpenho))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(empenho.id))
                        igual = True

                    else:

                        for x in range(self.empenhoParaArquivoListCtrl.GetItemCount()):

                            if empenho.numeroConvenio == unicode(self.empenhoParaArquivoListCtrl.GetItem(x, 0).GetText()) and empenho.notaEmpenho == unicode(self.empenhoParaArquivoListCtrl.GetItem(x, 1).GetText()) and empenho.unidadeOrcamentaria == unicode(self.empenhoParaArquivoListCtrl.GetItem(x, 2).GetText()) and empenho.anoEmpenho == unicode(self.empenhoParaArquivoListCtrl.GetItem(x, 3).GetText()):
                                igual = True

                    if not igual:

                        index = self.empenhoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.numeroConvenio))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(empenho.notaEmpenho))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(empenho.unidadeOrcamentaria))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(empenho.anoEmpenho))
                        self.empenhoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(empenho.id))
                        

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensEmpenhoGeraArquivos(self, event):

        item = self.empenhoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.empenhoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensEmpenhoParaArquivo(self, event):

        item = self.empenhoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.empenhoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os empenhos a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.empenhoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.empenhoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.empenhoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.empenhoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.empenhoGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.empenhoParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.empenhoGeraArquivoListCtrl.GetItem(item, 3).GetText()))
                self.empenhoParaArquivoListCtrl.SetStringItem(index, 4, unicode(self.empenhoGeraArquivoListCtrl.GetItem(item, 4).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.empenhoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os empenhos a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.empenhoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.empenhoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.empenhoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.empenhoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.empenhoParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.empenhoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(self.empenhoParaArquivoListCtrl.GetItem(item, 3).GetText()))
                self.empenhoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(self.empenhoParaArquivoListCtrl.GetItem(item, 4).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.empenhoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.empenhoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os empenhos para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="CONVENIOEMPENHO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        #VERIFICAR AS DEPENDENCIAS AKI DEPOIS
                        #self.message = wx.MessageDialog(None, u'Após criar o arquivo de convênios é necessário gerar o arquivo de Participantes de Convênio!\n', 'Info', wx.OK | wx.ICON_EXCLAMATION)
                        #self.message.ShowModal()

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Empenhos de Convênio gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Empenhos de Convênio com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.empenhoParaArquivoListCtrl.GetItemCount()):

            try:

                idEmpenho = int(self.empenhoParaArquivoListCtrl.GetItem(x, 4).GetText())
                empenho = ConvenioEmpenho.query.filter_by(id=idEmpenho).first()

                f.write(unicode(empenho.numeroConvenio.ljust(16).replace("'", "").replace("\"", "")))
                f.write(unicode(empenho.notaEmpenho.ljust(10).replace("'", "").replace("\"", "")))
                f.write(unicode(empenho.anoEmpenho.zfill(4)))
                f.write(unicode(empenho.unidadeOrcamentaria.ljust(6).replace("'", "").replace("\"", "")))
                f.write(unicode(u'\n'))

            except:
                return 0
        return 1
