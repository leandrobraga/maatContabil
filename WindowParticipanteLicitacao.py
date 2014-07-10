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

ID_TOOLBAR_PARTICIPANTE_LICITACAO_NOVO = 6001
ID_TOOLBAR_PARTICIPANTE_LICITACAO_EDITAR = 6002
ID_TOOLBAR_PARTICIPANTE_LICITACAO_EXCLUIR = 6003
ID_TOOLBAR_PARTICIPANTE_LICITACAO_CRIAR_ARQUIVO = 6004


class WindowParticipanteLicitacao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Participante de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelParticipanteLicitacao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelParticipanteLicitacao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.participanteListCtrl = wx.ListCtrl(self.panelParticipanteLicitacao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.participanteListCtrl.InsertColumn(0, u'Nome do Participante', width=150)
        self.participanteListCtrl.InsertColumn(1, u'CPF/CNPJ', width=120)
        self.participanteListCtrl.InsertColumn(2, u'Num. do Proc. Licitatório', width=250)
        self.participanteListCtrl.InsertColumn(3, u'', width=0)
        self.participanteListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.participanteListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.participanteListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoParticipanteLicitacao, id=ID_TOOLBAR_PARTICIPANTE_LICITACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaItem(event, self.idSelecionado), id=ID_TOOLBAR_PARTICIPANTE_LICITACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiParticipante(event, self.idSelecionado), id=ID_TOOLBAR_PARTICIPANTE_LICITACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_PARTICIPANTE_LICITACAO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_LICITACAO_CRIAR_ARQUIVO, gerar)

    def insereInCtrList(self, event):

        self.participanteListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:

            participantes = ParticipanteLicitacao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for participante in participantes:

                index = self.participanteListCtrl.InsertStringItem(sys.maxint, unicode(participante.nomeParticipante))
                self.participanteListCtrl.SetStringItem(index, 1, participante.cicParticipante)
                self.participanteListCtrl.SetStringItem(index, 2, participante.numeroProcessoLicitatorio)
                self.participanteListCtrl.SetStringItem(index, 3, unicode(participante.id))

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.participanteListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def novoParticipanteLicitacao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoParticipante = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(350, 380), pos=(300, 170), title=u'Novo - Participante de Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoParticipante = wx.Panel(self.windowNovoParticipante, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoParticipante, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)

        wx.StaticBox(self.panelNovoParticipante, -1, pos=(5, 50), size=(330, 250))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoParticipante, -1, u'Número Proc. Licitatório', pos=(10, 65))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 85), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.verificaParticipante)

        self.stConvidado = wx.StaticText(self.panelNovoParticipante, -1, u'Convidado', pos=(190, 65))
        self.cbConvidado = wx.ComboBox(self.panelNovoParticipante, -1, pos=(190, 85), size=(50, -1), choices=[u'S', u'N'], style=wx.CB_READONLY)

        self.stTipoJuridico = wx.StaticText(self.panelNovoParticipante, -1, u'Tipo Pessoa', pos=(10, 125))
        self.cbTipoJuridico = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 145), size=(150, -1), choices=[u'Física', u'Jurídica', u'Outros'], style=wx.CB_READONLY)
        self.cbTipoJuridico.Bind(wx.EVT_COMBOBOX, self.definirCampoCic)

        self.stCicParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'CNPJ ou CPF', pos=(190, 125), style=wx.ALIGN_LEFT)
        self.tcCicParticipante = masked.TextCtrl(self.panelNovoParticipante, -1, mask="")
        self.tcCicParticipante.SetSize((140, -1))
        self.tcCicParticipante.SetPosition((190, 145))
        self.tcCicParticipante.SetEditable(False)

        self.stNome = wx.StaticText(self.panelNovoParticipante, -1, u'Nome', pos=(10, 185))
        self.tcNome = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 205), size=(320, -1), style=wx.ALIGN_LEFT)
        self.tcNome.SetMaxLength(50)

        self.stTipoParticipacao = wx.StaticText(self.panelNovoParticipante, -1, u'Tipo Participação', pos=(10, 245))
        self.cbTipoParticipacao = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 265), size=(150, -1), choices=[u'Participante comum', u'Consórcio', u'Consorciado'], style=wx.CB_READONLY)
        self.cbTipoParticipacao.Bind(wx.EVT_COMBOBOX, self.habilitaCnpjConsorcio)

        self.stCicConsorcio = wx.StaticText(self.panelNovoParticipante, -1, u'CNPJ Consórcio', pos=(190, 245))
        self.tcCicConsorcio = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##.###.###/####-##")
        self.tcCicConsorcio.SetSize((140, -1))
        self.tcCicConsorcio.SetPosition((190, 265))
        self.tcCicConsorcio.SetEditable(False)

        self.btnSalvar = wx.Button(self.panelNovoParticipante, -1, u'Salvar', pos=(90, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarParticipante)
        self.btnCancelar = wx.Button(self.panelNovoParticipante, -1, u'Cancelar', pos=(190, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoParticipante)

        #Bind
        self.windowNovoParticipante.Bind(wx.EVT_CLOSE, self.quitNovoParticipante)

        self.windowNovoParticipante.Centre()
        self.windowNovoParticipante.Show()

    def quitNovoParticipante(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoParticipante.Destroy()

    def insereNumeroProcesso(self, event):

        self.cbNumeroProcesso.Clear()

        licitacoes = Licitacao.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()

        if not licitacoes:
            self.message = wx.MessageDialog(None, u'Não existe Licitações para a competência selecionada!', 'Info', wx.OK)
            self.message.ShowModal()

        else:
            for licitacao in licitacoes:

                self.cbNumeroProcesso.Append(unicode(licitacao.numeroProcessoLicitatorio))

            self.cbNumeroProcesso.Enable()

    def verificaParticipante(self, event):

        licitacao = Licitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).first()
        
        if licitacao.modalidadeLicitacao == u'Deserta' or licitacao.modalidadeLicitacao == u'Fracassada':
            
            self.cbConvidado.SetSelection(-1)
            self.cbConvidado.Disable()
            self.cbTipoJuridico.SetSelection(-1)
            self.cbTipoJuridico.Disable()
            self.tcCicParticipante.SetValue("")
            self.tcCicParticipante.Disable()
            self.tcNome.SetValue("")
            self.tcNome.Disable()
            self.cbTipoParticipacao.SetSelection(-1)
            self.cbTipoParticipacao.Disable()
            self.tcCicConsorcio.SetValue("")
            self.tcCicConsorcio.Disable()
            self.btnSalvar.Disable()

            self.message = wx.MessageDialog(None, u'Esta licitação não necessita de Participantes de Licitação.\n Esta licitação pertence a modalidade de licitação: Deserta ou Fracassada.', 'Info', wx.OK)
            self.message.ShowModal()


        else:

            self.cbConvidado.SetSelection(-1)
            self.cbConvidado.Enable()
            self.cbTipoJuridico.SetSelection(-1)
            self.cbTipoJuridico.Enable()
            self.tcCicParticipante.SetValue("")
            self.tcCicParticipante.Enable()
            self.tcNome.SetValue("")
            self.tcNome.Enable()
            self.cbTipoParticipacao.SetSelection(-1)
            self.cbTipoParticipacao.Enable()
            self.tcCicConsorcio.SetValue("")
            self.tcCicConsorcio.Enable()
            self.btnSalvar.Enable()


            
            

    def definirCampoCic(self, event):

        if self.cbTipoJuridico.GetValue() == u"Física":

            self.tcCicParticipante.SetValue('')
            self.tcCicParticipante.SetMask(("###.###.###-##"))
            self.tcCicParticipante.SetEditable(True)

        elif self.cbTipoJuridico.GetValue() == u"Jurídica":

            self.tcCicParticipante.SetValue('')
            self.tcCicParticipante.SetMask(("##.###.###/####-##"))
            self.tcCicParticipante.SetEditable(True)
        else:

            self.tcCicParticipante.SetValue('')
            self.tcCicParticipante.SetMask(("###############"))
            self.tcCicParticipante.SetMask(("##############"))
            self.tcCicParticipante.SetEditable(True)

    def habilitaCnpjConsorcio(self, event):

        if event.GetString() == u'Consórcio' or event.GetString() == u'Consorciado':
            self.tcCicConsorcio.SetEditable(True)
        else:
            self.tcCicConsorcio.SetValue("")
            self.tcCicConsorcio.SetEditable(False)

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

        if self.cbConvidado.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Convidado', 'Info', wx.OK)
            self.cbConvidado.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoJuridico.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Pessoa', 'Info', wx.OK)
            self.cbTipoJuridico.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoJuridico.GetSelection() == 0:
            if self.tcCicParticipante.GetValue() == "   .   .   -  ":
                self.message = wx.MessageDialog(None, u'O campo CNPJ ou CPF deve ser preenchido', 'Info', wx.OK)
                self.tcCicParticipante.SelectAll()
                self.tcCicParticipante.SetFocus()
                self.message.ShowModal()
                return 0

            if not burocracia.CPF(self.tcCicParticipante.GetValue()).isValid():
                self.message = wx.MessageDialog(None, u'CPF inválido!', 'Info', wx.OK)
                self.tcCicParticipante.SelectAll()
                self.tcCicParticipante.SetFocus()
                self.message.ShowModal()
                return 0

        if self.cbTipoJuridico.GetSelection() == 1:
            if self.tcCicParticipante.GetValue() == "  .   .   /    -  ":
                self.message = wx.MessageDialog(None, u'O campo CNPJ ou CPF deve ser preenchido', 'Info', wx.OK)
                self.tcCicParticipante.SelectAll()
                self.tcCicParticipante.SetFocus()
                self.message.ShowModal()
                return 0

            if not burocracia.CNPJ(self.tcCicParticipante.GetValue()).isValid():
                self.message = wx.MessageDialog(None, u'CNPJ inválido!', 'Info', wx.OK)
                self.tcCicParticipante.SelectAll()
                self.tcCicParticipante.SetFocus()
                self.message.ShowModal()
                return 0

        if self.cbTipoJuridico.GetSelection() == 2:
            if self.tcCicParticipante.GetValue() == '              ':
                self.message = wx.MessageDialog(None, u'Digite o identificador no campo CNPJ ou CPF', 'Info', wx.OK)
                self.tcCicParticipante.SelectAll()
                self.tcCicParticipante.SetFocus()
                self.message.ShowModal()
                return 0

        if self.tcNome.GetValue() == '':
            self.message = wx.MessageDialog(None, u'O campo Nome deve ser preenchido!', 'Info', wx.OK)
            self.tcNome.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoParticipacao.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Partição', 'Info', wx.OK)
            self.cbTipoParticipacao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoParticipacao.GetSelection == 1 or self.cbTipoParticipacao.GetSelection == 2:
            if self.tcCicConsorcio.GetValue() == "  .   .   /    -  ":
                self.message = wx.MessageDialog(None, u'O campo CNPJ Consórcio deve ser preenchido', 'Info', wx.OK)
                self.tcCicConsorcio.SelectAll()
                self.tcCicConsorcio.SetFocus()
                self.message.ShowModal()
                return 0

            if not burocracia.CNPJ(self.tcCicConsorcio.GetValue()).isValid():
                self.message = wx.MessageDialog(None, u'CNPJ do Consórcio inválido!', 'Info', wx.OK)
                self.tcCicConsorcio.SelectAll()
                self.tcCicConsorcio.SetFocus()
                self.message.ShowModal()
                return 0

        participantes = ParticipanteLicitacao.query.filter_by(cicParticipante=self.tcCicParticipante.GetValue()).all()
        
        if participantes:
            for participante in participantes:
                
                if (unicode(participante.cicParticipante.upper()) == unicode(self.tcCicParticipante.GetValue().upper())) and (participante.id != int(self.tcId.GetValue())) and (unicode(participante.numeroProcessoLicitatorio) == self.cbNumeroProcesso.GetValue()):
                    self.message = wx.MessageDialog(None, u'Participante já cadastrado para esta licitação!', 'Info', wx.OK)
                    self.tcCicParticipante.SetFocus()
                    self.message.ShowModal()
                    return 0

        return 1

    def salvarParticipante(self, event):

        if self.valida():

            ParticipanteLicitacao(
                numeroProcessoLicitatorio=unicode(self.cbNumeroProcesso.GetValue()),
                cicParticipante=unicode(self.tcCicParticipante.GetValue()),
                tipoJuridicoParticipante=unicode(self.cbTipoJuridico.GetValue()),
                nomeParticipante=unicode(self.tcNome.GetValue()),
                tipoParticipacao=unicode(self.cbTipoParticipacao.GetValue()),
                cicConsorcio=unicode(self.tcCicConsorcio.GetValue()),
                participanteConvidado=unicode(self.cbConvidado.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue())
            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Participante de Licitação salvo com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.windowNovoParticipante.Close()

    def vizualizaItem(self, event, idParticipante):

        if idParticipante is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Participante de Licitação foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.participante = ParticipanteLicitacao.query.filter_by(id=idParticipante).first() 

        self.toolBarControler(False, False, False, False)

        self.windowVizualizaParticipante = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(350, 380), pos=(300, 170), title=u'Editar - Participante de Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoParticipante = wx.Panel(self.windowVizualizaParticipante, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.participante.id))

        self.stCompetencia = wx.StaticText(self.panelNovoParticipante, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)
        self.cbCompetencia.SetValue(self.participante.competencia)

        wx.StaticBox(self.panelNovoParticipante, -1, pos=(5, 50), size=(330, 250))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoParticipante, -1, u'Número Proc. Licitatório', pos=(10, 65))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 85), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.insereNumeroProcesso(None)
        self.cbNumeroProcesso.SetValue(self.participante.numeroProcessoLicitatorio)
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.verificaParticipante)

        self.stConvidado = wx.StaticText(self.panelNovoParticipante, -1, u'Convidado', pos=(190, 65))
        self.cbConvidado = wx.ComboBox(self.panelNovoParticipante, -1, pos=(190, 85), size=(50, -1), choices=[u'S', u'N'], style=wx.CB_READONLY)
        self.cbConvidado.SetValue(self.participante.participanteConvidado)

        self.stTipoJuridico = wx.StaticText(self.panelNovoParticipante, -1, u'Tipo Pessoa', pos=(10, 125))
        self.cbTipoJuridico = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 145), size=(150, -1), choices=[u'Física', u'Jurídica', u'Outros'], style=wx.CB_READONLY)
        self.cbTipoJuridico.Bind(wx.EVT_COMBOBOX, self.definirCampoCic)
        self.cbTipoJuridico.SetValue(self.participante.tipoJuridicoParticipante)

        self.stCicParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'CNPJ ou CPF', pos=(190, 125), style=wx.ALIGN_LEFT)
        self.tcCicParticipante = masked.TextCtrl(self.panelNovoParticipante, -1, mask="")
        self.tcCicParticipante.SetSize((140, -1))
        self.tcCicParticipante.SetPosition((190, 145))
        self.tcCicParticipante.SetEditable(True)
        self.definirCampoCic(None)
        self.tcCicParticipante.SetValue(self.participante.cicParticipante)
        #self.tcCicParticipante.Bind(wx.EVT_CHAR, self.mantemCIC)

        self.stNome = wx.StaticText(self.panelNovoParticipante, -1, u'Nome', pos=(10, 185))
        self.tcNome = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 205), size=(320, -1), style=wx.ALIGN_LEFT)
        self.tcNome.SetMaxLength(50)
        self.tcNome.SetValue(self.participante.nomeParticipante)

        self.stTipoParticipacao = wx.StaticText(self.panelNovoParticipante, -1, u'Tipo Participação', pos=(10, 245))
        self.cbTipoParticipacao = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 265), size=(150, -1), choices=[u'Participante comum', u'Consórcio', u'Consorciado'], style=wx.CB_READONLY)
        self.cbTipoParticipacao.Bind(wx.EVT_COMBOBOX, self.habilitaCnpjConsorcio)
        self.cbTipoParticipacao.SetValue(self.participante.tipoParticipacao)

        self.stCicConsorcio = wx.StaticText(self.panelNovoParticipante, -1, u'CNPJ Consórcio', pos=(190, 245))
        self.tcCicConsorcio = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##.###.###/####-##")
        self.tcCicConsorcio.SetSize((140, -1))
        self.tcCicConsorcio.SetPosition((190, 265))
        self.tcCicConsorcio.SetEditable(False)
        self.tcCicConsorcio.SetValue(self.participante.cicConsorcio)

        self.btnSalvar = wx.Button(self.panelNovoParticipante, -1, u'Alterar', pos=(90, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarParticipante)
        self.btnCancelar = wx.Button(self.panelNovoParticipante, -1, u'Cancelar', pos=(190, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaParticipante)



        #Bind
        self.windowVizualizaParticipante.Bind(wx.EVT_CLOSE, self.quitVizualizaParticipante)

        self.windowVizualizaParticipante.Centre()
        self.windowVizualizaParticipante.Show()

    def quitVizualizaParticipante(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowVizualizaParticipante.Destroy()
    
    def editarParticipante(self, event):

        if self.valida():
            
            self.participante.numeroProcessoLicitatorio = unicode(self.cbNumeroProcesso.GetValue())
            self.participante.cicParticipante = unicode(self.tcCicParticipante.GetValue())
            self.participante.tipoJuridicoParticipante = unicode(self.cbTipoJuridico.GetValue())
            self.participante.nomeParticipante = unicode(self.tcNome.GetValue())
            self.participante.tipoParticipacao = unicode(self.cbTipoParticipacao.GetValue())
            self.participante.cicConsorcio = unicode(self.tcCicConsorcio.GetValue())
            self.participante.participanteConvidado = unicode(self.cbConvidado.GetValue())
            self.participante.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'O participante foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.participante = None
            self.quitVizualizaParticipante(None)

    def excluiParticipante(self, event, idParticipante):

        if idParticipante is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este participante?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.participante = ParticipanteLicitacao.query.filter_by(id=idParticipante).first() 
            self.participante.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Participante excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
        

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Participação de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        
        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereConvenioPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.participanteGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.participanteGeraArquivoListCtrl.InsertColumn(0, u'Num. do Proc. Licit.', width=130)
        self.participanteGeraArquivoListCtrl.InsertColumn(1, u'Nome', width=120)
        self.participanteGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.participanteGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.participanteParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.participanteParaArquivoListCtrl.InsertColumn(0, u'Num. Processo Licit.', width=130)
        self.participanteParaArquivoListCtrl.InsertColumn(1, u'Nome', width=120)
        self.participanteParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.participanteParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereConvenioPorCompetencia(self, event):

        participantes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            participantes = ParticipanteLicitacao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            participantes = Licitacao.query.all()

        self.participanteGeraArquivoListCtrl.DeleteAllItems()

        if not participantes:
            self.message = wx.MessageDialog(None, u'Não existe Licitações para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(participantes) == self.participanteParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for participante in participantes:
                    igual = False
                    if self.participanteParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.participanteGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(participante.numeroProcessoLicitatorio))
                        self.participanteGeraArquivoListCtrl.SetStringItem(index, 1, unicode(participante.nomeParticipante))
                        self.participanteGeraArquivoListCtrl.SetStringItem(index, 2, unicode(participante.id))
                        igual = True

                    else:

                        for x in range(self.participanteParaArquivoListCtrl.GetItemCount()):

                            if participante.nomeParticipante == unicode(self.participanteParaArquivoListCtrl.GetItem(x, 1).GetText()):
                                igual = True

                    if not igual:
                        
                        index = self.participanteGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(participante.numeroProcessoLicitatorio))
                        self.participanteGeraArquivoListCtrl.SetStringItem(index, 1, unicode(participante.nomeParticipante))
                        self.participanteGeraArquivoListCtrl.SetStringItem(index, 2, unicode(participante.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensLicitacaoGeraArquivos(self, event):

        item = self.participanteGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.participanteGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensLicitacaoParaArquivo(self, event):

        item = self.participanteParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.participanteParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os Participantes a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.participanteParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.participanteGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.participanteParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.participanteGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.participanteParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.participanteGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.participanteGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os Participantes a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.participanteGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.participanteParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.participanteGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.participanteParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.participanteGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.participanteParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.participanteParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.participanteParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Participantes para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="PARTICIPANTELICITACAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Participantes de Licitação gerados com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Participantes de Licitação gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.participanteParaArquivoListCtrl.GetItemCount()):

            try:

                idParticipante = int(self.participanteParaArquivoListCtrl.GetItem(x, 2).GetText())
                participante = ParticipanteLicitacao.query.filter_by(id=idParticipante).first()

                f.write(unicode(participante.numeroProcessoLicitatorio.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(self.retiraCaracteresCpfCnpj(participante.cicParticipante).zfill(14)))
                f.write(unicode(self.transformaTipoJuridico(participante.tipoJuridicoParticipante)))
                f.write(unicode(participante.nomeParticipante.ljust(50).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaTipoParticipacao(participante.tipoParticipacao)))
                f.write(unicode(self.retiraCaracteresCpfCnpj(participante.cicConsorcio)))
                f.write(unicode(participante.participanteConvidado))
                f.write(u"\n")

            except:
                return 0

        return 1

    def retiraCaracteresCpfCnpj(self, cic):

        cpf = ""
        for x in cic:
            if x == u'.':
                pass
            elif x == u'-':
                pass
            elif x == u'/':
                pass
            else:
                cpf = cpf+x
        return cpf

    def transformaTipoJuridico(self, tipo):
        if tipo == u'Física':
            return '1'
        elif tipo == u'Jurídica':
            return '2'
        else:
            return '3'

    def transformaTipoParticipacao(self, tipo):

        if tipo == u'Participante comum':
            return '1'
        elif tipo == u'Consórcio':
            return '2'
        else:
            return '3'



        



