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

ID_TOOLBAR_LICITACAO_ATA_NOVO = 5001
ID_TOOLBAR_LICITACAO_ATA_EDITAR = 5002
ID_TOOLBAR_LICITACAO_ATA_EXCLUIR = 5003
ID_TOOLBAR_LICITACAO_ATA_CRIAR_ARQUIVO = 5004


class WindowLicitacaoAta(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Adesão Ata de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelLicitacaoAta = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_ATA_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo Ata de Licitação')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_ATA_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Ata de Licitação selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_ATA_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Ata de Licitação selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_ATA_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de Ata de Licitação')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.choicesTipoAdesoes = [u'Adesão ata própria (Participante)', u'Adesão ata externa (Carona)']

        self.cbCompetenciaForView = wx.ComboBox(self.panelLicitacaoAta, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.licitacaoAtaListCtrl = wx.ListCtrl(self.panelLicitacaoAta, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.licitacaoAtaListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.licitacaoAtaListCtrl.InsertColumn(1, u'Número da Ata', width=200)
        self.licitacaoAtaListCtrl.InsertColumn(2, u'Tipo de Adesão', width=220)
        self.licitacaoAtaListCtrl.InsertColumn(3, u'', width=0)
        self.licitacaoAtaListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.licitacaoAtaListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.licitacaoAtaListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoLicitacaoAta, id=ID_TOOLBAR_LICITACAO_ATA_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaLicitacaoAta(event, self.idSelecionado), id=ID_TOOLBAR_LICITACAO_ATA_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiLicitacaoAta(event, self.idSelecionado), id=ID_TOOLBAR_LICITACAO_ATA_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_LICITACAO_ATA_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_ATA_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_ATA_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_ATA_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_ATA_CRIAR_ARQUIVO, gerar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.licitacaoAtaListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def insereInCtrList(self, event):

        self.licitacaoAtaListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            licitacoes = LicitacaoAta.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for licitacao in licitacoes:

                index = self.licitacaoAtaListCtrl.InsertStringItem(sys.maxint, unicode(licitacao.processoCompra))
                self.licitacaoAtaListCtrl.SetStringItem(index, 1, licitacao.numeroAta)
                self.licitacaoAtaListCtrl.SetStringItem(index, 2, licitacao.tipoAdesao)
                self.licitacaoAtaListCtrl.SetStringItem(index, 3, unicode(licitacao.id))

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def novoLicitacaoAta(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoLicitacaoAta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(440, 370), pos=(300, 170), title=u'Novo - Adesão Ata de Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoLicitacaoAta = wx.Panel(self.windowNovoLicitacaoAta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoLicitacaoAta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        
        wx.StaticBox(self.panelNovoLicitacaoAta, -1, pos=(5, 50), size=(420, 250))

        self.stProcessoCompra = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número do Proc. de Compra', pos=(10, 70))
        self.tcProcessoCompra = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoCompra.SetMaxLength(18)

        self.stNumeroAta = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número da Ata', pos=(200, 70))
        self.tcNumeroAta = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(200, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroAta.SetMaxLength(18)

        self.stNumeroLicitacao = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número Processo Licitatório', pos=(10, 130))
        self.tcNumeroLicitacao = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(10, 150), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroLicitacao.SetMaxLength(18) 
        
        self.stNumeroDOE = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número Diário Oficial', pos=(170, 130))
        self.tcNumeroDOE = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(170, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroDOE.SetMaxLength(6)
        
        self.stPublicacaoDOE = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Data Publicação D. Oficial', pos=(290, 130))
        self.tcPublicacaoDOE = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##/##/####")
        self.tcPublicacaoDOE.SetSize((80, -1))
        self.tcPublicacaoDOE.SetPosition((290, 150))

        self.stDataValidade = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Data de Validade da Ata', pos=(10, 190))
        self.tcDataValidade = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##/##/####")
        self.tcDataValidade.SetSize((80, -1))
        self.tcDataValidade.SetPosition((10, 210))

        self.stDataAdesao = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Data de Adesão', pos=(170, 190))
        self.tcDataAdesao = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##/##/####")
        self.tcDataAdesao.SetSize((80, -1))
        self.tcDataAdesao.SetPosition((170, 210))

        self.tcTipoAdesao = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Tipo de Adesão', pos=(10, 250))
        self.cbTipoAdesao = wx.ComboBox(self.panelNovoLicitacaoAta, -1, size=(200, -1), pos=(10, 270), choices=self.choicesTipoAdesoes, style= wx.CB_READONLY)

        self.stCNPJ = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'CNPJ do Órgão Gerenciador', pos=(230, 250))
        self.tcCnpjOrgao = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##.###.###/####-##")
        self.tcCnpjOrgao.SetSize((140, -1))
        self.tcCnpjOrgao.SetPosition((230, 270))
       
        self.btnSalvar = wx.Button(self.panelNovoLicitacaoAta, -1, u"Salvar", pos=(150, 315))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarLicitacaoAta)
        self.btnCancelar = wx.Button(self.panelNovoLicitacaoAta, -1, u"Cancelar", pos=(250, 315))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoLicitacaoAta)      

        #Bind
        self.windowNovoLicitacaoAta.Bind(wx.EVT_CLOSE, self.quitNovoLicitacaoAta)

        self.windowNovoLicitacaoAta.Centre()
        self.windowNovoLicitacaoAta.Show()

    def quitNovoLicitacaoAta(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoLicitacaoAta.Destroy()

    def vizualizaLicitacaoAta(self,event,idLicitacaoAta):
        
        if idLicitacaoAta is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Adesão Ata de Licitação foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.licitacao = LicitacaoAta.query.filter_by(id=idLicitacaoAta).first()

        self.windowEditaLicitacaoAta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(440, 370), pos=(300, 170), title=u'Editar - Adesão Ata de Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoLicitacaoAta = wx.Panel(self.windowEditaLicitacaoAta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.licitacao.id))

        self.stCompetencia = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoLicitacaoAta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.licitacao.competencia)

        wx.StaticBox(self.panelNovoLicitacaoAta, -1, pos=(5, 50), size=(420, 250))

        self.stProcessoCompra = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número do Proc. de Compra', pos=(10, 70))
        self.tcProcessoCompra = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(10, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcProcessoCompra.SetMaxLength(18)
        self.tcProcessoCompra.SetValue(self.licitacao.processoCompra)

        self.stNumeroAta = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número da Ata', pos=(200, 70))
        self.tcNumeroAta = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(200, 90), size=(140, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroAta.SetMaxLength(18)
        self.tcNumeroAta.SetValue(self.licitacao.numeroAta)

        self.stNumeroLicitacao = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número Processo Licitatório', pos=(10, 130))
        self.tcNumeroLicitacao = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(10, 150), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroLicitacao.SetMaxLength(18)
        self.tcNumeroLicitacao.SetValue(self.licitacao.numeroLicitacao) 
        
        self.stNumeroDOE = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Número Diário Oficial', pos=(170, 130))
        self.tcNumeroDOE = wx.TextCtrl(self.panelNovoLicitacaoAta, -1, pos=(170, 150), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroDOE.SetMaxLength(6)
        self.tcNumeroDOE.SetValue(self.licitacao.numeroDOE)
        
        self.stPublicacaoDOE = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Data Publicação D. Oficial', pos=(290, 130))
        self.tcPublicacaoDOE = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##/##/####")
        self.tcPublicacaoDOE.SetSize((80, -1))
        self.tcPublicacaoDOE.SetPosition((290, 150))
        self.tcPublicacaoDOE.SetValue(self.licitacao.publicacaoDOE)

        self.stDataValidade = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Data de Validade da Ata', pos=(10, 190))
        self.tcDataValidade = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##/##/####")
        self.tcDataValidade.SetSize((80, -1))
        self.tcDataValidade.SetPosition((10, 210))
        self.tcDataValidade.SetValue(self.licitacao.dataValidade)

        self.stDataAdesao = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Data de Adesão', pos=(170, 190))
        self.tcDataAdesao = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##/##/####")
        self.tcDataAdesao.SetSize((80, -1))
        self.tcDataAdesao.SetPosition((170, 210))
        self.tcDataAdesao.SetValue(self.licitacao.dataAdesao)

        self.tcTipoAdesao = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'Tipo de Adesão', pos=(10, 250))
        self.cbTipoAdesao = wx.ComboBox(self.panelNovoLicitacaoAta, -1, size=(200, -1), pos=(10, 270), choices=self.choicesTipoAdesoes, style= wx.CB_READONLY)
        self.cbTipoAdesao.SetValue(self.licitacao.tipoAdesao)

        self.stCNPJ = wx.StaticText(self.panelNovoLicitacaoAta, -1, u'CNPJ do Órgão Gerenciador', pos=(230, 250))
        self.tcCnpjOrgao = masked.TextCtrl(self.panelNovoLicitacaoAta, -1, mask="##.###.###/####-##")
        self.tcCnpjOrgao.SetSize((140, -1))
        self.tcCnpjOrgao.SetPosition((230, 270))
        self.tcCnpjOrgao.SetValue(self.licitacao.cnpjOrgao)
        
        self.btnSalvar = wx.Button(self.panelNovoLicitacaoAta, -1, u"Alterar", pos=(150, 315))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarLicitacaoAta)
        self.btnCancelar = wx.Button(self.panelNovoLicitacaoAta, -1, u"Cancelar", pos=(250, 315))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitLicitacaoAtaEdita)      

        #Bind
        self.windowEditaLicitacaoAta.Bind(wx.EVT_CLOSE, self.quitLicitacaoAtaEdita)

        self.windowEditaLicitacaoAta.Centre()
        self.windowEditaLicitacaoAta.Show()

    def quitLicitacaoAtaEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaLicitacaoAta.Destroy()

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

        if self.tcNumeroLicitacao.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número Processo Licitatório deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroLicitacao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroDOE.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número Diário Oficial  deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroDOE.SetFocus()
            self.message.ShowModal()
            return 0

        
        if not self.validateDate(self.tcPublicacaoDOE.GetValue(), u"Data Publicação D. Oficial") :

            self.tcPublicacaoDOE.SelectAll()
            self.tcPublicacaoDOE.SetFocus()
            return 0

        if not self.validateDate(self.tcDataValidade.GetValue(), u"Data de Validade da Ata") :

            self.tcDataValidade.SelectAll()
            self.tcDataValidade.SetFocus()
            return 0

        if not self.validateDate(self.tcDataAdesao.GetValue(), u"Data de Adesão") :

            self.tcDataValidade.SelectAll()
            self.tcDataAdesao.SetFocus()
            return 0
        
        if self.cbTipoAdesao.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo de Adesão!', 'Info', wx.OK)
            self.cbTipoAdesao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCnpjOrgao.GetValue() == "  .   .   /    -  ":
            self.message = wx.MessageDialog(None, u'O campo CNPJ deve ser preenchido', 'Info', wx.OK)
            self.tcCnpjOrgao.SelectAll()
            self.tcCnpjOrgao.SetFocus()
            self.message.ShowModal()
            return 0

        if not burocracia.CNPJ(self.tcCnpjOrgao.GetValue()).isValid():
            self.message = wx.MessageDialog(None, u'CNPJ inválido!', 'Info', wx.OK)
            self.tcCnpjOrgao.SelectAll()
            self.tcCnpjOrgao.SetFocus()
            self.message.ShowModal()
            return 0

        return 1

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

    def salvarLicitacaoAta(self, event):

        if self.valida():

            try:
                LicitacaoAta(processoCompra=unicode(self.tcProcessoCompra.GetValue()),
                        numeroAta=unicode(self.tcNumeroAta.GetValue()),
                        numeroLicitacao=unicode(self.tcNumeroLicitacao.GetValue()),
                        publicacaoDOE=unicode(self.tcPublicacaoDOE.GetValue()),
                        dataValidade=unicode(self.tcDataValidade.GetValue()),
                        numeroDOE=unicode(self.tcNumeroDOE.GetValue()),
                        dataAdesao=unicode(self.tcDataAdesao.GetValue()),
                        tipoAdesao=unicode(self.cbTipoAdesao.GetValue()),
                        cnpjOrgao=unicode(self.tcCnpjOrgao.GetValue()),
                        competencia=unicode(self.cbCompetencia.GetValue()), 
                        )

                session.commit()
                self.message = wx.MessageDialog(None, u'Adesão Ata de Licitação salvo com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoLicitacaoAta.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoLicitacaoAta.Close()

    def editarLicitacaoAta(self, event):

        if self.valida():

            self.licitacao.processoCompra=unicode(self.tcProcessoCompra.GetValue())
            self.licitacao.numeroAta=unicode(self.tcNumeroAta.GetValue())
            self.licitacao.numeroLicitacao=unicode(self.tcNumeroLicitacao.GetValue())
            self.licitacao.publicacaoDOE=unicode(self.tcPublicacaoDOE.GetValue())
            self.licitacao.dataValidade=unicode(self.tcDataValidade.GetValue())
            self.licitacao.numeroDOE=unicode(self.tcNumeroDOE.GetValue())
            self.licitacao.dataAdesao=unicode(self.tcDataAdesao.GetValue())
            self.licitacao.tipoAdesao=unicode(self.cbTipoAdesao.GetValue())
            self.licitacao.cnpjOrgao=unicode(self.tcCnpjOrgao.GetValue())
            self.licitacao.competencia=unicode(self.cbCompetencia.GetValue()) 

            session.commit()
            self.message = wx.MessageDialog(None, u'A Adesão Ata de Licitação foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.licitacao = None
            self.windowEditaLicitacaoAta.Close()

    def excluiLicitacaoAta(self, event, idLicitacaoAta):

        if idLicitacaoAta is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Adesão Ata de Licitação?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.licitacao = LicitacaoAta.query.filter_by(id=idLicitacaoAta).first()
            self.licitacao.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Adesão Ata de Licitação excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(710, 470), pos=(300, 170), title=u"Gerar Arquivo de Adesão Ata de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
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
        self.licitacaoAtaGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(300, 300), style=wx.LC_REPORT)
        self.licitacaoAtaGeraArquivoListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.licitacaoAtaGeraArquivoListCtrl.InsertColumn(1, u'Número da Ata', width=80)
        self.licitacaoAtaGeraArquivoListCtrl.InsertColumn(2, u'Tipo de Adesão', width=80)
        self.licitacaoAtaGeraArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.licitacaoAtaGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(320, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(320, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.licitacaoAtaParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(300, 300), style=wx.LC_REPORT)
        self.licitacaoAtaParaArquivoListCtrl.InsertColumn(0, u'Proc. de Compra', width=100)
        self.licitacaoAtaParaArquivoListCtrl.InsertColumn(1, u'Número da Ata', width=80)
        self.licitacaoAtaParaArquivoListCtrl.InsertColumn(2, u'Descrição do Item', width=80)
        self.licitacaoAtaParaArquivoListCtrl.InsertColumn(3, u'', width=0)
        self.licitacaoAtaParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def inserePorCompetencia(self, event):

        licitacoes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            licitacoes = LicitacaoAta.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            licitacoes = LicitacaoAta.query.all()

        self.licitacaoAtaGeraArquivoListCtrl.DeleteAllItems()

        if not licitacoes:
            self.message = wx.MessageDialog(None, u'Não existe Adesão Ata de Licitação para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(licitacoes) == self.licitacaoAtaParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for licitacao in licitacoes:
                    igual = False
                    if self.licitacaoAtaParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.licitacaoAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(licitacao.processoCompra))
                        self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(licitacao.numeroAta))
                        self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(licitacao.tipoAdesao))
                        self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 3, unicode(licitacao.id))
                        igual = True

                    else:

                        for x in range(self.licitacaoAtaParaArquivoListCtrl.GetItemCount()):

                            if licitacao.processoCompra == unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(x, 0).GetText()) and licitacao.numeroAta == unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(x, 1).GetText()) and licitacao.tipoAdesao == unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(x, 2).GetText()):
                                igual = True

                    if not igual:

                        index = self.licitacaoAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(item.processoCompra))
                        self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(item.numeroAta))
                        self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(item.descricaoItem))
                        self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 3, unicode(item.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensGeraArquivos(self, event):

        item = self.licitacaoAtaGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.licitacaoAtaGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensParaArquivo(self, event):

        item = self.licitacaoAtaParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.licitacaoAtaParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Adesões Ata de Licitação a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.licitacaoAtaParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.licitacaoAtaGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.licitacaoAtaParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.licitacaoAtaGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.licitacaoAtaParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.licitacaoAtaGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.licitacaoAtaParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.licitacaoAtaGeraArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.licitacaoAtaGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as Adesões Ata de Licitação a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.licitacaoAtaGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.licitacaoAtaGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.licitacaoAtaParaArquivoListCtrl.GetItem(item, 3).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.licitacaoAtaParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.licitacaoAtaParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Adesão Ata de Licitação para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="ADESAOATALICITACAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Adesão Ata de Licitação gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Adesão Ata de Licitação gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.licitacaoAtaParaArquivoListCtrl.GetItemCount()):

            try:

                idLicitacaoAta = int(self.licitacaoAtaParaArquivoListCtrl.GetItem(x, 3).GetText())
                item = LicitacaoAta.query.filter_by(id=idLicitacaoAta).first()

                f.write(unicode(item.processoCompra.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.numeroAta.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(item.numeroLicitacao.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(item.publicacaoDOE)))
                f.write(unicode(self.transformaData(item.dataValidade)))
                f.write(unicode(item.numeroDOE.ljust(6).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(item.dataAdesao)))
                f.write(unicode(self.transfromTipoAdesao(item.tipoAdesao).zfill(2)))
                f.write(unicode(self.retiraCaracteresCpfCnpj(item.cnpjOrgao).zfill(14)))                
                f.write(u'\n')

            except:

                return 0
        
        return 1

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]

    def transfromTipoAdesao(self, tipoAdesao):

        if tipoAdesao == u'Adesão ata própria (Participante)':
            
            return "1"
        
        else:
        
            return "2"                  

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