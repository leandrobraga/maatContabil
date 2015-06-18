# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs
import burocracia

setup_all()

ID_TOOLBAR_EMPENHO_ATA_NOVO = 5001
ID_TOOLBAR_EMPENHO_ATA_EDITAR = 5002
ID_TOOLBAR_EMPENHO_ATA_EXCLUIR = 5003
ID_TOOLBAR_EMPENHO_ATA_CRIAR_ARQUIVO = 5004


class WindowEmpenhoAta(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Adesão Ata Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEmpenhoAta = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_ATA_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo Ata de Empenho')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_ATA_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Ata de Empenho selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_ATA_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Ata de Empenho selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_ATA_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de Ata de Empenho')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelEmpenhoAta, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.empenhoAtaListCtrl = wx.ListCtrl(self.panelEmpenhoAta, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.empenhoAtaListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.empenhoAtaListCtrl.InsertColumn(1, u'Número da Ata', width=200)
        self.empenhoAtaListCtrl.InsertColumn(2, u'Num. Nota Empenho', width=220)
        self.empenhoAtaListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoAtaListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.empenhoAtaListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.empenhoAtaListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoEmpenhoAta, id=ID_TOOLBAR_EMPENHO_ATA_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaLicitacaoAta(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHO_ATA_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiLicitacaoAta(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHO_ATA_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_EMPENHO_ATA_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_ATA_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_ATA_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_ATA_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_ATA_CRIAR_ARQUIVO, gerar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.empenhoAtaListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def insereInCtrList(self, event):

        self.empenhoAtaListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            emepenhos = EmpenhoAta.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for empenho in emepenhos:

                index = self.empenhoAtaListCtrl.InsertStringItem(sys.maxint, unicode(empenho.processoCompra))
                self.empenhoAtaListCtrl.SetStringItem(index, 1, empenho.numeroAta)
                self.empenhoAtaListCtrl.SetStringItem(index, 2, empenho.numeroNotaEmpenho)
                self.empenhoAtaListCtrl.SetStringItem(index, 3, unicode(empenho.id))

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def novoEmpenhoAta(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoEmpenhoAta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(445, 280), pos=(300, 150), title=u'Novo - Ata de Empenho', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoEmpenhoAta = wx.Panel(self.windowNovoEmpenhoAta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoEmpenhoAta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoEmpenhoAta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoEmpenhoAta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        
        wx.StaticBox(self.panelNovoEmpenhoAta, -1, pos=(5, 50), size=(420, 140))

        self.stProcessoCompra = wx.StaticText(self.panelNovoEmpenhoAta, -1, u'Num. do Proc. de Compra', pos=(10, 70))
        self.tcProcessoCompra = wx.TextCtrl(self.panelNovoEmpenhoAta, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoCompra.SetMaxLength(18)

        self.stNumeroAta = wx.StaticText(self.panelNovoEmpenhoAta, -1, u'Número da Adesão Ata', pos=(200, 70))
        self.tcNumeroAta = wx.TextCtrl(self.panelNovoEmpenhoAta, -1, pos=(200, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroAta.SetMaxLength(18)

        self.stNumeroNotaEmpenho = wx.StaticText(self.panelNovoEmpenhoAta, -1, u'Num. da Nota de Empenho', pos=(10, 130))
        self.tcNumeroNotaEmpenho = wx.TextCtrl(self.panelNovoEmpenhoAta, -1, pos=(10, 150), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroNotaEmpenho.SetMaxLength(10) 
        
        self.stAnoEmpenho = wx.StaticText(self.panelNovoEmpenhoAta, -1, u'Ano do Empenho', pos=(170, 130))
        self.tcAnoEmpenho = wx.TextCtrl(self.panelNovoEmpenhoAta, -1, pos=(170, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcAnoEmpenho.SetMaxLength(4)

        self.stCodigoUnidade = wx.StaticText(self.panelNovoEmpenhoAta, -1, u'Cód. da un. Orçamentária', pos=(290, 130))
        self.tcCodigoUnidade = wx.TextCtrl(self.panelNovoEmpenhoAta, -1, pos=(290, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoUnidade.SetMaxLength(6)
        
        self.btnSalvar = wx.Button(self.panelNovoEmpenhoAta, -1, u"Salvar", pos=(150, 200))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarEmpenhoAta)
        self.btnCancelar = wx.Button(self.panelNovoEmpenhoAta, -1, u"Cancelar", pos=(250, 200))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoEmpenhoAta)      

        #Bind
        self.windowNovoEmpenhoAta.Bind(wx.EVT_CLOSE, self.quitNovoEmpenhoAta)

        self.windowNovoEmpenhoAta.Centre()
        self.windowNovoEmpenhoAta.Show()

    def quitNovoEmpenhoAta(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoEmpenhoAta.Destroy()

    def vizualizaLicitacaoAta(self,event,idEmpenhoAta):
        
        if idEmpenhoAta is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Ata de Empenho foi selecionada! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.empenho = EmpenhoAta.query.filter_by(id=idEmpenhoAta).first()

        self.windowEditaEmpenhoAta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(445, 280), pos=(300, 150), title=u'Novo - Ata de Empenho', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaEmpenhoAta = wx.Panel(self.windowEditaEmpenhoAta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelEditaEmpenhoAta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.empenho.id))

        self.stCompetencia = wx.StaticText(self.panelEditaEmpenhoAta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaEmpenhoAta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.empenho.competencia)

        wx.StaticBox(self.panelEditaEmpenhoAta, -1, pos=(5, 50), size=(420, 140))

        self.stProcessoCompra = wx.StaticText(self.panelEditaEmpenhoAta, -1, u'Num. do Proc. de Compra', pos=(10, 70))
        self.tcProcessoCompra = wx.TextCtrl(self.panelEditaEmpenhoAta, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoCompra.SetMaxLength(18)
        self.tcProcessoCompra.SetValue(self.empenho.processoCompra)

        self.stNumeroAta = wx.StaticText(self.panelEditaEmpenhoAta, -1, u'Número da Adesão Ata', pos=(200, 70))
        self.tcNumeroAta = wx.TextCtrl(self.panelEditaEmpenhoAta, -1, pos=(200, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroAta.SetMaxLength(18)
        self.tcNumeroAta.SetValue(self.empenho.numeroAta)

        self.stNumeroNotaEmpenho = wx.StaticText(self.panelEditaEmpenhoAta, -1, u'Num. da Nota de Empenho', pos=(10, 130))
        self.tcNumeroNotaEmpenho = wx.TextCtrl(self.panelEditaEmpenhoAta, -1, pos=(10, 150), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroNotaEmpenho.SetMaxLength(10)
        self.tcNumeroNotaEmpenho.SetValue(self.empenho.numeroNotaEmpenho) 
        
        self.stAnoEmpenho = wx.StaticText(self.panelEditaEmpenhoAta, -1, u'Ano do Empenho', pos=(170, 130))
        self.tcAnoEmpenho = wx.TextCtrl(self.panelEditaEmpenhoAta, -1, pos=(170, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcAnoEmpenho.SetMaxLength(4)
        self.tcAnoEmpenho.SetValue(self.empenho.anoEmpenho)

        self.stCodigoUnidade = wx.StaticText(self.panelEditaEmpenhoAta, -1, u'Cód. da un. Orçamentária', pos=(290, 130))
        self.tcCodigoUnidade = wx.TextCtrl(self.panelEditaEmpenhoAta, -1, pos=(290, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoUnidade.SetMaxLength(6)
        self.tcCodigoUnidade.SetValue(self.empenho.codigoUnidade)
        
        self.btnSalvar = wx.Button(self.panelEditaEmpenhoAta, -1, u"Alterar", pos=(150, 200))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarEmpenhoAta)
        self.btnCancelar = wx.Button(self.panelEditaEmpenhoAta, -1, u"Cancelar", pos=(250, 200))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEmpenhoAtaEdita)      
      

        #Bind
        self.windowEditaEmpenhoAta.Bind(wx.EVT_CLOSE, self.quitEmpenhoAtaEdita)

        self.windowEditaEmpenhoAta.Centre()
        self.windowEditaEmpenhoAta.Show()

    def quitEmpenhoAtaEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaEmpenhoAta.Destroy()

    def valida(self):

        if self.cbCompetencia.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Competência', 'Info', wx.OK)
            self.cbCompetencia.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcProcessoCompra.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número do Proc. de Compra deve ser preenchido!', 'Info', wx.OK)
            self.tcProcessoCompra.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroAta.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número da Adesão Ata deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroAta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroNotaEmpenho.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Num. da Nota de Empenho deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroNotaEmpenho.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcAnoEmpenho.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Ano do Empenho deve ser preenchido!', 'Info', wx.OK)
            self.tcAnoEmpenho.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoUnidade.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Cód. da un. Orçamentária deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoUnidade.SetFocus()
            self.message.ShowModal()
            return 0        
       
        return 1

    def salvarEmpenhoAta(self, event):

        if self.valida():

            try:
                EmpenhoAta(processoCompra=unicode(self.tcProcessoCompra.GetValue()),
                        numeroAta=unicode(self.tcNumeroAta.GetValue()),
                        numeroNotaEmpenho=unicode(self.tcNumeroNotaEmpenho.GetValue()),
                        anoEmpenho=unicode(self.tcAnoEmpenho.GetValue()),
                        codigoUnidade=unicode(self.tcCodigoUnidade.GetValue()),
                        competencia=unicode(self.cbCompetencia.GetValue()), 
                        )

                session.commit()
                self.message = wx.MessageDialog(None, u'Ata de Empenho salvo com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoEmpenhoAta.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoEmpenhoAta.Close()

    def editarEmpenhoAta(self, event):

        if self.valida():

            self.empenho.processoCompra=unicode(self.tcProcessoCompra.GetValue())
            self.empenho.numeroAta=unicode(self.tcNumeroAta.GetValue())
            self.empenho.numeroNotaEmpenho=unicode(self.tcNumeroNotaEmpenho.GetValue())
            self.empenho.anoEmpenho=unicode(self.tcAnoEmpenho.GetValue())
            self.empenho.codigoUnidade=unicode(self.tcCodigoUnidade.GetValue())
            self.empenho.competencia=unicode(self.cbCompetencia.GetValue()) 

            session.commit()
            self.message = wx.MessageDialog(None, u'A Ata de Empenho foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.empenho = None
            self.windowEditaEmpenhoAta.Close()

    def excluiLicitacaoAta(self, event, idEmpenhoAta):

        if idEmpenhoAta is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Ata de Empenho?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.empenho = EmpenhoAta.query.filter_by(id=idEmpenhoAta).first()
            self.empenho.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Ata de Empenho excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(710, 470), pos=(300, 170), title=u"Gerar Arquivo de Ata de Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)
        
        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.inserePorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.empenhoAtaGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(300, 300), style=wx.LC_REPORT)
        self.empenhoAtaGeraArquivoListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.empenhoAtaGeraArquivoListCtrl.InsertColumn(1, u'Número da Ata', width=80)
        self.empenhoAtaGeraArquivoListCtrl.InsertColumn(2, u'Num. Nota Empenho', width=80)
        self.empenhoAtaGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoAtaGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(320, 200), size=(60, -1))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(320, 250), size=(60, -1))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.empenhoAtaParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(300, 300), style=wx.LC_REPORT)
        self.empenhoAtaParaArquivoListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.empenhoAtaParaArquivoListCtrl.InsertColumn(1, u'Número da Ata', width=80)
        self.empenhoAtaParaArquivoListCtrl.InsertColumn(2, u'Num. Nota Empenho', width=80)
        self.empenhoAtaParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoAtaParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def inserePorCompetencia(self, event):

        empenhos = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            empenhos = EmpenhoAta.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            empenhos = EmpenhoAta.query.all()

        self.empenhoAtaGeraArquivoListCtrl.DeleteAllItems()

        if not empenhos:
            self.message = wx.MessageDialog(None, u'Não existe Ata de Emepenho para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(empenhos) == self.empenhoAtaParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for empenho in empenhos:
                    igual = False
                    if self.empenhoAtaParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.empenhoAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.processoCompra))
                        self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(empenho.numeroAta))
                        self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(empenho.numeroNotaEmpenho))
                        self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 3, unicode(empenho.id))
                        igual = True

                    else:

                        for x in range(self.empenhoAtaParaArquivoListCtrl.GetItemCount()):

                            if empenho.processoCompra == unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(x, 0).GetText()) and empenho.numeroAta == unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(x, 1).GetText()) and empenho.numeroNotaEmpenho == unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(x, 2).GetText()):
                                igual = True

                    if not igual:

                        index = self.empenhoAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.processoCompra))
                        self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.numeroAta))
                        self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.numeroNotaEmpenho))
                        self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 3, unicode(item.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensGeraArquivos(self, event):

        item = self.empenhoAtaGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.empenhoAtaGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensParaArquivo(self, event):

        item = self.empenhoAtaParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.empenhoAtaParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Ata de Empenho a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.empenhoAtaParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.empenhoAtaGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.empenhoAtaParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoAtaGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.empenhoAtaParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.empenhoAtaGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.empenhoAtaParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.empenhoAtaGeraArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.empenhoAtaGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as Ata de Empenho a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.empenhoAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.empenhoAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.empenhoAtaParaArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.empenhoAtaParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.empenhoAtaParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Ata de Empenho para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="ADESAOATAEMPENHO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Ata de Empenho gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Ata de Empenho gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.empenhoAtaParaArquivoListCtrl.GetItemCount()):

            try:

                idEmpenhoAta = int(self.empenhoAtaParaArquivoListCtrl.GetItem(x, 3).GetText())
                item = EmpenhoAta.query.filter_by(id=idEmpenhoAta).first()

                f.write(unicode(item.processoCompra.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.numeroAta.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.numeroNotaEmpenho.ljust(10).replace("'", "").replace("\"", "")))
                f.write(unicode(item.anoEmpenho.zfill(4)))
                f.write(unicode(item.codigoUnidade.ljust(6).replace("'", "").replace("\"", "")))
                f.write(u'\n')

            except:

                return 0
        
        return 1
   