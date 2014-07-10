# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_ITEM_LICITACAO_NOVO = 6001
ID_TOOLBAR_ITEM_LICITACAO_EDITAR = 6002
ID_TOOLBAR_ITEM_LICITACAO_EXCLUIR = 6003
ID_TOOLBAR_ITEM_LICITACAO_CRIAR_ARQUIVO = 6004


class WindowItemLicitacao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Item de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelItem = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_LICITACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_LICITACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_LICITACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_LICITACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
            u'Outubro', u'Novembro',u'Dezembro']

        self.choicesStatusItem = [u'Homologado', u'Deserto', u'Fracassado', u'Cancelado', u'Anulado/Revogado (Toda a licitação foi anulada)',]

        self.cbCompetenciaForView = wx.ComboBox(self.panelItem, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.itemListCtrl = wx.ListCtrl(self.panelItem, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.itemListCtrl.InsertColumn(0, u'Proc. Licitatório', width=100)
        self.itemListCtrl.InsertColumn(1, u'Sequência Item', width=200)
        self.itemListCtrl.InsertColumn(2, u'Descrição', width=220)
        self.itemListCtrl.InsertColumn(3, u'', width=0)
        self.itemListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.itemListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.itemListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoItem, id=ID_TOOLBAR_ITEM_LICITACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaItem(event, self.idSelecionado), id=ID_TOOLBAR_ITEM_LICITACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiItem(event, self.idSelecionado), id=ID_TOOLBAR_ITEM_LICITACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_ITEM_LICITACAO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_LICITACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_LICITACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_LICITACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_LICITACAO_CRIAR_ARQUIVO, gerar)

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.itemListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def insereInCtrList(self, event):

        self.itemListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            itens = ItemLicitacao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for item in itens:

                index = self.itemListCtrl.InsertStringItem(sys.maxint, unicode(item.numeroProcessoLicitatorio))
                self.itemListCtrl.SetStringItem(index, 1, item.sequenciaItem)
                self.itemListCtrl.SetStringItem(index, 2, item.descricaoItem)
                self.itemListCtrl.SetStringItem(index, 3, unicode(item.id))

    def novoItem(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoItem = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(540, 380), pos=(300, 170), title=u'Item Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoItem = wx.Panel(self.windowNovoItem, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoItem, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoItem, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoItem, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)

        wx.StaticBox(self.panelNovoItem, -1, pos=(5, 50), size=(520, 250))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoItem, -1, u'Número Proc. Licitatório', pos=(10, 65))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoItem, -1, pos=(10, 85), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.verificaLicitacao)

        self.stSequenciaItem = wx.StaticText(self.panelNovoItem, -1, u'Sequência Item', pos=(190, 65))
        self.tcSequenciaItem = wx.TextCtrl(self.panelNovoItem, -1, pos=(190, 85), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcSequenciaItem.SetMaxLength(5)
        self.tcSequenciaItem.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stControleItem = wx.StaticText(self.panelNovoItem, -1, u'Controle Item / Lote', pos=(300, 65))
        self.cbControleItem = wx.ComboBox(self.panelNovoItem, -1, pos=(300, 85), size=(70, -1), choices=['Item','Lote'] ,style=wx.CB_READONLY)
        
        self.stDescricaoItem = wx.StaticText(self.panelNovoItem, -1, u'Descrição do Item', pos=(10, 125))
        self.tcDescricaoItem = wx.TextCtrl(self.panelNovoItem, -1, pos=(10, 145), size=(380, -1), style=wx.ALIGN_LEFT)
        self.tcDescricaoItem.SetMaxLength(300)

        self.stQuantidadeItem = wx.StaticText(self.panelNovoItem, -1, u'Quant. de Itens Solicitados', pos=(10, 185))
        self.tcQuantidadeItem = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoItem, pos=wx.Point(10, 205), style=0, value=0)
        self.tcQuantidadeItem.SetFractionWidth(2)
        self.tcQuantidadeItem.SetGroupChar(u"#")
        self.tcQuantidadeItem.SetDecimalChar(u",")
        self.tcQuantidadeItem.SetGroupChar(u".")
        self.tcQuantidadeItem.SetAllowNegative(False)

        self.stUnidademedida = wx.StaticText(self.panelNovoItem, -1, u'Unidade de Medida', pos=(170, 185))
        self.tcUnidadeMedida = wx.TextCtrl(self.panelNovoItem, -1, pos=(170, 205), size=(70, -1),  style=wx.ALIGN_LEFT)
        self.tcUnidadeMedida.SetMaxLength(30)
                
        self.stStatusItem = wx.StaticText(self.panelNovoItem, -1, u'Status do Item', pos=(280, 185))
        self.cbStatusItem = wx.ComboBox(self.panelNovoItem, -1, pos=(280, 205), size=(240, -1), choices=self.choicesStatusItem, style=wx.CB_READONLY)

        self.stDataAssinatura = wx.StaticText(self.panelNovoItem, -1, u'Data da Assinatura', pos=(10, 245))
        self.tcDataAssinatura = masked.TextCtrl(self.panelNovoItem, -1, mask="##/##/####")
        self.tcDataAssinatura.SetSize((80, -1))
        self.tcDataAssinatura.SetPosition((10, 265))

        self.stDataPublicacao = wx.StaticText(self.panelNovoItem, -1, u'Data da Publicação', pos=(190, 245))
        self.tcDataPublicacao = masked.TextCtrl(self.panelNovoItem, -1, mask='##/##/####')
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((190, 265))

        self.btnSalvar = wx.Button(self.panelNovoItem, -1, u'Salvar', pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarItem)
        self.btnCancelar = wx.Button(self.panelNovoItem, -1, u'Cancelar', pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoItem)

        #Bind
        self.windowNovoItem.Bind(wx.EVT_CLOSE, self.quitNovoItem)

        self.windowNovoItem.Centre()
        self.windowNovoItem.Show()

    def quitNovoItem(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoItem.Destroy()

    def verificaLicitacao(self, event):

        licitacao = Licitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).first()
        
        if licitacao.modalidadeLicitacao == u'Deserta' or licitacao.modalidadeLicitacao == u'Fracassada' or licitacao.modalidadeLicitacao == u'Internacional':
        
            self.tcDataAssinatura.Disable()
            self.tcDataPublicacao.Disable()
            self.tcDataAssinatura.SetValue("")
            self.tcDataPublicacao.SetValue("")
            if event != None:
                self.message = wx.MessageDialog(None, u'Esta licitação não necessita de data de Assinatura e Publicação.\nPeretence a uma das modalidades: Deserta, Fracassada ou Internacional!', 'Info', wx.OK)
                self.message.ShowModal()
            self.licitacaoModalidadeLiberada = 1

        
        else:
        
            self.tcDataAssinatura.Enable()
            self.tcDataPublicacao.Enable()
            self.licitacaoModalidadeLiberada = 0
            

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

        if self.cbControleItem.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Controle Item / Lote', 'Info', wx.OK)
            self.cbControleItem.SetFocus()
            self.message.ShowModal()
            return 0


        if self.tcSequenciaItem.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Sequência Item deve ser preenchido!', 'Info', wx.OK)
            self.tcSequenciaItem.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcDescricaoItem.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Descrição do Item deve ser preenchido!', 'Info', wx.OK)
            self.tcDescricaoItem.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcQuantidadeItem.GetValue() == 0.0:

            self.message = wx.MessageDialog(None, u'O campo Quantidade de Itens Solicitados deve ser diferente de zero!', 'Info', wx.OK)
            self.tcDescricaoItem.SetFocus()
            self.message.ShowModal()
            return 0


        if self.cbStatusItem.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Status Item', 'Info', wx.OK)
            self.cbControleItem.SetFocus()
            self.message.ShowModal()
            return 0
        
        if not self.licitacaoModalidadeLiberada:
            if not self.validateDate(self.tcDataAssinatura.GetValue(), u'Data da Assinatura'):

                self.tcDataAssinatura.SelectAll()
                self.tcDataAssinatura.SetFocus()
                return 0

            if not self.validateDate(self.tcDataPublicacao.GetValue(), u'Data da Publicação'):

                self.tcDataPublicacao.SelectAll()
                self.tcDataPublicacao.SetFocus()
                return 0
        

        itens = ItemLicitacao.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()

        if itens:

            for item in itens:

                if (item.numeroProcessoLicitatorio == self.cbNumeroProcesso.GetValue()) and (unicode(item.sequenciaItem.upper()) == unicode(self.tcSequenciaItem.GetValue().upper())) and (item.id != int(self.tcId.GetValue())):

                    self.message = wx.MessageDialog(None, u'Já existe uma Item de Licitação com o número Sequência Item : '+self.tcSequenciaItem.GetValue()+u'!', 'Info', wx.OK)
                    self.tcSequenciaItem.SelectAll()
                    self.tcSequenciaItem.SetFocus()
                    self.message.ShowModal()
                    return 0

        return 1

    def salvarItem(self, event):

        if self.valida():

            ItemLicitacao(
                numeroProcessoLicitatorio=unicode(self.cbNumeroProcesso.GetValue()),
                sequenciaItem=unicode(self.tcSequenciaItem.GetValue()),
                descricaoItem=unicode(self.tcDescricaoItem.GetValue()),
                quantidadeItem=unicode(self.tcQuantidadeItem.GetValue()),
                dataAssinatura=unicode(self.tcDataAssinatura.GetValue()),
                dataPublicacao=unicode(self.tcDataPublicacao.GetValue()),
                unidadeMedida=unicode(self.tcUnidadeMedida.GetValue()),
                statusItem=unicode(self.cbStatusItem.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue()),
                controleItem=unicode(self.cbControleItem.GetValue()),

            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Item Licitação salva com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.windowNovoItem.Close()

    def vizualizaItem(self, event, idItem):

        if idItem is None:
            self.message = wx.MessageDialog(None, u'Nenhum Item de Licitação foi selecionado! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.item = ItemLicitacao.query.filter_by(id=idItem).first()

        self.windowEditaItem = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(540, 380), pos=(300, 170), title=u'Item Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaItem = wx.Panel(self.windowEditaItem, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelEditaItem, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.item.id))

        self.stCompetencia = wx.StaticText(self.panelEditaItem, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaItem, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)
        self.cbCompetencia.SetValue(self.item.competencia)

        wx.StaticBox(self.panelEditaItem, -1, pos=(5, 50), size=(480, 250))

        self.stNumeroProcesso = wx.StaticText(self.panelEditaItem, -1, u'Número Proc. Licitatório', pos=(10, 65))
        self.cbNumeroProcesso = wx.ComboBox(self.panelEditaItem, -1, pos=(10, 85), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.insereNumeroProcesso(None)
        self.cbNumeroProcesso.SetValue(self.item.numeroProcessoLicitatorio)
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.verificaLicitacao)
        
        self.stSequenciaItem = wx.StaticText(self.panelEditaItem, -1, u'Sequência Item', pos=(190, 65))
        self.tcSequenciaItem = wx.TextCtrl(self.panelEditaItem, -1, pos=(190, 85), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcSequenciaItem.SetMaxLength(5)
        self.tcSequenciaItem.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcSequenciaItem.SetValue(self.item.sequenciaItem)

        self.stControleItem = wx.StaticText(self.panelEditaItem, -1, u'Controle Item / Lote', pos=(300, 65))
        self.cbControleItem = wx.ComboBox(self.panelEditaItem, -1, pos=(300, 85), size=(70, -1), choices=['Item','Lote'] ,style=wx.CB_READONLY)
        if not self.item.controleItem:
            self.cbControleItem.SetValue('')    
        else:
            self.cbControleItem.SetValue(self.item.controleItem)

        self.stDescricaoItem = wx.StaticText(self.panelEditaItem, -1, u'Descrição do Item', pos=(10, 125))
        self.tcDescricaoItem = wx.TextCtrl(self.panelEditaItem, -1, pos=(10, 145), size=(380, -1), style=wx.ALIGN_LEFT)
        self.tcDescricaoItem.SetMaxLength(300)
        self.tcDescricaoItem.SetValue(self.item.descricaoItem)

        self.stQuantidadeItem = wx.StaticText(self.panelEditaItem, -1, u'Quant. de Itens Solicitados', pos=(10, 185))
        self.tcQuantidadeItem = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaItem, pos=wx.Point(10, 205), style=0, value=0)
        self.tcQuantidadeItem.SetFractionWidth(2)
        self.tcQuantidadeItem.SetGroupChar(u"#")
        self.tcQuantidadeItem.SetDecimalChar(u",")
        self.tcQuantidadeItem.SetGroupChar(u".")
        self.tcQuantidadeItem.SetAllowNegative(False)
        self.tcQuantidadeItem.SetValue(float(self.item.quantidadeItem))

        self.stUnidademedida = wx.StaticText(self.panelEditaItem, -1, u'Unidade de Medida', pos=(170, 185))
        self.tcUnidadeMedida = wx.TextCtrl(self.panelEditaItem, -1, pos=(170, 205), size=(70, -1),  style=wx.ALIGN_LEFT)
        self.tcUnidadeMedida.SetMaxLength(30)
        self.tcUnidadeMedida.SetValue(self.item.unidadeMedida)

        self.stStatusItem = wx.StaticText(self.panelEditaItem, -1, u'Status do Item', pos=(280, 185))
        self.cbStatusItem = wx.ComboBox(self.panelEditaItem, -1, pos=(280, 205), size=(240, -1), choices=self.choicesStatusItem, style=wx.CB_READONLY)
        self.cbStatusItem.SetValue(self.item.statusItem)

        self.stDataAssinatura = wx.StaticText(self.panelEditaItem, -1, u'Data da Assinatura', pos=(10, 245))
        self.tcDataAssinatura = masked.TextCtrl(self.panelEditaItem, -1, mask="##/##/####")
        self.tcDataAssinatura.SetSize((80, -1))
        self.tcDataAssinatura.SetPosition((10, 265))
        self.tcDataAssinatura.SetValue(self.item.dataAssinatura)

        self.stDataPublicacao = wx.StaticText(self.panelEditaItem, -1, u'Data da Publicação', pos=(190, 245))
        self.tcDataPublicacao = masked.TextCtrl(self.panelEditaItem, -1, mask='##/##/####')
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((190, 265))
        self.tcDataPublicacao.SetValue(self.item.dataPublicacao)

        self.verificaLicitacao(None)

        self.btnSalvar = wx.Button(self.panelEditaItem, -1, u'Alterar', pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarItem)
        self.btnCancelar = wx.Button(self.panelEditaItem, -1, u'Cancelar', pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaItem)

        #Bind
        self.windowEditaItem.Bind(wx.EVT_CLOSE, self.quitVizualizaItem)

        self.windowEditaItem.Centre()
        self.windowEditaItem.Show()

    def quitVizualizaItem(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaItem.Destroy()

    def editarItem(self, event):

        if self.valida():

            self.item.numeroProcessoLicitatorio = unicode(self.cbNumeroProcesso.GetValue())
            self.item.sequenciaItem = unicode(self.tcSequenciaItem.GetValue())
            self.item.descricaoItem = unicode(self.tcDescricaoItem.GetValue())
            self.item.quantidadeItem = unicode(self.tcQuantidadeItem.GetValue())
            self.item.dataAssinatura = unicode(self.tcDataAssinatura.GetValue())
            self.item.dataPublicacao = unicode(self.tcDataPublicacao.GetValue())
            self.item.unidadeMedida = unicode(self.tcUnidadeMedida.GetValue())
            self.item.statusItem = unicode(self.cbStatusItem.GetValue())
            self.item.competencia = unicode(self.cbCompetencia.GetValue())
            self.item.controleItem = unicode(self.cbControleItem.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'O Item de Licitação foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.item = None
            self.windowEditaItem.Close()

    def excluiItem(self, event, idItem):

        if idItem is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este Item de Licitação?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.item = ItemLicitacao.query.filter_by(id=idItem).first()
            self.item.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Item de Licitação excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Item de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereItemPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.itemGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.itemGeraArquivoListCtrl.InsertColumn(0, u'Proc. Licitatório', width=130)
        self.itemGeraArquivoListCtrl.InsertColumn(1, u'Sequência Item', width=120)
        self.itemGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.itemGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensItemLicitacaoGeraArquivos)

        self.btnIncluiGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.itemParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.itemParaArquivoListCtrl.InsertColumn(0, u'Proc. Licitatório', width=130)
        self.itemParaArquivoListCtrl.InsertColumn(1, u'Sequência Item', width=120)
        self.itemParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.itemParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensItemLicitacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)

        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os Itens de Licitação a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.itemParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.itemGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.itemParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.itemGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.itemParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.itemGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.itemGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os Itens de Licitação a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.itemGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.itemParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.itemGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.itemParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.itemGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.itemParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.itemParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def insereItemPorCompetencia(self, event):

        itens = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            itens = ItemLicitacao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            itens = ItemLicitacao.query.all()

        self.itemGeraArquivoListCtrl.DeleteAllItems()

        if not itens:
            self.message = wx.MessageDialog(None, u'Não existe Itens de Licitação para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(itens) == self.itemParaArquivoListCtrl.GetItemCount():
                pass
            else:

                for item in itens:
                    igual = False
                    if self.itemParaArquivoListCtrl.GetItemCount() == 0:

                        index = self.itemGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.numeroProcessoLicitatorio))
                        self.itemGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.sequenciaItem))
                        self.itemGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.id))
                        igual = True

                    else:

                        for x in range(self.itemParaArquivoListCtrl.GetItemCount()):

                            if item.sequenciaItem == unicode(self.itemParaArquivoListCtrl.GetItem(x, 1).GetText()):
                                igual = True
                    if not igual:
                        index = self.itemGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.numeroProcessoLicitatorio))
                        self.itemGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.sequenciaItem))
                        self.itemGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensItemLicitacaoGeraArquivos(self, event):

        item = self.itemGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.itemGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensItemLicitacaoParaArquivo(self, event):

        item = self.itemParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.itemParaArquivoListCtrl.GetNextSelected(item)

    def geraArquivoDialog(self, event):

        if self.itemParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Itens de Licitações para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="ITEMLICITACAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Itens de Licitação gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Itens de Licitação gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.itemParaArquivoListCtrl.GetItemCount()):

            try:
                idItem = int(self.itemParaArquivoListCtrl.GetItem(x, 2).GetText())
                item = ItemLicitacao.query.filter_by(id=idItem).first()

                f.write(unicode(item.numeroProcessoLicitatorio.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.sequenciaItem.zfill(5)))
                f.write(unicode(item.descricaoItem.ljust(300).replace("'", "").replace("\"", "")))
                
                partes = item.quantidadeItem.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((item.quantidadeItem).zfill(16).replace(".", ",")))
                
                else:
                    f.write(unicode((item.quantidadeItem+'0').zfill(16).replace(".", ",")))

                f.write(unicode(self.transformaData(item.dataAssinatura)))
                f.write(unicode(self.transformaData(item.dataPublicacao)))
                
                f.write(unicode(item.unidadeMedida.ljust(30).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaStatus(item.statusItem)).zfill(2))

                f.write(unicode(item.controleItem.ljust(10).replace("'", "").replace("\"", "")))
                                
                f.write(u'\n')
            except:
                return 0

        return 1

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]

    def transformaStatus(self, status):

        if status == u'Homologado':
            return "1"
        elif status == u'Deserto':
            return "2"
        elif status == u'Fracassado':
            return "3"
        elif status == u'Cancelado':
            return "4"
        else:
            return "5"