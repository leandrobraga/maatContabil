# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs
from sqlalchemy import func

setup_all()

ID_TOOLBAR_PUBLICACAO_NOVO = 5001
ID_TOOLBAR_PUBLICACAO_EDITAR = 5002
ID_TOOLBAR_PUBLICACAO_EXCLUIR = 5003
ID_TOOLBAR_PUBLICACAO_CRIAR_ARQUIVO = 5004


class WindowPublicacao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Publicação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelPublicacao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_PUBLICACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova publicação')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PUBLICACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita publicação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PUBLICACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui publicação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PUBLICACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de publicação')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelPublicacao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.publicacaoListCtrl = wx.ListCtrl(self.panelPublicacao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.publicacaoListCtrl.InsertColumn(0, u'Licitação', width=150)
        self.publicacaoListCtrl.InsertColumn(1, u'Data Publicação', width=200)
        self.publicacaoListCtrl.InsertColumn(2, u'Veículo', width=170)
        self.publicacaoListCtrl.InsertColumn(3, u'', width=0)
        self.publicacaoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.publicacaoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.publicacaoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoPublicacao, id=ID_TOOLBAR_PUBLICACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaPublicacao(event, self.idSelecionado), id=ID_TOOLBAR_PUBLICACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiPublicacao(event, self.idSelecionado), id=ID_TOOLBAR_PUBLICACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_PUBLICACAO_CRIAR_ARQUIVO)
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

        self.idSelecionado = self.publicacaoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_PUBLICACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_PUBLICACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_PUBLICACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_PUBLICACAO_CRIAR_ARQUIVO, gerar)

    def insereInCtrList(self, event):

        self.publicacaoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            publicacoes = Publicacao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for publicacao in publicacoes:

                index = self.publicacaoListCtrl.InsertStringItem(sys.maxint, unicode(publicacao.numeroProcesso))
                self.publicacaoListCtrl.SetStringItem(index, 1, publicacao.dataPublicacao)
                self.publicacaoListCtrl.SetStringItem(index, 2, publicacao.veiculoComunicacao)
                self.publicacaoListCtrl.SetStringItem(index, 3, unicode(publicacao.id))

    def novoPublicacao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovopublicacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 270), pos=(300, 170), title=u'Novo - Publicação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoPublicacao = wx.Panel(self.windowNovopublicacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoPublicacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoPublicacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoPublicacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)

        wx.StaticBox(self.panelNovoPublicacao, -1, pos=(5, 50), size=(480, 140))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoPublicacao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoPublicacao, -1, pos=(10, 90), size=(100, -1), style=wx.CB_READONLY)

        self.stDataPublicacao = wx.StaticText(self.panelNovoPublicacao, -1, u'Data Publicação', pos=(160, 70))
        self.tcDataPublicacao = masked.TextCtrl(self.panelNovoPublicacao, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((160, 90))
        
        self.stVeiculoComunicacao = wx.StaticText(self.panelNovoPublicacao, -1, u'Veículo de Comunicação', pos=(10, 130))
        self.tcVeiculoComunicacao = wx.TextCtrl(self.panelNovoPublicacao, -1, pos=(10, 150), size=(320, -1), style=wx.ALIGN_LEFT)
        self.tcVeiculoComunicacao.SetMaxLength(50)

        self.btnSalvar = wx.Button(self.panelNovoPublicacao, -1, u"Salvar", pos=(150, 210))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarPublicacao)
        self.btnCancelar = wx.Button(self.panelNovoPublicacao, -1, u"Cancelar", pos=(250, 210))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoPublicacao)

        #Bind
        self.windowNovopublicacao.Bind(wx.EVT_CLOSE, self.quitNovoPublicacao)

        self.windowNovopublicacao.Centre()
        self.windowNovopublicacao.Show()

    def quitNovoPublicacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovopublicacao.Destroy()

    def insereNumeroProcesso(self, event):

        self.cbNumeroProcesso.Clear()

        licitacoes = Licitacao.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()

        if not licitacoes:
            self.message = wx.MessageDialog(None, u'Não existe Licitações para a competência selecionada!', 'Info', wx.OK)
            self.message.ShowModal()
            self.cnNumeroProcesso.Disable()

        else:
            for licitacao in licitacoes:

                self.cbNumeroProcesso.Append(unicode(licitacao.numeroProcessoLicitatorio))

            self.cbNumeroProcesso.Enable()

    def validateDate(self, date, field):

        if date == "  /  /    ":
            self.message = wx.MessageDialog(None, u'O campo '+field+' deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if date[0:2] == '  ':
            self.message = wx.MessageDialog(None, u'Preencha o dia no campo '+field, 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if date[3:5] == '  ':
            self.message = wx.MessageDialog(None, u'Preencha o mês no campo '+field, 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if date[6:] == '    ':
            self.message = wx.MessageDialog(None, u'Preencha o ano no campo '+field, 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if int(date[0:2]) < 1 or int(date[0:2]) > 31:
                self.message = wx.MessageDialog(None, u'No campo '+field+u' o dia deve estar entre 1 e 31!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0

        if int(date[3:5]) < 1 or int(date[3:5]) > 12:
                self.message = wx.MessageDialog(None, u'No campo '+field+u' o mês deve estar entre 1 e 12!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0

        if int(date[6:]) < 1900:
                self.message = wx.MessageDialog(None, u'No campo '+field+u' o ano deve estar no formato de quatro dígitos!E ser maior que 1900!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0

        if int(date[3:5]) == 2:
            if int(date[0:2]) > 29:
                self.message = wx.MessageDialog(None, u'Campo: '+field+u'\nNo mês de Fevereiro nunca tem um dia maior que 29!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0
            else:
                try:
                    datetime.date(int(date[6:10]), int(date[3:5]), int(date[0:2]))
                except ValueError:
                    self.message = wx.MessageDialog(None, u'Campo: '+field+u'\nEste ano Fevereiro não possui o dia 29!', 'Info', wx.OK)
                    self.message.ShowModal()
                    return 0
        return 1

    def valida(self):

        if self.cbCompetencia.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Competência', 'Info', wx.OK)
            self.cbCompetencia.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbNumeroProcesso.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Número Proc. Licitatório', 'Info', wx.OK)
            self.cbNumeroProcesso.SetFocus()
            self.message.ShowModal()
            return 0
        
        if not self.validateDate(self.tcDataPublicacao.GetValue(), u"Data Publicação"):
            self.tcDataPublicacao.SelectAll()
            self.tcDataPublicacao.SetFocus()
            return 0

        if self.tcVeiculoComunicacao.GetValue() == u'':

            self.message = wx.MessageDialog(None, u'O campo Veículo de Comunicação deve ser preenchido!', 'Info', wx.OK)
            self.tcVeiculoComunicacao.SetFocus()
            self.message.ShowModal()
            return 0

        return 1

    def salvarPublicacao(self, event):

        if self.valida():

            Publicacao(numeroProcesso=unicode(self.cbNumeroProcesso.GetValue()),
                       dataPublicacao=unicode(self.tcDataPublicacao.GetValue()),
                       veiculoComunicacao=unicode(self.tcVeiculoComunicacao.GetValue()),
                       competencia=unicode(self.cbCompetencia.GetValue())
                       )

            session.commit()
            self.message = wx.MessageDialog(None, u'Publicação salva com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitNovoPublicacao(None)

    
    def vizualizaPublicacao(self, event, idPublicacao):

        if idPublicacao is None:
            self.message = wx.MessageDialog(None, u'Nenhuma publicação foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.publicacao = Publicacao.query.filter_by(id=idPublicacao).first()

        self.toolBarControler(False, False, False, False)

        self.windowVizualizapublicacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 270), pos=(300, 170), title=u'Editar - Publicação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelVizualizaPublicacao = wx.Panel(self.windowVizualizapublicacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelVizualizaPublicacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.publicacao.id))

        self.stCompetencia = wx.StaticText(self.panelVizualizaPublicacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelVizualizaPublicacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)
        self.cbCompetencia.SetValue(self.publicacao.competencia)

        wx.StaticBox(self.panelVizualizaPublicacao, -1, pos=(5, 50), size=(480, 140))

        self.stNumeroProcesso = wx.StaticText(self.panelVizualizaPublicacao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelVizualizaPublicacao, -1, pos=(10, 90), size=(100, -1), style=wx.CB_READONLY)
        self.insereNumeroProcesso(None)
        self.cbNumeroProcesso.SetValue(self.publicacao.numeroProcesso)

        self.stDataPublicacao = wx.StaticText(self.panelVizualizaPublicacao, -1, u'Data Publicação', pos=(160, 70))
        self.tcDataPublicacao = masked.TextCtrl(self.panelVizualizaPublicacao, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((160, 90))
        #self.tcDataPublicacao.Bind(wx.EVT_KILL_FOCUS, self.adicionaSequencia)
        self.tcDataPublicacao.SetValue(self.publicacao.dataPublicacao)
        
        self.stVeiculoComunicacao = wx.StaticText(self.panelVizualizaPublicacao, -1, u'Veículo de Comunicação', pos=(10, 130))
        self.tcVeiculoComunicacao = wx.TextCtrl(self.panelVizualizaPublicacao, -1, pos=(10, 150), size=(320, -1), style=wx.ALIGN_LEFT)
        self.tcVeiculoComunicacao.SetMaxLength(50)
        self.tcVeiculoComunicacao.SetValue(self.publicacao.veiculoComunicacao)

        self.btnSalvar = wx.Button(self.panelVizualizaPublicacao, -1, u"Alterar", pos=(150, 210))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarPublicacao)
        self.btnCancelar = wx.Button(self.panelVizualizaPublicacao, -1, u"Cancelar", pos=(250, 210))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaPublicacao)

        #Bind
        self.windowVizualizapublicacao.Bind(wx.EVT_CLOSE, self.quitNovoPublicacao)

        self.windowVizualizapublicacao.Centre()
        self.windowVizualizapublicacao.Show()

    def quitVizualizaPublicacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowVizualizapublicacao.Destroy()

    def editarPublicacao(self, event):

        if self.valida():

            self.publicacao.numeroProcesso = unicode(self.cbNumeroProcesso.GetValue())
            self.publicacao.dataPublicacao = unicode(self.tcDataPublicacao.GetValue())
            self.publicacao.veiculoComunicacao = unicode(self.tcVeiculoComunicacao.GetValue())
            self.publicacao.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'Publicação alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitVizualizaPublicacao(None)

    def excluiPublicacao(self, event, idPublicacao):

        if idPublicacao is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta publicação?', u'Excluir - Publicação', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.publicacao = Publicacao.query.filter_by(id=idPublicacao).first()
            self.publicacao.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Publicação excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo Publicação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Publicação', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.inserePublicacaoPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.publicacaoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.publicacaoGeraArquivoListCtrl.InsertColumn(0, u'Licitação', width=100)
        self.publicacaoGeraArquivoListCtrl.InsertColumn(1, u'Data Publicação', width=80)
        self.publicacaoGeraArquivoListCtrl.InsertColumn(2, u'Veículo', width=70)
        self.publicacaoGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.publicacaoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensPublicacaoGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.publicacaoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.publicacaoParaArquivoListCtrl.InsertColumn(0, u'Licitação', width=100)
        self.publicacaoParaArquivoListCtrl.InsertColumn(1, u'Data Publicação', width=80)
        self.publicacaoParaArquivoListCtrl.InsertColumn(2, u'Veículo', width=70)
        self.publicacaoParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.publicacaoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensPublicacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def inserePublicacaoPorCompetencia(self, event):

        publicacoes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            publicacoes = Publicacao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            publicacoes = Publicacao.query.all()

        self.publicacaoGeraArquivoListCtrl.DeleteAllItems()

        if not publicacoes:
            self.message = wx.MessageDialog(None, u'Não existe publicações para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(publicacoes) == self.publicacaoParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for publicacao in publicacoes:
                    igual = False
                    if self.publicacaoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.publicacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(publicacao.numeroProcesso))
                        self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(publicacao.dataPublicacao))
                        self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(publicacao.veiculoComunicacao))
                        self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(publicacao.id))
                        igual = True

                    else:

                        for x in range(self.publicacaoParaArquivoListCtrl.GetItemCount()):

                            if publicacao.numeroProcesso == unicode(self.publicacaoParaArquivoListCtrl.GetItem(x, 0).GetText()) and publicacao.dataPublicacao == unicode(self.publicacaoParaArquivoListCtrl.GetItem(x, 1).GetText()) and publicacao.veiculoComunicacao == unicode(self.publicacaoParaArquivoListCtrl.GetItem(x, 2).GetText()):
                                igual = True

                    if not igual:

                        index = self.publicacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(publicacao.numeroProcesso))
                        self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(publicacao.dataPublicacao))
                        self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(publicacao.veiculoComunicacao))
                        self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(publicacao.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensPublicacaoGeraArquivos(self, event):

        item = self.publicacaoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.publicacaoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensPublicacaoParaArquivo(self, event):

        item = self.publicacaoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.publicacaoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os publicacoes a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.publicacaoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.publicacaoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.publicacaoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.publicacaoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.publicacaoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.publicacaoGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.publicacaoParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.publicacaoGeraArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.publicacaoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os publicacoes a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.publicacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.publicacaoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.publicacaoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.publicacaoParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.publicacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(self.publicacaoParaArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.publicacaoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.publicacaoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os publicacoes para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="PUBLICACAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Publicações gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Publicações com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.publicacaoParaArquivoListCtrl.GetItemCount()):

            try:

                idEmpenho = int(self.publicacaoParaArquivoListCtrl.GetItem(x, 3).GetText())
                publicacao = Publicacao.query.filter_by(id=idEmpenho).first()

                f.write(unicode(publicacao.numeroProcesso.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(publicacao.dataPublicacao)))
                f.write(unicode(publicacao.veiculoComunicacao).ljust(50).replace("'", "").replace("\"", ""))
                f.write(unicode(u'\n'))

            except:
                return 0
        return 1

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]
