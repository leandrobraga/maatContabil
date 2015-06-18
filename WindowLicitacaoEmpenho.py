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

ID_TOOLBAR_EMPENHO_LICITACAO_NOVO = 5001
ID_TOOLBAR_EMPENHO_LICITACAO_EDITAR = 5002
ID_TOOLBAR_EMPENHO_LICITACAO_EXCLUIR = 5003
ID_TOOLBAR_EMPENHO_LICITACAO_CRIAR_ARQUIVO = 5004


class WindowLicitacaoEmpenho(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Licitação Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEmpenhoLicitacao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_LICITACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo Ata de Empenho')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_LICITACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Ata de Empenho selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_LICITACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Ata de Empenho selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_LICITACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de Ata de Empenho')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelEmpenhoLicitacao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.empenhoLicitacaoListCtrl = wx.ListCtrl(self.panelEmpenhoLicitacao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.empenhoLicitacaoListCtrl.InsertColumn(0, u'Num. do Proc. Licitatório', width=100)
        self.empenhoLicitacaoListCtrl.InsertColumn(1, u'Ano Empenho', width=200)
        self.empenhoLicitacaoListCtrl.InsertColumn(2, u'Num. Nota Empenho', width=220)
        self.empenhoLicitacaoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoLicitacaoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.empenhoLicitacaoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.empenhoLicitacaoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoEmpenhoLicitacao, id=ID_TOOLBAR_EMPENHO_LICITACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaLicitacaoEmpenho(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHO_LICITACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiLicitacaoEmpenho(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHO_LICITACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_EMPENHO_LICITACAO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_LICITACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_LICITACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_LICITACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_LICITACAO_CRIAR_ARQUIVO, gerar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.empenhoLicitacaoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def insereInCtrList(self, event):

        self.empenhoLicitacaoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            emepenhos = LicitacaoEmpenho.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for empenho in emepenhos:

                index = self.empenhoLicitacaoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.processoLicitacao))
                self.empenhoLicitacaoListCtrl.SetStringItem(index, 1, empenho.anoEmpenho)
                self.empenhoLicitacaoListCtrl.SetStringItem(index, 2, empenho.numeroNotaEmpenho)
                self.empenhoLicitacaoListCtrl.SetStringItem(index, 3, unicode(empenho.id))

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def novoEmpenhoLicitacao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoEmpenhoLicitacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(445, 280), pos=(300, 150), title=u'Novo - Licitação Empenho', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoEmpenhoLicitacao = wx.Panel(self.windowNovoEmpenhoLicitacao, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoEmpenhoLicitacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoEmpenhoLicitacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoEmpenhoLicitacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        
        wx.StaticBox(self.panelNovoEmpenhoLicitacao, -1, pos=(5, 50), size=(420, 140))

        self.stProcessoLicitacao = wx.StaticText(self.panelNovoEmpenhoLicitacao, -1, u'Num. do Proc. Licitatório', pos=(10, 70))
        self.tcProcessoLicitacao = wx.TextCtrl(self.panelNovoEmpenhoLicitacao, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoLicitacao.SetMaxLength(18)
        
        self.stNumeroNotaEmpenho = wx.StaticText(self.panelNovoEmpenhoLicitacao, -1, u'Num. da Nota de Empenho', pos=(10, 130))
        self.tcNumeroNotaEmpenho = wx.TextCtrl(self.panelNovoEmpenhoLicitacao, -1, pos=(10, 150), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroNotaEmpenho.SetMaxLength(10) 
        
        self.stAnoEmpenho = wx.StaticText(self.panelNovoEmpenhoLicitacao, -1, u'Ano do Empenho', pos=(170, 130))
        self.tcAnoEmpenho = wx.TextCtrl(self.panelNovoEmpenhoLicitacao, -1, pos=(170, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcAnoEmpenho.SetMaxLength(4)

        self.stCodigoUnidade = wx.StaticText(self.panelNovoEmpenhoLicitacao, -1, u'Cód. da un. Orçamentária', pos=(290, 130))
        self.tcCodigoUnidade = wx.TextCtrl(self.panelNovoEmpenhoLicitacao, -1, pos=(290, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoUnidade.SetMaxLength(6)
        
        self.btnSalvar = wx.Button(self.panelNovoEmpenhoLicitacao, -1, u"Salvar", pos=(150, 200))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarEmpenhoLicitacao)
        self.btnCancelar = wx.Button(self.panelNovoEmpenhoLicitacao, -1, u"Cancelar", pos=(250, 200))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoEmpenhoLicitacao)      

        #Bind
        self.windowNovoEmpenhoLicitacao.Bind(wx.EVT_CLOSE, self.quitNovoEmpenhoLicitacao)

        self.windowNovoEmpenhoLicitacao.Centre()
        self.windowNovoEmpenhoLicitacao.Show()

    def quitNovoEmpenhoLicitacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoEmpenhoLicitacao.Destroy()

    def vizualizaLicitacaoEmpenho(self,event,idEmpenhoLicitacao):
        
        if idEmpenhoLicitacao is None:
            self.message = wx.MessageDialog(None, u'Nenhum Lcitação Empenho foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.empenho = LicitacaoEmpenho.query.filter_by(id=idEmpenhoLicitacao).first()

        self.windowEditaEmpenhoLicitacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(445, 280), pos=(300, 150), title=u'Novo - Ata de Empenho', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaEmpenhoLicitacao = wx.Panel(self.windowEditaEmpenhoLicitacao, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelEditaEmpenhoLicitacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.empenho.id))

        self.stCompetencia = wx.StaticText(self.panelEditaEmpenhoLicitacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaEmpenhoLicitacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.empenho.competencia)

        wx.StaticBox(self.panelEditaEmpenhoLicitacao, -1, pos=(5, 50), size=(420, 140))

        self.stProcessoLicitacao = wx.StaticText(self.panelEditaEmpenhoLicitacao, -1, u'Num. do Proc. Licitatório', pos=(10, 70))
        self.tcProcessoLicitacao = wx.TextCtrl(self.panelEditaEmpenhoLicitacao, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoLicitacao.SetMaxLength(18)
        self.tcProcessoLicitacao.SetValue(self.empenho.processoLicitacao)

        self.stNumeroNotaEmpenho = wx.StaticText(self.panelEditaEmpenhoLicitacao, -1, u'Num. da Nota de Empenho', pos=(10, 130))
        self.tcNumeroNotaEmpenho = wx.TextCtrl(self.panelEditaEmpenhoLicitacao, -1, pos=(10, 150), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroNotaEmpenho.SetMaxLength(10)
        self.tcNumeroNotaEmpenho.SetValue(self.empenho.numeroNotaEmpenho) 
        
        self.stAnoEmpenho = wx.StaticText(self.panelEditaEmpenhoLicitacao, -1, u'Ano do Empenho', pos=(170, 130))
        self.tcAnoEmpenho = wx.TextCtrl(self.panelEditaEmpenhoLicitacao, -1, pos=(170, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcAnoEmpenho.SetMaxLength(4)
        self.tcAnoEmpenho.SetValue(self.empenho.anoEmpenho)

        self.stCodigoUnidade = wx.StaticText(self.panelEditaEmpenhoLicitacao, -1, u'Cód. da un. Orçamentária', pos=(290, 130))
        self.tcCodigoUnidade = wx.TextCtrl(self.panelEditaEmpenhoLicitacao, -1, pos=(290, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoUnidade.SetMaxLength(6)
        self.tcCodigoUnidade.SetValue(self.empenho.codigoUnidade)
        
        self.btnSalvar = wx.Button(self.panelEditaEmpenhoLicitacao, -1, u"Alterar", pos=(150, 200))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarEmpenhoAta)
        self.btnCancelar = wx.Button(self.panelEditaEmpenhoLicitacao, -1, u"Cancelar", pos=(250, 200))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEmpenhoAtaEdita)      
      

        #Bind
        self.windowEditaEmpenhoLicitacao.Bind(wx.EVT_CLOSE, self.quitEmpenhoAtaEdita)

        self.windowEditaEmpenhoLicitacao.Centre()
        self.windowEditaEmpenhoLicitacao.Show()

    def quitEmpenhoAtaEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaEmpenhoLicitacao.Destroy()

    def valida(self):

        if self.cbCompetencia.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Competência', 'Info', wx.OK)
            self.cbCompetencia.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcProcessoLicitacao.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número do Proc. de Compra deve ser preenchido!', 'Info', wx.OK)
            self.tcProcessoLicitacao.SetFocus()
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

    def salvarEmpenhoLicitacao(self, event):

        if self.valida():

            try:
                LicitacaoEmpenho(processoLicitacao=unicode(self.tcProcessoLicitacao.GetValue()),
                        numeroNotaEmpenho=unicode(self.tcNumeroNotaEmpenho.GetValue()),
                        anoEmpenho=unicode(self.tcAnoEmpenho.GetValue()),
                        codigoUnidade=unicode(self.tcCodigoUnidade.GetValue()),
                        competencia=unicode(self.cbCompetencia.GetValue()), 
                        )

                session.commit()
                self.message = wx.MessageDialog(None, u'Licitação Empenho salvo com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoEmpenhoLicitacao.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoEmpenhoLicitacao.Close()

    def editarEmpenhoAta(self, event):

        if self.valida():

            self.empenho.processoLicitacao=unicode(self.tcProcessoLicitacao.GetValue())
            self.empenho.numeroNotaEmpenho=unicode(self.tcNumeroNotaEmpenho.GetValue())
            self.empenho.anoEmpenho=unicode(self.tcAnoEmpenho.GetValue())
            self.empenho.codigoUnidade=unicode(self.tcCodigoUnidade.GetValue())
            self.empenho.competencia=unicode(self.cbCompetencia.GetValue()) 

            session.commit()
            self.message = wx.MessageDialog(None, u'A Licitação Empenho foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.empenho = None
            self.windowEditaEmpenhoLicitacao.Close()

    def excluiLicitacaoEmpenho(self, event, idEmpenhoLicitacao):

        if idEmpenhoLicitacao is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Licitação Empenho?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.empenho = LicitacaoEmpenho.query.filter_by(id=idEmpenhoLicitacao).first()
            self.empenho.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Licitação Empenho excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(710, 470), pos=(300, 170), title=u"Gerar Arquivo de Licitação Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
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
        self.empenhoLicitacaoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(300, 300), style=wx.LC_REPORT)
        self.empenhoLicitacaoGeraArquivoListCtrl.InsertColumn(0, u'Num. do Proc. Licitatório', width=100)
        self.empenhoLicitacaoGeraArquivoListCtrl.InsertColumn(1, u'Ano Empenho', width=80)
        self.empenhoLicitacaoGeraArquivoListCtrl.InsertColumn(2, u'Num. Nota Empenho', width=80)
        self.empenhoLicitacaoGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoLicitacaoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(320, 200), size=(60, -1))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(320, 250), size=(60, -1))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.empenhoLicitacaoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(300, 300), style=wx.LC_REPORT)
        self.empenhoLicitacaoParaArquivoListCtrl.InsertColumn(0, u'Num. do Proc. Licitatório', width=100)
        self.empenhoLicitacaoParaArquivoListCtrl.InsertColumn(1, u'Ano Empenho', width=80)
        self.empenhoLicitacaoParaArquivoListCtrl.InsertColumn(2, u'Num. Nota Empenho', width=80)
        self.empenhoLicitacaoParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.empenhoLicitacaoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParaArquivo)

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

            empenhos = LicitacaoEmpenho.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            empenhos = EmpenhoAta.query.all()

        self.empenhoLicitacaoGeraArquivoListCtrl.DeleteAllItems()

        if not empenhos:
            self.message = wx.MessageDialog(None, u'Não existe Licitação de Empenho para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(empenhos) == self.empenhoLicitacaoParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for empenho in empenhos:
                    igual = False
                    if self.empenhoLicitacaoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.empenhoLicitacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.processoLicitacao))
                        self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(empenho.anoEmpenho))
                        self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(empenho.numeroNotaEmpenho))
                        self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(empenho.id))
                        igual = True

                    else:

                        for x in range(self.empenhoLicitacaoParaArquivoListCtrl.GetItemCount()):

                            if empenho.processoCompra == unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(x, 0).GetText()) and empenho.anoEmpenho == unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(x, 1).GetText()) and empenho.numeroNotaEmpenho == unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(x, 2).GetText()):
                                igual = True

                    if not igual:

                        index = self.empenhoLicitacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.processoLicitacao))
                        self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.anoEmpenho))
                        self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.numeroNotaEmpenho))
                        self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(item.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensGeraArquivos(self, event):

        item = self.empenhoLicitacaoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.empenhoLicitacaoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensParaArquivo(self, event):

        item = self.empenhoLicitacaoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.empenhoLicitacaoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Ata de Empenho a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.empenhoLicitacaoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.empenhoLicitacaoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.empenhoLicitacaoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoLicitacaoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.empenhoLicitacaoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.empenhoLicitacaoGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.empenhoLicitacaoParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.empenhoLicitacaoGeraArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.empenhoLicitacaoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as Ata de Empenho a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.empenhoLicitacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.empenhoLicitacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.empenhoLicitacaoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.empenhoLicitacaoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Ata de Empenho para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="LICITACAOEMPENHO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Licitação Empenho gerado com sucesso!', 'Info', wx.OK)
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

        for x in range(self.empenhoLicitacaoParaArquivoListCtrl.GetItemCount()):

            try:

                idEmpenhoLicitacao = int(self.empenhoLicitacaoParaArquivoListCtrl.GetItem(x, 3).GetText())
                item = LicitacaoEmpenho.query.filter_by(id=idEmpenhoLicitacao).first()

                f.write(unicode(item.processoLicitacao.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.numeroNotaEmpenho.ljust(10).replace("'", "").replace("\"", "")))
                f.write(unicode(item.anoEmpenho.zfill(4)))
                f.write(unicode(item.codigoUnidade.ljust(6).replace("'", "").replace("\"", "")))
                f.write(u'\n')

            except:

                return 0
        
        return 1
   