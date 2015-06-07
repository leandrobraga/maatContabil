# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_ITEM_ATA_NOVO = 5001
ID_TOOLBAR_ITEM_ATA_EDITAR = 5002
ID_TOOLBAR_ITEM_ATA_EXCLUIR = 5003
ID_TOOLBAR_ITEM_ATA_CRIAR_ARQUIVO = 5004


class WindowItemAta(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Item Adesão de Ata", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelItemAta = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_ATA_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo Item de adesão de Ata')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_ATA_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Item de adesão de Ata selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_ATA_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Item de adesão de Ata selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_ITEM_ATA_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de Item de adesão de Ata')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelItemAta, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.itemAtaListCtrl = wx.ListCtrl(self.panelItemAta, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.itemAtaListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.itemAtaListCtrl.InsertColumn(1, u'Número da Ata', width=200)
        self.itemAtaListCtrl.InsertColumn(2, u'Descrição do Item', width=220)
        self.itemAtaListCtrl.InsertColumn(3, u'', width=0)
        self.itemAtaListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.itemAtaListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.itemAtaListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoItemAta, id=ID_TOOLBAR_ITEM_ATA_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaItemAta(event, self.idSelecionado), id=ID_TOOLBAR_ITEM_ATA_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiItemAta(event, self.idSelecionado), id=ID_TOOLBAR_ITEM_ATA_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_ITEM_ATA_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_ATA_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_ATA_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_ATA_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_ITEM_ATA_CRIAR_ARQUIVO, gerar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.itemAtaListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def insereInCtrList(self, event):

        self.itemAtaListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            itens = ItemAta.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for item in itens:

                index = self.itemAtaListCtrl.InsertStringItem(sys.maxint, unicode(item.processoCompra))
                self.itemAtaListCtrl.SetStringItem(index, 1, item.numeroAta)
                self.itemAtaListCtrl.SetStringItem(index, 2, item.descricaoItem)
                self.itemAtaListCtrl.SetStringItem(index, 3, unicode(item.id))

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def novoItemAta(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoItemAta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(470, 390), pos=(300, 170), title=u'Novo - Item Adesão de Ata', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoItemAta = wx.Panel(self.windowNovoItemAta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoItemAta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoItemAta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoItemAta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        
        wx.StaticBox(self.panelNovoItemAta, -1, pos=(5, 50), size=(450, 260))

        self.stProcessoCompra = wx.StaticText(self.panelNovoItemAta, -1, u'Número do Proc. de Compra', pos=(10, 70))
        self.tcProcessoCompra = wx.TextCtrl(self.panelNovoItemAta, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoCompra.SetMaxLength(18)

        self.stNumeroAta = wx.StaticText(self.panelNovoItemAta, -1, u'Número da Ata', pos=(200, 70))
        self.tcNumeroAta = wx.TextCtrl(self.panelNovoItemAta, -1, pos=(200, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroAta.SetMaxLength(18)

        self.stDescricaoItem = wx.StaticText(self.panelNovoItemAta, -1, u'Descrição do Item', pos=(10, 130))
        self.tcDescricaoItem = wx.TextCtrl(self.panelNovoItemAta, -1, pos=(10, 150), size=(300, -1), style=wx.ALIGN_LEFT)
        self.tcDescricaoItem.SetMaxLength(300) 

        self.stQuantidade = wx.StaticText(self.panelNovoItemAta, -1, u'Quantidade', pos=(325, 130))
        self.tcQuantidade = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoItemAta, pos=wx.Point(325, 150), style=0, value=0)
        self.tcQuantidade.SetFractionWidth(2)
        self.tcQuantidade.SetGroupChar(u"#")
        self.tcQuantidade.SetDecimalChar(u",")
        self.tcQuantidade.SetGroupChar(u".")
        self.tcQuantidade.SetAllowNegative(False)
        
        self.stSequenciaItem = wx.StaticText(self.panelNovoItemAta, -1, u'Sequência Item', pos=(10, 190))
        self.tcSequenciaItem = wx.TextCtrl(self.panelNovoItemAta, -1, pos=(10, 210), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcSequenciaItem.SetMaxLength(5)
        self.tcSequenciaItem.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stValorItem = wx.StaticText(self.panelNovoItemAta, -1, u'Valor', pos=(140, 190))
        self.tcValorItem = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoItemAta, pos=wx.Point(140, 210), style=0, value=0)
        self.tcValorItem.SetFractionWidth(2)
        self.tcValorItem.SetGroupChar(u"#")
        self.tcValorItem.SetDecimalChar(u",")
        self.tcValorItem.SetGroupChar(u".")
        self.tcValorItem.SetAllowNegative(False)
        
        self.stUnidadeMedida = wx.StaticText(self.panelNovoItemAta, -1, u'Unidade de Medida', pos=(320, 190))
        self.tcUnidadeMedida = wx.TextCtrl(self.panelNovoItemAta, -1, pos=(320, 210), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcUnidadeMedida.SetMaxLength(30)

        self.stControleItem = wx.StaticText(self.panelNovoItemAta, -1, u'Controle Item / Lote', pos=(10, 250))
        self.cbControleItem = wx.ComboBox(self.panelNovoItemAta, -1, pos=(10, 270), size=(70, -1), choices=['Item','Lote'], style=wx.CB_READONLY)
        
        self.btnSalvar = wx.Button(self.panelNovoItemAta, -1, u"Salvar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarItemAta)
        self.btnCancelar = wx.Button(self.panelNovoItemAta, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoItemAta)      

        #Bind
        self.windowNovoItemAta.Bind(wx.EVT_CLOSE, self.quitNovoItemAta)

        self.windowNovoItemAta.Centre()
        self.windowNovoItemAta.Show()

    def quitNovoItemAta(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoItemAta.Destroy()

    def vizualizaItemAta(self,event,idItemAta):
        
        if idItemAta is None:
            self.message = wx.MessageDialog(None, u'Nenhum Item de Adesão de Ata foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.item = ItemAta.query.filter_by(id=idItemAta).first()

        self.windowEditaItemAta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(470, 390), pos=(300, 170), title=u'Editar2 - Item Adesão de Ata', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaItemAta = wx.Panel(self.windowEditaItemAta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelEditaItemAta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.item.id))

        self.stCompetencia = wx.StaticText(self.panelEditaItemAta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaItemAta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.item.competencia)

        wx.StaticBox(self.panelEditaItemAta, -1, pos=(5, 50), size=(450, 260))

        self.stProcessoCompra = wx.StaticText(self.panelEditaItemAta, -1, u'Número do Proc. de Compra', pos=(10, 70))
        self.tcProcessoCompra = wx.TextCtrl(self.panelEditaItemAta, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoCompra.SetMaxLength(18)
        self.tcProcessoCompra.SetValue(self.item.processoCompra)

        self.stNumeroAta = wx.StaticText(self.panelEditaItemAta, -1, u'Número da Ata', pos=(200, 70))
        self.tcNumeroAta = wx.TextCtrl(self.panelEditaItemAta, -1, pos=(200, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroAta.SetMaxLength(18)
        self.tcNumeroAta.SetValue(self.item.numeroAta)

        self.stDescricaoItem = wx.StaticText(self.panelEditaItemAta, -1, u'Descrição do Item', pos=(10, 130))
        self.tcDescricaoItem = wx.TextCtrl(self.panelEditaItemAta, -1, pos=(10, 150), size=(300, -1), style=wx.ALIGN_LEFT)
        self.tcDescricaoItem.SetMaxLength(300)
        self.tcDescricaoItem.SetValue(self.item.descricaoItem)

        self.stQuantidade = wx.StaticText(self.panelEditaItemAta, -1, u'Quantidade', pos=(325, 130))
        self.tcQuantidade = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaItemAta, pos=wx.Point(325, 150), style=0, value=0)
        self.tcQuantidade.SetFractionWidth(2)
        self.tcQuantidade.SetGroupChar(u"#")
        self.tcQuantidade.SetDecimalChar(u",")
        self.tcQuantidade.SetGroupChar(u".")
        self.tcQuantidade.SetAllowNegative(False)
        self.tcQuantidade.SetValue(float(self.item.quantidade)) 
        
        self.stSequenciaItem = wx.StaticText(self.panelEditaItemAta, -1, u'Sequência Item', pos=(10, 190))
        self.tcSequenciaItem = wx.TextCtrl(self.panelEditaItemAta, -1, pos=(10, 210), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcSequenciaItem.SetMaxLength(5)
        self.tcSequenciaItem.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcSequenciaItem.SetValue(self.item.sequenciaItem)

        
        self.stValorItem = wx.StaticText(self.panelEditaItemAta, -1, u'Valor', pos=(140, 190))
        self.tcValorItem = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaItemAta,pos=wx.Point(140, 210), style=0, value=0)
        self.tcValorItem.SetFractionWidth(2)
        self.tcValorItem.SetGroupChar(u"#")
        self.tcValorItem.SetDecimalChar(u",")
        self.tcValorItem.SetGroupChar(u".")
        self.tcValorItem.SetAllowNegative(False)
        self.tcValorItem.SetValue(float(self.item.valorItem))
        
        self.stUnidadeMedida = wx.StaticText(self.panelEditaItemAta, -1, u'Unidade de Medida', pos=(320, 190))
        self.tcUnidadeMedida = wx.TextCtrl(self.panelEditaItemAta, -1, pos=(320, 210), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcUnidadeMedida.SetMaxLength(30)
        self.tcUnidadeMedida.SetValue(self.item.unidadeMedida)

        self.stControleItem = wx.StaticText(self.panelEditaItemAta, -1, u'Controle Item / Lote', pos=(10, 250))
        self.cbControleItem = wx.ComboBox(self.panelEditaItemAta, -1, pos=(10, 270), size=(70, -1), choices=['Item','Lote'], style=wx.CB_READONLY)
        self.cbControleItem.SetValue(self.item.controleItem)
                
        self.btnSalvar = wx.Button(self.panelEditaItemAta, -1, u"Alterar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarItemAta)
        self.btnCancelar = wx.Button(self.panelEditaItemAta, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitItemAtaEdita)      

        #Bind
        self.windowEditaItemAta.Bind(wx.EVT_CLOSE, self.quitItemAtaEdita)

        self.windowEditaItemAta.Centre()
        self.windowEditaItemAta.Show()

    def quitItemAtaEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaItemAta.Destroy()

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

            self.message = wx.MessageDialog(None, u'O campo Número da Ata deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroAta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcDescricaoItem.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Descrição do Item deve ser preenchido!', 'Info', wx.OK)
            self.tcDescricaoItem.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcSequenciaItem.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Sequência Item  deve ser preenchido!', 'Info', wx.OK)
            self.tcSequenciaItem.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcQuantidade.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Quantidade deve ser preenchido!', 'Info', wx.OK)
            self.tcQuantidade.SetFocus()
            self.message.ShowModal()
            return 0

        
        if self.tcUnidadeMedida.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Unidade Medida  deve ser preenchido!', 'Info', wx.OK)
            self.tcUnidadeMedida.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbControleItem.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Controle Item / Lote', 'Info', wx.OK)
            self.cbControleItem.SetFocus()
            self.message.ShowModal()
            return 0



        return 1

    def salvarItemAta(self, event):

        if self.valida():

            try:
                ItemAta(processoCompra=unicode(self.tcProcessoCompra.GetValue()),
                        numeroAta=unicode(self.tcNumeroAta.GetValue()),
                        quantidade=unicode(self.tcQuantidade.GetValue()),
                        sequenciaItem=unicode(self.tcSequenciaItem.GetValue()),
                        valorItem=unicode(self.tcValorItem.GetValue()),
                        unidadeMedida=unicode(self.tcUnidadeMedida.GetValue()),
                        descricaoItem=unicode(self.tcDescricaoItem.GetValue()),
                        controleItem=unicode(self.cbControleItem.GetValue()),
                        competencia=unicode(self.cbCompetencia.GetValue()), 
                        )

                session.commit()
                self.message = wx.MessageDialog(None, u'Item de Adesão de Ata salvo com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoItemAta.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoItemAta.Close()

    def editarItemAta(self, event):

        if self.valida():

            self.item.processoCompra=unicode(self.tcProcessoCompra.GetValue())
            self.item.numeroAta=unicode(self.tcNumeroAta.GetValue())
            self.item.quantidade=unicode(self.tcQuantidade.GetValue())
            self.item.sequenciaItem=unicode(self.tcSequenciaItem.GetValue())
            self.item.valorItem=unicode(self.tcValorItem.GetValue())
            self.item.unidadeMedida=unicode(self.tcUnidadeMedida.GetValue())
            self.item.descricaoItem=unicode(self.tcDescricaoItem.GetValue())
            self.item.controleItem = unicode(self.cbControleItem.GetValue())
            self.item.competencia=unicode(self.cbCompetencia.GetValue()) 

            session.commit()
            self.message = wx.MessageDialog(None, u'O Item de Adesão de Ata foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.item = None
            self.windowEditaItemAta.Close()

    def excluiItemAta(self, event, idItemAta):

        if idItemAta is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este Item de Adesão de Ata?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.item = ItemAta.query.filter_by(id=idItemAta).first()
            self.item.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Item de Adesão de Ata excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(710, 470), pos=(300, 170), title=u"Gerar Arquivo de Item de Adesão de Ata", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
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
        self.itemAtaGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(300, 300), style=wx.LC_REPORT)
        self.itemAtaGeraArquivoListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.itemAtaGeraArquivoListCtrl.InsertColumn(1, u'Número da Ata', width=80)
        self.itemAtaGeraArquivoListCtrl.InsertColumn(2, u'Descrição do Item', width=80)
        self.itemAtaGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.itemAtaGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(320, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(320, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.itemAtaParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(300, 300), style=wx.LC_REPORT)
        self.itemAtaParaArquivoListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.itemAtaParaArquivoListCtrl.InsertColumn(1, u'Número da Ata', width=80)
        self.itemAtaParaArquivoListCtrl.InsertColumn(2, u'Descrição do Item', width=80)
        self.itemAtaParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.itemAtaParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def inserePorCompetencia(self, event):

        itens = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            itens = ItemAta.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            itens = ItemAta.query.all()

        self.itemAtaGeraArquivoListCtrl.DeleteAllItems()

        if not itens:
            self.message = wx.MessageDialog(None, u'Não existe Item Adesão de Ata para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(itens) == self.itemAtaParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for item in itens:
                    igual = False
                    if self.itemAtaParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.itemAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.processoCompra))
                        self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.numeroAta))
                        self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.descricaoItem))
                        self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 3, unicode(item.id))
                        igual = True

                    else:

                        for x in range(self.itemAtaParaArquivoListCtrl.GetItemCount()):

                            if item.processoCompra == unicode(self.itemAtaParaArquivoListCtrl.GetItem(x, 0).GetText()) and item.numeroAta == unicode(self.itemAtaParaArquivoListCtrl.GetItem(x, 1).GetText()) and item.descricaoItem == unicode(self.itemAtaParaArquivoListCtrl.GetItem(x, 2).GetText()):
                                igual = True

                    if not igual:

                        index = self.itemAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.processoCompra))
                        self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.numeroAta))
                        self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.descricaoItem))
                        self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 3, unicode(item.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensGeraArquivos(self, event):

        item = self.itemAtaGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.itemAtaGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensParaArquivo(self, event):

        item = self.itemAtaParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.itemAtaParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Item Adessão de Ata  a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.itemAtaParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.itemAtaGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.itemAtaParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.itemAtaGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.itemAtaParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.itemAtaGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.itemAtaParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.itemAtaGeraArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.itemAtaGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as Item Adessão de Ata a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.itemAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.itemAtaParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.itemAtaParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.itemAtaParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.itemAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.itemAtaParaArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.itemAtaParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.itemAtaParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Itens Adessão de Ata para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="ITEMADESAOATA.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Item Adessão de Ata gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Item Adessão de Ata gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.itemAtaParaArquivoListCtrl.GetItemCount()):

            #try:

                idItemAta = int(self.itemAtaParaArquivoListCtrl.GetItem(x, 3).GetText())
                item = ItemAta.query.filter_by(id=idItemAta).first()

                f.write(unicode(item.processoCompra.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.numeroAta.ljust(18).replace("'", "").replace("\"", "")))
                
                partes = item.quantidade.split('.')
                
                if len(partes[1])> 1:
                    f.write(unicode((item.quantidade).zfill(16).replace(".", ",")))
                else:
                    f.write(unicode((item.quantidade+'0').zfill(16).replace(".", ",")))

                f.write(unicode(item.sequenciaItem.zfill(5)))
                
                partes = item.valorItem.split('.')
                
                if len(partes[1])> 1:
                    f.write(unicode((item.valorItem).zfill(16).replace(".", ",")))
                else:
                    f.write(unicode((item.valorItem+'0').zfill(16).replace(".", ",")))  
                
                f.write(unicode(item.unidadeMedida.ljust(30).replace("'", "").replace("\"", "")))
                f.write(unicode(item.descricaoItem.ljust(300).replace("'", "").replace("\"", "")))
                f.write(unicode(item.controleItem.ljust(10).replace("'", "").replace("\"", "")))                
                f.write(u'\n')

            #except:

                #return 0
        return 1
