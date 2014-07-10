# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_COTACAO_NOVO = 5001
ID_TOOLBAR_COTACAO_EDITAR = 5002
ID_TOOLBAR_COTACAO_EXCLUIR = 5003
ID_TOOLBAR_COTACAO_CRIAR_ARQUIVO = 5004


class WindowCotacao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Cotação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelCotacao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_COTACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova cotação')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_COTACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita cotação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_COTACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui cotação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_COTACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de cotação')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelCotacao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.cotacaoListCtrl = wx.ListCtrl(self.panelCotacao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.cotacaoListCtrl.InsertColumn(0, u'Proc. Licitatório', width=100)
        self.cotacaoListCtrl.InsertColumn(1, u'Sequência do Item', width=200)
        self.cotacaoListCtrl.InsertColumn(2, u'Participante', width=220)
        self.cotacaoListCtrl.InsertColumn(3, u'', width=0)
        self.cotacaoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.cotacaoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.cotacaoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoCotacao, id=ID_TOOLBAR_COTACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaCotacao(event, self.idSelecionado), id=ID_TOOLBAR_COTACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiCotacao(event, self.idSelecionado), id=ID_TOOLBAR_COTACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_COTACAO_CRIAR_ARQUIVO)
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

        self.idSelecionado = self.cotacaoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_COTACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_COTACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_COTACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_COTACAO_CRIAR_ARQUIVO, gerar)

    def novoCotacao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoCotacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 380), pos=(300, 170), title=u'Cotação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoCotacao = wx.Panel(self.windowNovoCotacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoCotacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoCotacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoCotacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)

        wx.StaticBox(self.panelNovoCotacao, -1, pos=(5, 50), size=(480, 140))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoCotacao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoCotacao, -1, pos=(10, 90), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroProcesso.Disable()
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.insereParticipante)

        self.stSequeciaItem = wx.StaticText(self.panelNovoCotacao, -1, u'Seq. Item de Licitação', pos=(190, 70))
        self.cbSequenciaItem = wx.ComboBox(self.panelNovoCotacao, -1, pos=(190, 90), size=(90, -1), choices=[], style=wx.CB_READONLY)
        self.cbSequenciaItem.Disable()

        self.stControleItem = wx.StaticText(self.panelNovoCotacao, -1, u'Controle Item / Lote', pos=(310, 70))
        self.cbControleItem = wx.ComboBox(self.panelNovoCotacao, -1, pos=(310, 90), size=(90, -1), choices=['Item','Lote'], style=wx.CB_READONLY)
        
        self.stCicParticipante = wx.StaticText(self.panelNovoCotacao, -1, u'CPF/CNPJ Participante', pos=(10, 130))
        self.cbCicParticipante = wx.ComboBox(self.panelNovoCotacao, -1, pos=(10, 150), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbCicParticipante.Disable()
        self.cbCicParticipante.Bind(wx.EVT_COMBOBOX, self.insereTipoPessoa)

        self.stTipoPessoa = wx.StaticText(self.panelNovoCotacao, -1, u'Tipo Pessoa', pos=(190, 130))
        self.cbTipoPessoa = wx.ComboBox(self.panelNovoCotacao, -1, pos=(190, 150), size=(100, -1), choices=[u'Física', u'Jurídica', u'Outros'], style=wx.CB_READONLY)
        self.cbTipoPessoa.Disable()

        wx.StaticBox(self.panelNovoCotacao, -1, pos=(5, 190), size=(480, 120))

        self.stSituacaoParticipante = wx.StaticText(self.panelNovoCotacao, -1, u'Situação Participante', pos=(10, 210))
        self.cbSituacaoParticipante = wx.ComboBox(self.panelNovoCotacao, -1, pos=(10, 230), size=(140, -1), choices=[u'Vencedor', u'Perdedor'], style=wx.CB_READONLY)
        
        self.stTipoValor = wx.StaticText(self.panelNovoCotacao, -1, u'Tipo de Valor', pos=(10, 260))
        self.cbTipoValor = wx.ComboBox(self.panelNovoCotacao, -1, pos=(10, 280), size=(140, -1), choices=[u'Espécie', u'Percentual'], style=wx.CB_READONLY)

        self.stValorCotado = wx.StaticText(self.panelNovoCotacao, -1, u'Valor Cotado', pos=(190, 260))
        self.tcValorCotado = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoCotacao, pos=wx.Point(190, 280), style=0, value=0)
        self.tcValorCotado.SetFractionWidth(2)
        self.tcValorCotado.SetGroupChar(u"#")
        self.tcValorCotado.SetDecimalChar(u",")
        self.tcValorCotado.SetGroupChar(u".")
        self.tcValorCotado.SetAllowNegative(False)

        self.stQuantidadeItem = wx.StaticText(self.panelNovoCotacao, -1, u'Quantidade Itens', pos=(350, 260))
        self.tcQuantidadeItem = wx.TextCtrl(self.panelNovoCotacao, -1, pos=(350, 280), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcQuantidadeItem.Bind(wx.EVT_CHAR, self.escapaChar)

        #Bind
        self.windowNovoCotacao.Bind(wx.EVT_CLOSE, self.quitNovoCotacao)
        self.Bind(wx.EVT_CLOSE, self.quit)

        self.btnSalvar = wx.Button(self.panelNovoCotacao, -1, u"Salvar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarCotacao)
        self.btnCancelar = wx.Button(self.panelNovoCotacao, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoCotacao)

        self.windowNovoCotacao.Centre()
        self.windowNovoCotacao.Show()

    def quitNovoCotacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoCotacao.Destroy()

    def insereInCtrList(self, event):

        
            self.cotacaoListCtrl.DeleteAllItems()

            if self.cbCompetenciaForView.GetSelection() != -1:
                cotacoes = Cotacao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

                for cotacao in cotacoes:

                    index = self.cotacaoListCtrl.InsertStringItem(sys.maxint, unicode(cotacao.numeroProcessoLicitatorio))
                    self.cotacaoListCtrl.SetStringItem(index, 1, cotacao.sequenciaItem)
                    self.cotacaoListCtrl.SetStringItem(index, 2, cotacao.cicParticipante)
                    self.cotacaoListCtrl.SetStringItem(index, 3, unicode(cotacao.id))

    def insereNumeroProcesso(self, event):

        self.cbNumeroProcesso.Clear()

        licitacoes = Licitacao.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()

        if not licitacoes:
            self.message = wx.MessageDialog(None, u'Não existe Licitações para a competência selecionada!', 'Info', wx.OK)
            self.message.ShowModal()
            self.cbNumeroProcesso.Disable()

        else:
            for licitacao in licitacoes:

                self.cbNumeroProcesso.Append(unicode(licitacao.numeroProcessoLicitatorio))

            self.cbNumeroProcesso.Enable()

    def insereSequenciaItem(self, event):

        self.cbSequenciaItem.Clear()

        itens = ItemLicitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).all()

        if not itens:
            self.message = wx.MessageDialog(None, u'Não existe Itens de Licitações para a licitação selecionada!', 'Info', wx.OK)
            self.message.ShowModal()
            self.cbSequenciaItem.Disable()

        else:
            for item in itens:

                self.cbSequenciaItem.Append(unicode(item.sequenciaItem))

            self.cbSequenciaItem.Enable()

    def insereParticipante(self, event):

        licitacao = Licitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).first()
        
        if licitacao.modalidadeLicitacao == u'Deserta' or licitacao.modalidadeLicitacao == u'Fracassada':
            
            self.cbSequenciaItem.SetSelection(-1)
            self.cbSequenciaItem.Disable()
            self.cbCicParticipante.SetSelection(-1)
            self.cbCicParticipante.Disable()
            self.cbTipoPessoa.SetSelection(-1)
            self.cbTipoPessoa.Disable()
            self.cbSituacaoParticipante.SetSelection(-1)
            self.cbSituacaoParticipante.Disable()
            self.cbTipoValor.SetSelection(-1)
            self.cbTipoValor.Disable()
            self.tcValorCotado.Disable()
            self.tcValorCotado.SetValue(0.0)
            self.tcQuantidadeItem.Disable()
            self.tcQuantidadeItem.SetValue("")
            self.btnSalvar.Disable()

            self.message = wx.MessageDialog(None, u'Esta licitação não necessita de Cotação.\n Esta licitação pertence a modalidade de licitação: Deserta ou Fracassada.', 'Info', wx.OK)
            self.message.ShowModal()

        else:        
            
            self.cbSequenciaItem.Enable()
            self.cbCicParticipante.Enable()
            self.cbTipoPessoa.Enable()
            self.cbSituacaoParticipante.Enable()
            self.cbTipoValor.Enable()
            self.tcValorCotado.Enable()
            self.tcQuantidadeItem.Enable()
            self.btnSalvar.Enable()

            self.cbCicParticipante.Clear()

            participantes = ParticipanteLicitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).all()

            if not participantes:
                self.message = wx.MessageDialog(None, u'Não existe Participantes de Licitação para a licitação selecionada!', 'Info', wx.OK)
                self.message.ShowModal()
                self.cbCicParticipante.Disable()
            else:
                for participante in participantes:
                    self.cbCicParticipante.Append(unicode(participante.cicParticipante))

                self.cbCicParticipante.Enable()

            self.insereSequenciaItem(None)
            self.insereTipoPessoa(None)

    def insereTipoPessoa(self, event):

        participante = ParticipanteLicitacao.query.filter_by(cicParticipante=self.cbCicParticipante.GetValue()).first()

        if not participante:
            self.cbTipoPessoa.Enable()
            self.cbTipoPessoa.Disable()
            self.cbTipoPessoa.SetSelection(-1)
        else:
            self.cbTipoPessoa.SetValue(participante.tipoJuridicoParticipante)

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

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

        if self.cbSequenciaItem.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Seq. Item de Licitação', 'Info', wx.OK)
            self.cbSequenciaItem.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbControleItem.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Controle Item / Lote', 'Info', wx.OK)
            self.cbControleItem.SetFocus()
            self.message.ShowModal()
            return 0


        if self.cbCicParticipante.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo CPF/CNPJ Participante', 'Info', wx.OK)
            self.cbCicParticipante.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbSituacaoParticipante.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Situação Participante', 'Info', wx.OK)
            self.cbSituacaoParticipante.SetFocus()
            self.message.ShowModal()
            return 0

        
        if self.cbTipoValor.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo de Valor', 'Info', wx.OK)
            self.cbTipoValor.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcQuantidadeItem.GetValue() == '':
            self.message = wx.MessageDialog(None, u'O campo Quantidade Itens deve ser preenchido', 'Info', wx.OK)
            self.tcQuantidadeItem.SetFocus()
            self.message.ShowModal()
            return 0

        cotacoes = Cotacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).all()

        if cotacoes:
            for cotacao in cotacoes:

                if (cotacao.numeroProcessoLicitatorio == self.cbNumeroProcesso.GetValue()) and (cotacao.id != int(self.tcId.GetValue())) and (cotacao.cicParticipante == self.cbCicParticipante.GetValue()) and (cotacao.sequenciaItem == self.cbSequenciaItem.GetValue()):
                    self.message = wx.MessageDialog(None, u'A cotação não pode ser salva! Já existe uma cotação do item e participante indicado!', 'Info', wx.OK)
                    self.cbCicParticipante.SetFocus()
                    self.message.ShowModal()
                    return 0

        return 1

    def salvarCotacao(self, event):

        if self.valida():

            Cotacao(
                tipoValor=unicode(self.cbTipoValor.GetValue()),
                numeroProcessoLicitatorio=unicode(self.cbNumeroProcesso.GetValue()),
                tipoJuridico=unicode(self.cbTipoPessoa.GetValue()),
                cicParticipante=unicode(self.cbCicParticipante.GetValue()),
                sequenciaItem=unicode(self.cbSequenciaItem.GetValue()),
                valorCotado=unicode(self.tcValorCotado.GetValue()),
                situacaoParticipante=unicode(self.cbSituacaoParticipante.GetValue()),
                quantidadeItem=unicode(self.tcQuantidadeItem.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue()),
                controleItem=unicode(self.cbControleItem.GetValue()),
            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Cotação salva com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitNovoCotacao(None)

    def vizualizaCotacao(self, event, idCotacao):

        if idCotacao is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Cotação foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.cotacao = Cotacao.query.filter_by(id=idCotacao).first()

        self.toolBarControler(False, False, False, False)

        self.windowVizualizaCotacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 380), pos=(300, 170), title=u'Cotação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelVizualizaCotacao = wx.Panel(self.windowVizualizaCotacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelVizualizaCotacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.cotacao.id))

        self.stCompetencia = wx.StaticText(self.panelVizualizaCotacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)
        self.cbCompetencia.SetValue(self.cotacao.competencia)

        wx.StaticBox(self.panelVizualizaCotacao, -1, pos=(5, 50), size=(480, 140))

        self.stNumeroProcesso = wx.StaticText(self.panelVizualizaCotacao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(10, 90), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.insereParticipante)
        self.insereNumeroProcesso(None)
        self.cbNumeroProcesso.SetValue(self.cotacao.numeroProcessoLicitatorio)

        self.stSequeciaItem = wx.StaticText(self.panelVizualizaCotacao, -1, u'Seq. Item de Licitação', pos=(190, 70))
        self.cbSequenciaItem = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(190, 90), size=(90, -1), choices=[], style=wx.CB_READONLY)
        
        self.stControleItem = wx.StaticText(self.panelVizualizaCotacao, -1, u'Controle Item / Lote', pos=(310, 70))
        self.cbControleItem = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(310, 90), size=(90, -1), choices=['Item','Lote'], style=wx.CB_READONLY)
        if not self.cotacao.controleItem:
            self.cbControleItem.SetValue('')
        else:
            self.cbControleItem.SetValue(self.cotacao.controleItem)
        
        self.stCicParticipante = wx.StaticText(self.panelVizualizaCotacao, -1, u'CPF/CNPJ Participante', pos=(10, 130))
        self.cbCicParticipante = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(10, 150), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbCicParticipante.Bind(wx.EVT_COMBOBOX, self.insereTipoPessoa)

        self.stTipoPessoa = wx.StaticText(self.panelVizualizaCotacao, -1, u'Tipo Pessoa', pos=(190, 130))
        self.cbTipoPessoa = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(190, 150), size=(100, -1), choices=[u'Física', u'Jurídica', u'Outros'], style=wx.CB_READONLY)

        
        wx.StaticBox(self.panelVizualizaCotacao, -1, pos=(5, 190), size=(480, 120))

        self.stSituacaoParticipante = wx.StaticText(self.panelVizualizaCotacao, -1, u'Situação Participante', pos=(10, 210))
        self.cbSituacaoParticipante = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(10, 230), size=(140, -1), choices=[u'Vencedor', u'Perdedor'], style=wx.CB_READONLY)
        self.cbSituacaoParticipante.SetValue(self.cotacao.situacaoParticipante)
        
        self.stTipoValor = wx.StaticText(self.panelVizualizaCotacao, -1, u'Tipo de Valor', pos=(10, 260))
        self.cbTipoValor = wx.ComboBox(self.panelVizualizaCotacao, -1, pos=(10, 280), size=(140, -1), choices=[u'Espécie', u'Percentual'], style=wx.CB_READONLY)
        self.cbTipoValor.SetValue(self.cotacao.tipoValor)

        self.stValorCotado = wx.StaticText(self.panelVizualizaCotacao, -1, u'Valor Cotado', pos=(190, 260))
        self.tcValorCotado = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelVizualizaCotacao, pos=wx.Point(190, 280), style=0, value=0)
        self.tcValorCotado.SetFractionWidth(2)
        self.tcValorCotado.SetGroupChar(u"#")
        self.tcValorCotado.SetDecimalChar(u",")
        self.tcValorCotado.SetGroupChar(u".")
        self.tcValorCotado.SetAllowNegative(False)
        self.tcValorCotado.SetValue(float(self.cotacao.valorCotado))

        self.stQuantidadeItem = wx.StaticText(self.panelVizualizaCotacao, -1, u'Quantidade Itens', pos=(350, 260))
        self.tcQuantidadeItem = wx.TextCtrl(self.panelVizualizaCotacao, -1, pos=(350, 280), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcQuantidadeItem.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcQuantidadeItem.SetValue(self.cotacao.quantidadeItem)


        #Bind
        self.windowVizualizaCotacao.Bind(wx.EVT_CLOSE, self.quitVizualizaCotacao)

        self.btnSalvar = wx.Button(self.panelVizualizaCotacao, -1, u'Alterar', pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarCotacao)
        self.btnCancelar = wx.Button(self.panelVizualizaCotacao, -1, u'Cancelar', pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaCotacao)

        self.insereParticipante(None)
        self.cbSequenciaItem.SetValue(self.cotacao.sequenciaItem)
        self.cbCicParticipante.SetValue(self.cotacao.cicParticipante)
        self.insereTipoPessoa(None)
        self.cbTipoPessoa.SetValue(self.cotacao.tipoJuridico)

                
        self.windowVizualizaCotacao.Centre()
        self.windowVizualizaCotacao.Show()

    def quitVizualizaCotacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowVizualizaCotacao.Destroy()

    def editarCotacao(self, event):

        if self.valida():

            self.cotacao.tipoValor = unicode(self.cbTipoValor.GetValue())
            self.cotacao.numeroProcessoLicitatorio = unicode(self.cbNumeroProcesso.GetValue())
            self.cotacao.tipoJuridico = unicode(self.cbTipoPessoa.GetValue())
            self.cotacao.cicParticipante = unicode(self.cbCicParticipante.GetValue())
            self.cotacao.sequenciaItem = unicode(self.cbSequenciaItem.GetValue())
            self.cotacao.valorCotado = unicode(self.tcValorCotado.GetValue())
            self.cotacao.situacaoParticipante = unicode(self.cbSituacaoParticipante.GetValue())
            self.cotacao.quantidadeItem = unicode(self.tcQuantidadeItem.GetValue())
            self.cotacao.competencia = unicode(self.cbCompetencia.GetValue())
            self.cotacao.controleItem = unicode(self.cbControleItem.GetValue())
            
            session.commit()
            self.message = wx.MessageDialog(None, u'A Cotação foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.cotacao = None
            self.quitVizualizaCotacao(None)

    def excluiCotacao(self, event, idCotacao):

        if idCotacao is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Cotação?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.cotacao = Cotacao.query.filter_by(id=idCotacao).first()
            self.cotacao.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Cotação excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal() 

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Ctação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)
        
        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereCotacaoPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.cotacaoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.cotacaoGeraArquivoListCtrl.InsertColumn(0, u'Num. Processo Licit.', width=100)
        self.cotacaoGeraArquivoListCtrl.InsertColumn(1, u'Item', width=80)
        self.cotacaoGeraArquivoListCtrl.InsertColumn(2, u'Participante', width=70)
        self.cotacaoGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.cotacaoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensCotacaoGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.cotacaoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.cotacaoParaArquivoListCtrl.InsertColumn(0, u'Num. Processo Licit.', width=100)
        self.cotacaoParaArquivoListCtrl.InsertColumn(1, u'Item', width=80)
        self.cotacaoParaArquivoListCtrl.InsertColumn(2, u'Participante', width=70)
        self.cotacaoParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.cotacaoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensCotacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereCotacaoPorCompetencia(self, event):

        cotacoes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            cotacoes = Cotacao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            cotacoes = Cotacao.query.all()

        self.cotacaoGeraArquivoListCtrl.DeleteAllItems()

        if not cotacoes:
            self.message = wx.MessageDialog(None, u'Não existe Cotações para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(cotacoes) == self.cotacaoParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for cotacao in cotacoes:
                    igual = False
                    if self.cotacaoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.cotacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(cotacao.numeroProcessoLicitatorio))
                        self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(cotacao.sequenciaItem))
                        self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(cotacao.cicParticipante))
                        self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(cotacao.id))
                        igual = True

                    else:

                        for x in range(self.cotacaoParaArquivoListCtrl.GetItemCount()):

                            if cotacao.numeroProcessoLicitatorio == unicode(self.cotacaoParaArquivoListCtrl.GetItem(x, 0).GetText()) and cotacao.sequenciaItem == unicode(self.cotacaoParaArquivoListCtrl.GetItem(x, 1).GetText()) and cotacao.cicParticipante == unicode(self.cotacaoParaArquivoListCtrl.GetItem(x, 2).GetText()):
                                igual = True

                    if not igual:

                        index = self.cotacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(cotacao.numeroProcessoLicitatorio))
                        self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(cotacao.sequenciaItem))
                        self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(cotacao.cicParticipante))
                        self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(cotacao.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensCotacaoGeraArquivos(self, event):

        item = self.cotacaoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.cotacaoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensCotacaoParaArquivo(self, event):

        item = self.cotacaoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.cotacaoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Licitações a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.cotacaoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.cotacaoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.cotacaoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.cotacaoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.cotacaoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.cotacaoGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.cotacaoParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.cotacaoGeraArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.cotacaoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as licitações a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.cotacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.cotacaoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.cotacaoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.cotacaoParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.cotacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(self.cotacaoParaArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.cotacaoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.cotacaoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Cotações para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="COTACAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Cotações gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Cotações gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.cotacaoParaArquivoListCtrl.GetItemCount()):

            try:

                idCotacao = int(self.cotacaoParaArquivoListCtrl.GetItem(x, 3).GetText())
                cotacao = Cotacao.query.filter_by(id=idCotacao).first()

                f.write(unicode(self.transformaTipoValor(cotacao.tipoValor)))
                f.write(unicode(cotacao.numeroProcessoLicitatorio.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaTipoJuridico(cotacao.tipoJuridico)))
                f.write(unicode(self.retiraCaracteresCpfCnpj(cotacao.cicParticipante).zfill(14)))
                f.write(unicode(cotacao.sequenciaItem.zfill(5)))
                
                partes = cotacao.valorCotado.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((cotacao.valorCotado).zfill(16).replace(".", ",")))
                else:
                    f.write(unicode((cotacao.valorCotado+'0').zfill(16).replace(".", ",")))
               
                f.write(unicode(self.transformaSituacao(cotacao.situacaoParticipante)))
                f.write(unicode(cotacao.quantidadeItem.zfill(16)))
                f.write(unicode(cotacao.controleItem.ljust(10).replace("'", "").replace("\"", "")))
                
                f.write(u'\n')

            except:
                return 0

        return 1

    def transformaTipoValor(self, tipo):

        if tipo == u'Espécie':
            return u'E'
        else:
            return u'P'

    def transformaTipoJuridico(self, tipo):
        if tipo == u'Física':
            return '1'
        elif tipo == u'Jurídica':
            return '2'
        else:
            return '3'

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

    def transformaSituacao(self, situacao):
        if situacao == u'Vencedor':
            return u'V'
        else:
            return u'P'
