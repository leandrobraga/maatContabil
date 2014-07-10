# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import burocracia
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_CONTRATO_NOVO = 1001
ID_TOOLBAR_CONTRATO_EDITAR = 1002
ID_TOOLBAR_CONTRATO_EXCLUIR = 1003
ID_TOOLBAR_CONTRATO_CRIAR_ARQUIVO = 1004


class WindowContrato(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 280), pos=(300, 170), title="Contrato", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelContrato = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTRATO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp='Adiciona novo contrato')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTRATO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp='Edita contrato selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTRATO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp='Exclui contrato selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTRATO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp='Gera arquivo de contrato')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']

        self.cbCompetenciaForView = wx.ComboBox(self.panelContrato, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereContratoListCtrl)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.contratoListCtrl = wx.ListCtrl(self.panelContrato, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.contratoListCtrl.InsertColumn(0, u"Número do Contrato", width=115)
        self.contratoListCtrl.InsertColumn(1, u"Nome Contratado", width=155)
        self.contratoListCtrl.InsertColumn(2, u"Objetivo do Contrato", width=250)
        self.contratoListCtrl.InsertColumn(3, u'', width=0)
        self.contratoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.contratoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.contratoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl
        #self.insereContratoListCtrl()

        self.siglasContratos = {u'Termo de Contrato': 'CT', u'Termo Aditivo ao Contrato': 'TACT', u'Termo de Re-Ratificação de Contrato':'TRRCT', 
                                 u'Termo de Distrato de Contrato':'TDCT', u'Termo de Rescisão de Contrato':'TRCT', u'Termo Concessão de Uso':'TCU',
            u'Termo de Aditivo de Concessão de Uso':'TACU', u'Termo de Permissão de Uso':'TPU', u'Termo Aditivo de Permissão de Uso':'TAPU',
            u'Termo de Autorização de Uso':'TAU', u'Termo Aditivo de Autorização de Uso':'TAAU', u'Termo de Cessão':'TC', u'Termo Aditivo a Cessão':'TAC',
            u'Termo de Compromisso':'TCO', u'Termo Aditivo ao Compromisso':'TACO', u'Termo de Direito Real de Uso':'TDRU', 
            u'Termo Aditivo ao Direito Real de Uso':'TADU', u'Termo de Doação':'TD', u'Carta Contrato':'CACT', u'Ordem de Serviços':'OS',
            u'Termo Aditivo a Ordem de Serviços':'TAOS', u'Termo de Revogação de Autorização de Uso':'TRTA', u'Termo de Adesão ao Contrato':'TA',
            u'Termo de Outorga':'TOU', u'Termo Aditivo de Outorga':'TAOU', u'Termo de Ex-Ofício':'TEXO', u'Termo Aditivo de Carta Contrato':'TACC',
            u'Termo de Cooperação Técnica':'TCT', u'Termo Aditivo de Cooperação Técnica':'ATCT', u'Termo de Ordem de Serviços':'TOS',
            u'Termo de Recebimento de Auxílio Aluguel':'TRAA', u'Termo de Recebimento de Cheque Moradia':'TRCM', u'Termo de Recebimento de Indenização':'TRIN',
            u'Termo de Quitação de Contrato':'TQC', u'Protocolo de Intenções':'PI', u'Termo Aditivo de Protocolo de Intenções':'TAPI',
            u'Termo Aditivo de Doação':'TAD', u'Apostila de Retificação de Contrato':'ARC', u'Termo de Contrato de Gestão':'TCG', 
            u'Termo Aditivo de Contrato de Gestão':'TACG', u'Termo de Rescisão de Cessão':'TRCES', u'Termo de Apostilamento de Contrato':'TAPC',
            u'Apólice de contratação de serviços de seguro':'ASS', u'Termo Aditivo de Apólice de contratação de serviços de seguro':'TASS'}

        self.choicesTipoContrato = [u'Termo de Contrato', u'Termo Aditivo ao Contrato', u'Termo de Re-Ratificação de Contrato', u'Termo de Distrato de Contrato',
                                u'Termo de Rescisão de Contrato', u'Termo Concessão de Uso', u'Termo de Aditivo de Concessão de Uso', u'Termo de Permissão de Uso',
                                u'Termo Aditivo de Permissão de Uso', u'Termo de Autorização de Uso', u'Termo Aditivo de Autorização de Uso', u'Termo de Cessão',
                                u'Termo Aditivo a Cessão', u'Termo de Compromisso', u'Termo Aditivo ao Compromisso', u'Termo de Direito Real de Uso',
                                u'Termo Aditivo ao Direito Real de Uso', u'Termo de Doação', u'Carta Contrato', u'Ordem de Serviços',
                                u'Termo Aditivo a Ordem de Serviços', u'Termo de Revogação de Autorização de Uso', u'Termo de Adesão ao Contrato',
                                u'Termo de Outorga', u'Termo Aditivo de Outorga', u'Termo de Ex-Ofício', u'Termo Aditivo de Carta Contrato',
                                u'Termo de Cooperação Técnica', u'Termo Aditivo de Cooperação Técnica', u'Termo de Ordem de Serviços',
                                u'Termo de Recebimento de Auxílio Aluguel', u'Termo de Recebimento de Cheque Moradia', u'Termo de Recebimento de Indenização',
                                u'Termo de Quitação de Contrato', u'Protocolo de Intenções', u'Termo Aditivo de Protocolo de Intenções',
                                u'Termo Aditivo de Doação', u'Apostila de Retificação de Contrato', u'Termo de Contrato de Gestão',
                                u'Termo Aditivo de Contrato de Gestão', u'Termo de Rescisão de Cessão', u'Termo de Apostilamento de Contrato',
                                u'Apólice de contratação de serviços de seguro', u'Termo Aditivo de Apólice de contratação de serviços de seguro']

        self.choicesRecebeValor = [u'S', u'N']

        self.choicesTipoJuridicoContratado = [u'Física', u'Jurídica', u'Outros']

        self.choicesCodigoMoeda = [u'Real', u'Dolar', u'Outra Moeda']

        #Binds

        self.Bind(wx.EVT_CLOSE, self.quit)
        self.Bind(wx.EVT_MENU, self.novoContrato, id=ID_TOOLBAR_CONTRATO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.editaWindowContrato(event, self.idSelecionado), id=ID_TOOLBAR_CONTRATO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiContrato(event, self.idSelecionado), id=ID_TOOLBAR_CONTRATO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_CONTRATO_CRIAR_ARQUIVO)

        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.contratoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_CONTRATO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_CONTRATO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_CONTRATO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_CONTRATO_CRIAR_ARQUIVO, gerar)

    def novoContrato(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoContrato = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 750), pos=(300, 170), title="Novo - Contrato", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoContrato = wx.Panel(self.windowNovoContrato, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoContrato, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoContrato, -1, u'Competência', pos=(10, 0), style=wx.ALIGN_LEFT)
        self.cbCompetencia = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 20), size=(250, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 42), size=(660, 60))

        self.stTipoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Tipo', pos=(10, 50), style=wx.ALIGN_LEFT)
        self.cbTipoContrato = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 70), size=(400, -1), choices=self.choicesTipoContrato, style=wx.CB_READONLY)
        self.cbTipoContrato.Bind(wx.EVT_COMBOBOX, self.insereSiglaContrato)

        self.stRecebeValor = wx.StaticText(self.panelNovoContrato, -1, u'Recebe Valor ?', pos=(430, 50), style=wx.ALIGN_LEFT)
        self.cbRecebeValor = wx.ComboBox(self.panelNovoContrato, -1, pos=(430, 70), size=(50, -1), choices=self.choicesRecebeValor, style=wx.CB_READONLY)
        self.cbRecebeValor.Bind(wx.EVT_COMBOBOX, self.liberaValor)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 105), size=(660, 60))

        self.stTipoJuridicoContratado = wx.StaticText(self.panelNovoContrato, -1, u'Tipo Pessoa', pos=(10, 115), style=wx.ALIGN_LEFT)
        self.cbTipoJuridicoContratado = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 135), size=(150, -1), choices=self.choicesTipoJuridicoContratado, style=wx.CB_READONLY)
        self.cbTipoJuridicoContratado.Bind(wx.EVT_COMBOBOX, self.definirCampoCic)

        self.stCicContratado = wx.StaticText(self.panelNovoContrato, -1, u'CNPJ ou CPF', pos=(180, 115), style=wx.ALIGN_LEFT)
        self.tcCicContratado = masked.TextCtrl(self.panelNovoContrato, -1, mask="")
        self.tcCicContratado.SetSize((140, -1))
        self.tcCicContratado.SetPosition((180, 135))
        self.tcCicContratado.SetEditable(False)

        self.stNomeContratado = wx.StaticText(self.panelNovoContrato, -1, u'Nome', pos=(340, 115), style=wx.ALIGN_LEFT)
        self.tcNomeContratado = wx.TextCtrl(self.panelNovoContrato, -1, pos=(340, 135), size=(310, -1), style=wx.ALIGN_LEFT)
        self.tcNomeContratado.SetMaxLength(50)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 165), size=(660, 170))

        self.stNumeroContrato = wx.StaticText(self.panelNovoContrato, -1, u'Número', pos=(10, 180), style=wx.ALIGN_LEFT)
        self.tcNumeroContratado = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 200), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroContratado.SetMaxLength(16)

        self.stObjetivoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Objetivo', pos=(130, 180), style=wx.ALIGN_LEFT)
        self.tcObjetivoContratado = wx.TextCtrl(self.panelNovoContrato, -1, pos=(130, 200), size=(350, -1), style=wx.ALIGN_LEFT)
        self.tcObjetivoContratado.SetMaxLength(300)

        self.stCodigoMoeda = wx.StaticText(self.panelNovoContrato, -1, u'Tipo de Moeda', pos=(10, 230), style=wx.ALIGN_LEFT)
        self.cbCodigoMoeda = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 250), size=(90, -1), choices=self.choicesCodigoMoeda, style=wx.CB_READONLY)
        self.cbCodigoMoeda.Disable()

        self.stValorContrato = wx.StaticText(self.panelNovoContrato, -1, u'Valor', pos=(130, 230), style=wx.ALIGN_LEFT)
        self.tcValorContrato = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoContrato, pos=wx.Point(130, 250), style=0, value=0)
        self.tcValorContrato.SetFractionWidth(2)
        self.tcValorContrato.SetGroupChar(u"#")
        self.tcValorContrato.SetDecimalChar(u",")
        self.tcValorContrato.SetGroupChar(u".")
        self.tcValorContrato.SetAllowNegative(False)
        self.tcValorContrato.Disable()

        self.stDataAssinaturaContrato = wx.StaticText(self.panelNovoContrato, -1, u'Data de Assinatura', pos=(290, 230), style=wx.ALIGN_LEFT)
        self.tcDataAssinaturaContrato = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataAssinaturaContrato.SetSize((80, -1))
        self.tcDataAssinaturaContrato.SetPosition((290, 250))

        self.stDataVencimentoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(410, 230), style=wx.ALIGN_LEFT)
        self.tcDataVencimentoContrato = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoContrato.SetSize((80, -1))
        self.tcDataVencimentoContrato.SetPosition((410, 250))

        self.stNumeroProcessoLicitatorio = wx.StaticText(self.panelNovoContrato, -1, u'Número do Processo Licitatório', pos=(10, 280), style=wx.ALIGN_LEFT)
        self.tcNumeroProcessoLicitatorio = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 300), size=(200, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroProcessoLicitatorio.SetMaxLength(16)

        self.stNumeroDiarioOficial = wx.StaticText(self.panelNovoContrato, -1, u'Número Diário Oficial', pos=(240, 280), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial = wx.TextCtrl(self.panelNovoContrato, -1, pos=(240, 300), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial.SetMaxLength(6)
        self.tcNumeroDiarioOficial.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stDataPublicacaoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Data de Publicação', pos=(380, 280), style=wx.ALIGN_LEFT)
        self.tcDataPublicacaoContrato = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataPublicacaoContrato.SetSize((80, -1))
        self.tcDataPublicacaoContrato.SetPosition((380, 300))

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 335), size=(660, 360))

        self.stNumeroCertidaoINSS = wx.StaticText(self.panelNovoContrato, -1, u'INSS', pos=(10, 350), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoINSS = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 370), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoINSS.SetMaxLength(60)

        self.stDataCertidaoINSS = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 350), style= wx.ALIGN_LEFT)
        self.tcDataCertidaoINSS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataCertidaoINSS.SetSize((80, -1))
        self.tcDataCertidaoINSS.SetPosition((150, 370))

        self.stDataValidadeINSS = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 350), style= wx.ALIGN_LEFT)
        self.tcDataValidadeINSS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataValidadeINSS.SetSize((80, -1))
        self.tcDataValidadeINSS.SetPosition((280, 370))

        self.stNumeroCertidaoFGTS = wx.StaticText(self.panelNovoContrato, -1, u'FGTS', pos=(10, 400), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFGTS = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 420), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFGTS.SetMaxLength(60)
        
        self.stDataCertidaoFGTS = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 400), style= wx.ALIGN_LEFT)
        self.tcDataCertidaoFGTS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataCertidaoFGTS.SetSize((80, -1))
        self.tcDataCertidaoFGTS.SetPosition((150, 420))

        self.stDataValidadeFGTS = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 400), style= wx.ALIGN_LEFT)
        self.tcDataValidadeFGTS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataValidadeFGTS.SetSize((80, -1))
        self.tcDataValidadeFGTS.SetPosition((280, 420))

        self.stNumeroCertidaoFazendaEstadual = wx.StaticText(self.panelNovoContrato, -1, u'Fazenda Estadual', pos=(10, 450), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaEstadual = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 470), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaEstadual.SetMaxLength(60)
        
        self.stDataEmissaoFazendaEstadual = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 450), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoFazendaEstadual = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoFazendaEstadual.SetSize((80, -1))
        self.tcDataEmissaoFazendaEstadual.SetPosition((150, 470))

        self.stDataVencimentoFazendaEstadual = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 450), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoFazendaEstadual = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoFazendaEstadual.SetSize((80, -1))
        self.tcDataVencimentoFazendaEstadual.SetPosition((280, 470))

        self.stNumeroCertidaoFazendaMunicipal = wx.StaticText(self.panelNovoContrato, -1, u'Fazenda Municipal', pos=(10, 500), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaMunicipal = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 520), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaMunicipal.SetMaxLength(60)
        
        self.stDataEmissaoFazendaMunicipal = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 500), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoFazendaMunicipal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoFazendaMunicipal.SetSize((80, -1))
        self.tcDataEmissaoFazendaMunicipal.SetPosition((150, 520))

        self.stDataVencimentoFazendaMunicipal = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 500), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoFazendaMunicipal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoFazendaMunicipal.SetSize((80, -1))
        self.tcDataVencimentoFazendaMunicipal.SetPosition((280, 520))

        self.stNumeroCertidaoFazendaFederal = wx.StaticText(self.panelNovoContrato, -1, u'Fazenda Federal', pos=(10, 550), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaFederal = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 570), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaFederal.SetMaxLength(60)
        
        self.stDataEmissaoFazendaFederal = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 550), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoFazendaFederal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoFazendaFederal.SetSize((80, -1))
        self.tcDataEmissaoFazendaFederal.SetPosition((150, 570))

        self.stDataVencimentoFazendaFederal = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 550), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoFazendaFederal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoFazendaFederal.SetSize((80, -1))
        self.tcDataVencimentoFazendaFederal.SetPosition((280, 570))

        self.stNumeroCertidaoCNDT = wx.StaticText(self.panelNovoContrato, -1, u'CNDT', pos=(10, 600), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoCNDT = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 620), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoCNDT.SetMaxLength(60)
        
        self.stDataEmissaoCNDT = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 600), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoCNDT = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoCNDT.SetSize((80, -1))
        self.tcDataEmissaoCNDT.SetPosition((150, 620))

        self.stDataVencimentoCNDT = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 600), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoCNDT = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoCNDT.SetSize((80, -1))
        self.tcDataVencimentoCNDT.SetPosition((280, 620))

        self.stNumeroCertidaoOutras = wx.StaticText(self.panelNovoContrato, -1, u'Outras', pos=(10, 650), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoOutras = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 670), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoOutras.SetMaxLength(60)
        
        self.stDataEmissaoOutras = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 650), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoOutras = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoOutras.SetSize((80, -1))
        self.tcDataEmissaoOutras.SetPosition((150, 670))

        self.stDataVencimentoOutras = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 650), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoOutras = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoOutras.SetSize((80, -1))
        self.tcDataVencimentoOutras.SetPosition((280, 670))


        self.btnSalvar = wx.Button(self.panelNovoContrato, -1, "Salvar", pos=(230, 700),size=(-1,18))
        self.btnCancelar = wx.Button(self.panelNovoContrato, -1, "Cancelar", pos=(350, 700),size=(-1,18))

        self.windowNovoContrato.Centre()
        self.windowNovoContrato.Show()

        #Bind
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitContratoNovo)
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarContrato)
        self.windowNovoContrato.Bind(wx.EVT_CLOSE, self.quitContratoNovo)
        #Fim Bind

    def liberaValor(self, event):

        if self.cbRecebeValor.GetValue() == 'S':
            self.cbCodigoMoeda.Enable()
            self.tcValorContrato.Enable()
        else:
            self.cbCodigoMoeda.Disable()
            self.cbCodigoMoeda.SetSelection(-1)
            self.tcValorContrato.Disable()
            self.tcValorContrato.SetValue("0")

    def salvarContrato(self, event):

        if self.valida():
            Contrato(tipoContrato=unicode(self.cbTipoContrato.GetValue()),
                recebeValor=unicode(self.cbRecebeValor.GetValue()),
                tipoJuridicoContratado=unicode(self.cbTipoJuridicoContratado.GetValue()),
                cicContratado=unicode(self.tcCicContratado.GetValue()),
                nomeContratado=unicode(self.tcNomeContratado.GetValue()),
                numeroContrato=unicode(self.tcNumeroContratado.GetValue()),
                objetivoContrato=unicode(self.tcObjetivoContratado.GetValue()),
                codigoMoeda=unicode(self.cbCodigoMoeda.GetValue()),
                valorContrato=unicode(self.tcValorContrato.GetValue()),
                dataAssinaturaContrato=unicode(self.tcDataAssinaturaContrato.GetValue()),
                dataVencimentoContrato=unicode(self.tcDataVencimentoContrato.GetValue()),
                numeroProcessoLicitatorio=unicode(self.tcNumeroProcessoLicitatorio.GetValue()),
                numeroDiarioOficial=unicode(self.tcNumeroDiarioOficial.GetValue()),
                dataPublicacaoContrato=unicode(self.tcDataPublicacaoContrato.GetValue()),
                numeroCertidaoINSS=unicode(self.tcNumeroCertidaoINSS.GetValue()),
                dataCertidaoINSS=unicode(self.tcDataCertidaoINSS.GetValue()),
                dataValidadeINSS=unicode(self.tcDataValidadeINSS.GetValue()),
                numeroCertidaoFGTS=unicode(self.tcNumeroCertidaoFGTS.GetValue()),
                dataCertidaoFGTS=unicode(self.tcDataCertidaoFGTS.GetValue()),
                dataValidadeFGTS=unicode(self.tcDataValidadeFGTS.GetValue()),
                numeroCertidaoFazendaEstadual=unicode(self.tcNumeroCertidaoFazendaEstadual.GetValue()),
                dataCertidaoFazendaEstadual=unicode(self.tcDataEmissaoFazendaEstadual.GetValue()),
                dataValidadeFazendaEstadual=unicode(self.tcDataVencimentoFazendaEstadual.GetValue()),
                numeroCertidaoFazendaMunicipal=unicode(self.tcNumeroCertidaoFazendaMunicipal.GetValue()),
                dataCertidaoFazendaMunicipal=unicode(self.tcDataEmissaoFazendaMunicipal.GetValue()),
                dataValidadeFazendaMunicipal=unicode(self.tcDataVencimentoFazendaMunicipal.GetValue()),
                numeroCertidaoFazendaFederal=unicode(self.tcNumeroCertidaoFazendaFederal.GetValue()),
                dataCertidaoFazendaFederal=unicode(self.tcDataEmissaoFazendaFederal.GetValue()),
                dataValidadeFazendaFederal=unicode(self.tcDataVencimentoFazendaFederal.GetValue()),
                numeroCertidaoCNDT=unicode(self.tcNumeroCertidaoCNDT.GetValue()),
                dataCertidaoCNDT=unicode(self.tcDataEmissaoCNDT.GetValue()),
                dataValidadeCNDT=unicode(self.tcDataVencimentoCNDT.GetValue()),
                numeroCertidaoOutras=unicode(self.tcNumeroCertidaoOutras.GetValue()),
                dataCertidaoOutras=unicode(self.tcDataEmissaoOutras.GetValue()),
                dataValidadeOutras=unicode(self.tcDataVencimentoOutras.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue()),
            )
            session.commit()
            self.message = wx.MessageDialog(None, u'Contrato salvo com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereContratoListCtrl(None)
            self.windowNovoContrato.Close()

    def quitContratoNovo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoContrato.Destroy()

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def definirCampoCic(self, event):

        if event.GetString() == u"Física":

            self.tcCicContratado.SetValue('')
            self.tcCicContratado.SetMask(("###.###.###-##"))
            self.tcCicContratado.SetEditable(True)

        elif event.GetString() == u"Jurídica":

            self.tcCicContratado.SetValue('')
            self.tcCicContratado.SetMask(("##.###.###/####-##"))
            self.tcCicContratado.SetEditable(True)
        else:

            self.tcCicContratado.SetValue('')
            self.tcCicContratado.SetMask(('###############'))
            self.tcCicContratado.SetMask(('##############'))
            self.tcCicContratado.SetEditable(True)

    def editaWindowContrato(self, event, idContrato):

        if idContrato is None:
            self.message = wx.MessageDialog(None, u'Nenhum contrato foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.contrato = Contrato.query.filter_by(id=idContrato).first()

        self.windowEditaContrato = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 750), pos=(300, 170), title=u"Editar - Contrato", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoContrato = wx.Panel(self.windowEditaContrato, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoContrato, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.contrato.id))

        self.stCompetencia = wx.StaticText(self.panelNovoContrato, -1, u'Competência', pos=(10, 0), style=wx.ALIGN_LEFT)
        self.cbCompetencia = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 20), size=(250, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.contrato.competencia)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 40), size=(660, 60))

        self.stTipoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Tipo', pos=(10, 50), style=wx.ALIGN_LEFT)
        self.cbTipoContrato = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 70), size=(400, -1), choices=self.choicesTipoContrato, style=wx.CB_READONLY)
        self.cbTipoContrato.SetValue(self.contrato.tipoContrato)
        self.cbTipoContrato.Bind(wx.EVT_COMBOBOX, self.editaInsereSiglaContrato)

        self.stRecebeValor = wx.StaticText(self.panelNovoContrato, -1, u'Recebe Valor ?', pos=(430, 50), style=wx.ALIGN_LEFT)
        self.cbRecebeValor = wx.ComboBox(self.panelNovoContrato, -1, pos=(430, 70), size=(50, -1), choices=self.choicesRecebeValor, style=wx.CB_READONLY)
        self.cbRecebeValor.Bind(wx.EVT_COMBOBOX, self.liberaValor)
        self.cbRecebeValor.SetValue(self.contrato.recebeValor)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 105), size=(660, 60))

        self.stTipoJuridicoContratado = wx.StaticText(self.panelNovoContrato, -1, u'Tipo Pessoa', pos=(10, 115), style=wx.ALIGN_LEFT)
        self.cbTipoJuridicoContratado = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 135), size=(150, -1), choices=self.choicesTipoJuridicoContratado, style=wx.CB_READONLY)
        self.cbTipoJuridicoContratado.Bind(wx.EVT_COMBOBOX, self.definirCampoCic)
        self.cbTipoJuridicoContratado.SetValue(self.contrato.tipoJuridicoContratado)

        self.stCicContratado = wx.StaticText(self.panelNovoContrato, -1, u'CNPJ ou CPF', pos=(180, 115), style=wx.ALIGN_LEFT)
        self.tcCicContratado = masked.TextCtrl(self.panelNovoContrato, -1, mask="")
        self.tcCicContratado.SetSize((140, -1))
        self.tcCicContratado.SetPosition((180, 135))
        self.tcCicContratado.SetEditable(True)
        self.tcCicContratado.SetValue(self.contrato.cicContratado)

        self.stNomeContratado = wx.StaticText(self.panelNovoContrato, -1, u'Nome', pos=(340, 115), style=wx.ALIGN_LEFT)
        self.tcNomeContratado = wx.TextCtrl(self.panelNovoContrato, -1, pos=(340, 135), size=(310, -1), style=wx.ALIGN_LEFT)
        self.tcNomeContratado.SetMaxLength(50)
        self.tcNomeContratado.SetValue(self.contrato.nomeContratado)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 165), size=(660, 170))

        self.stNumeroContrato = wx.StaticText(self.panelNovoContrato, -1, u'Número', pos=(10, 180), style=wx.ALIGN_LEFT)
        self.tcNumeroContratado = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 200), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroContratado.SetMaxLength(16)
        self.tcNumeroContratado.SetValue(self.contrato.numeroContrato)

        self.stObjetivoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Objetivo', pos=(130, 180), style=wx.ALIGN_LEFT)
        self.tcObjetivoContratado = wx.TextCtrl(self.panelNovoContrato, -1, pos=(130, 200), size=(350, -1), style=wx.ALIGN_LEFT)
        self.tcObjetivoContratado.SetMaxLength(300)
        self.tcObjetivoContratado.SetValue(self.contrato.objetivoContrato)

        self.stCodigoMoeda = wx.StaticText(self.panelNovoContrato, -1, u'Tipo de Moeda', pos=(10, 230), style=wx.ALIGN_LEFT)
        self.cbCodigoMoeda = wx.ComboBox(self.panelNovoContrato, -1, pos=(10, 250), size=(90, -1), choices=self.choicesCodigoMoeda, style=wx.CB_READONLY)
        self.cbCodigoMoeda.SetValue(self.contrato.codigoMoeda)

        self.stValorContrato = wx.StaticText(self.panelNovoContrato, -1, u'Valor', pos=(130, 230), style=wx.ALIGN_LEFT)
        self.tcValorContrato = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoContrato, pos=wx.Point(130, 250), style=0, value=0)
        self.tcValorContrato.SetFractionWidth(2)
        self.tcValorContrato.SetGroupChar(u"#")
        self.tcValorContrato.SetDecimalChar(u",")
        self.tcValorContrato.SetGroupChar(u".")
        self.tcValorContrato.SetAllowNegative(False)
        self.tcValorContrato.SetValue(float(self.contrato.valorContrato))
        self.liberaValor(None)

        self.stDataAssinaturaContrato = wx.StaticText(self.panelNovoContrato, -1, u'Data de Assinatura', pos=(290, 230), style=wx.ALIGN_LEFT)
        self.tcDataAssinaturaContrato = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataAssinaturaContrato.SetSize((80, -1))
        self.tcDataAssinaturaContrato.SetPosition((290, 250))
        self.tcDataAssinaturaContrato.SetValue(self.contrato.dataAssinaturaContrato)

        self.stDataVencimentoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(410, 230), style=wx.ALIGN_LEFT)
        self.tcDataVencimentoContrato = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoContrato.SetSize((80, -1))
        self.tcDataVencimentoContrato.SetPosition((410, 250))
        self.tcDataVencimentoContrato.SetValue(self.contrato.dataVencimentoContrato)

        self.stNumeroProcessoLicitatorio = wx.StaticText(self.panelNovoContrato, -1, u'Número do Processo Licitatório', pos=(10, 280), style=wx.ALIGN_LEFT)
        self.tcNumeroProcessoLicitatorio = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 300), size=(200, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroProcessoLicitatorio.SetMaxLength(16)
        self.tcNumeroProcessoLicitatorio.SetValue(self.contrato.numeroProcessoLicitatorio)

        self.stNumeroDiarioOficial = wx.StaticText(self.panelNovoContrato, -1, u'Número Diário Oficial', pos=(240, 280), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial = wx.TextCtrl(self.panelNovoContrato, -1, pos=(240, 300), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial.SetMaxLength(6)
        self.tcNumeroDiarioOficial.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcNumeroDiarioOficial.SetValue(self.contrato.numeroDiarioOficial)

        self.stDataPublicacaoContrato = wx.StaticText(self.panelNovoContrato, -1, u'Data de Publicação', pos=(380, 280), style=wx.ALIGN_LEFT)
        self.tcDataPublicacaoContrato = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataPublicacaoContrato.SetSize((80, -1))
        self.tcDataPublicacaoContrato.SetPosition((380, 300))
        self.tcDataPublicacaoContrato.SetValue(self.contrato.dataPublicacaoContrato)

        wx.StaticBox(self.panelNovoContrato, -1, pos=(1, 335), size=(660, 360))

        self.stNumeroCertidaoINSS = wx.StaticText(self.panelNovoContrato, -1, u'INSS', pos=(10, 350), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoINSS = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 370), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoINSS.SetMaxLength(60)
        self.tcNumeroCertidaoINSS.SetValue(self.contrato.numeroCertidaoINSS)

        self.stDataCertidaoINSS = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 350), style= wx.ALIGN_LEFT)
        self.tcDataCertidaoINSS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataCertidaoINSS.SetSize((80, -1))
        self.tcDataCertidaoINSS.SetPosition((150, 370))
        self.tcDataCertidaoINSS.SetValue(self.contrato.dataCertidaoINSS)

        self.stDataValidadeINSS = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 350), style= wx.ALIGN_LEFT)
        self.tcDataValidadeINSS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataValidadeINSS.SetSize((80, -1))
        self.tcDataValidadeINSS.SetPosition((280, 370))
        self.tcDataValidadeINSS.SetValue(self.contrato.dataValidadeINSS)

        self.stNumeroCertidaoFGTS = wx.StaticText(self.panelNovoContrato, -1, u'FGTS', pos=(10, 400), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFGTS = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 420), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFGTS.SetMaxLength(60)
        self.tcNumeroCertidaoFGTS.SetValue(self.contrato.numeroCertidaoFGTS)

        self.stDataCertidaoFGTS = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 400), style= wx.ALIGN_LEFT)
        self.tcDataCertidaoFGTS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataCertidaoFGTS.SetSize((80, -1))
        self.tcDataCertidaoFGTS.SetPosition((150, 420))
        self.tcDataCertidaoFGTS.SetValue(self.contrato.dataCertidaoFGTS)

        self.stDataValidadeFGTS = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 400), style= wx.ALIGN_LEFT)
        self.tcDataValidadeFGTS = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataValidadeFGTS.SetSize((80, -1))
        self.tcDataValidadeFGTS.SetPosition((280, 420))
        self.tcDataValidadeFGTS.SetValue(self.contrato.dataValidadeFGTS)

        self.stNumeroCertidaoFazendaEstadual = wx.StaticText(self.panelNovoContrato, -1, u'Fazenda Estadual', pos=(10, 450), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaEstadual = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 470), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaEstadual.SetMaxLength(60)
        self.tcNumeroCertidaoFazendaEstadual.SetValue(self.contrato.numeroCertidaoFazendaEstadual)

        self.stDataEmissaoFazendaEstadual = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 450), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoFazendaEstadual = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoFazendaEstadual.SetSize((80, -1))
        self.tcDataEmissaoFazendaEstadual.SetPosition((150, 470))
        self.tcDataEmissaoFazendaEstadual.SetValue(self.contrato.dataCertidaoFazendaEstadual)

        self.stDataVencimentoFazendaEstadual = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 450), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoFazendaEstadual = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoFazendaEstadual.SetSize((80, -1))
        self.tcDataVencimentoFazendaEstadual.SetPosition((280, 470))
        self.tcDataVencimentoFazendaEstadual.SetValue(self.contrato.dataValidadeFazendaEstadual)

        self.stNumeroCertidaoFazendaMunicipal = wx.StaticText(self.panelNovoContrato, -1, u'Fazenda Municipal', pos=(10, 500), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaMunicipal = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 520), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaMunicipal.SetMaxLength(60)
        self.tcNumeroCertidaoFazendaMunicipal.SetValue(self.contrato.numeroCertidaoFazendaMunicipal)

        self.stDataEmissaoFazendaMunicipal = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 500), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoFazendaMunicipal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoFazendaMunicipal.SetSize((80, -1))
        self.tcDataEmissaoFazendaMunicipal.SetPosition((150, 520))
        self.tcDataEmissaoFazendaMunicipal.SetValue(self.contrato.dataCertidaoFazendaMunicipal)

        self.stDataVencimentoFazendaMunicipal = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 500), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoFazendaMunicipal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoFazendaMunicipal.SetSize((80, -1))
        self.tcDataVencimentoFazendaMunicipal.SetPosition((280, 520))
        self.tcDataVencimentoFazendaMunicipal.SetValue(self.contrato.dataValidadeFazendaMunicipal)

        self.stNumeroCertidaoFazendaFederal = wx.StaticText(self.panelNovoContrato, -1, u'Fazenda Federal', pos=(10, 550), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaFederal = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 570), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoFazendaFederal.SetMaxLength(60)
        self.tcNumeroCertidaoFazendaFederal.SetValue(self.contrato.numeroCertidaoFazendaFederal)

        self.stDataEmissaoFazendaFederal = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 550), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoFazendaFederal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoFazendaFederal.SetSize((80, -1))
        self.tcDataEmissaoFazendaFederal.SetPosition((150, 570))
        self.tcDataEmissaoFazendaFederal.SetValue(self.contrato.dataCertidaoFazendaFederal)

        self.stDataVencimentoFazendaFederal = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 550), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoFazendaFederal = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoFazendaFederal.SetSize((80, -1))
        self.tcDataVencimentoFazendaFederal.SetPosition((280, 570))
        self.tcDataVencimentoFazendaFederal.SetValue(self.contrato.dataValidadeFazendaFederal)

        self.stNumeroCertidaoCNDT = wx.StaticText(self.panelNovoContrato, -1, u'CNDT', pos=(10, 600), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoCNDT = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 620), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoCNDT.SetMaxLength(60)
        self.tcNumeroCertidaoCNDT.SetValue(self.contrato.numeroCertidaoCNDT)
        
        self.stDataEmissaoCNDT = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 600), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoCNDT = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoCNDT.SetSize((80, -1))
        self.tcDataEmissaoCNDT.SetPosition((150, 620))
        self.tcDataEmissaoCNDT.SetValue(self.contrato.dataCertidaoCNDT)

        self.stDataVencimentoCNDT = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 600), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoCNDT = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoCNDT.SetSize((80, -1))
        self.tcDataVencimentoCNDT.SetPosition((280, 620))
        self.tcDataVencimentoCNDT.SetValue(self.contrato.dataValidadeCNDT)

        self.stNumeroCertidaoOutras = wx.StaticText(self.panelNovoContrato, -1, u'Outras', pos=(10, 650), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoOutras = wx.TextCtrl(self.panelNovoContrato, -1, pos=(10, 670), size=(100, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroCertidaoOutras.SetMaxLength(60)
        self.tcNumeroCertidaoOutras.SetValue(self.contrato.numeroCertidaoOutras)
        
        self.stDataEmissaoOutras = wx.StaticText(self.panelNovoContrato, -1, u'Data Emissão', pos=(150, 650), style= wx.ALIGN_LEFT)
        self.tcDataEmissaoOutras = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataEmissaoOutras.SetSize((80, -1))
        self.tcDataEmissaoOutras.SetPosition((150, 670))
        self.tcDataEmissaoOutras.SetValue(self.contrato.dataCertidaoOutras)

        self.stDataVencimentoOutras = wx.StaticText(self.panelNovoContrato, -1, u'Data de Vencimento', pos=(280, 650), style= wx.ALIGN_LEFT)
        self.tcDataVencimentoOutras = masked.TextCtrl(self.panelNovoContrato, -1, mask="##/##/####")
        self.tcDataVencimentoOutras.SetSize((80, -1))
        self.tcDataVencimentoOutras.SetPosition((280, 670))
        self.tcDataVencimentoOutras.SetValue(self.contrato.dataValidadeOutras)

        self.btnEditar = wx.Button(self.panelNovoContrato, -1, "Alterar", pos=(230, 700),size=(-1,18))
        self.btnCancelar = wx.Button(self.panelNovoContrato, -1, "Cancelar", pos=(350, 700),size=(-1,18))


        self.windowEditaContrato.Centre()
        self.windowEditaContrato.Show()

        #Bind
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEditarContrato)
        self.btnEditar.Bind(wx.EVT_BUTTON, lambda event: self.editarContrato(event, self.contrato.id))
        self.windowEditaContrato.Bind(wx.EVT_CLOSE, self.quitEditarContrato)
        #Fim Bind

    def quitEditarContrato(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaContrato.Destroy()

    def editarContrato(self, event, id):

        if self.valida():

            self.contrato.numeroContrato = unicode(self.tcNumeroContratado.GetValue())
            self.contrato.valorContrato = unicode(self.tcValorContrato.GetValue())
            self.contrato.dataAssinaturaContrato = unicode(self.tcDataAssinaturaContrato.GetValue())
            self.contrato.objetivoContrato = unicode(self.tcObjetivoContratado.GetValue())
            self.contrato.numeroProcessoLicitatorio = unicode(self.tcNumeroProcessoLicitatorio.GetValue())
            self.contrato.codigoMoeda = unicode(self.cbCodigoMoeda.GetValue())
            self.contrato.tipoJuridicoContratado = unicode(self.cbTipoJuridicoContratado.GetValue())
            self.contrato.cicContratado = unicode(self.tcCicContratado.GetValue())
            self.contrato.nomeContratado = unicode(self.tcNomeContratado.GetValue())
            self.contrato.dataVencimentoContrato = unicode(self.tcDataVencimentoContrato.GetValue())
            self.contrato.numeroDiarioOficial = unicode(self.tcNumeroDiarioOficial.GetValue())
            self.contrato.dataPublicacaoContrato = unicode(self.tcDataPublicacaoContrato.GetValue())
            self.contrato.recebeValor = unicode(self.cbRecebeValor.GetValue())
            self.contrato.numeroCertidaoINSS = unicode(self.tcNumeroCertidaoINSS.GetValue())
            self.contrato.dataCertidaoINSS = unicode(self.tcDataCertidaoINSS.GetValue())
            self.contrato.dataValidadeINSS = unicode(self.tcDataValidadeINSS.GetValue())
            self.contrato.numeroCertidaoFGTS = unicode(self.tcNumeroCertidaoFGTS.GetValue())
            self.contrato.dataCertidaoFGTS = unicode(self.tcDataCertidaoFGTS.GetValue())
            self.contrato.dataValidadeFGTS = unicode(self.tcDataValidadeFGTS.GetValue())
            self.contrato.numeroCertidaoFazendaEstadual = unicode(self.tcNumeroCertidaoFazendaEstadual.GetValue())
            self.contrato.dataCertidaoFazendaEstadual = unicode(self.tcDataEmissaoFazendaEstadual.GetValue())
            self.contrato.dataValidadeFazendaEstadual = unicode(self.tcDataVencimentoFazendaEstadual.GetValue())
            self.contrato.numeroCertidaoFazendaMunicipal = unicode(self.tcNumeroCertidaoFazendaMunicipal.GetValue())
            self.contrato.dataCertidaoFazendaMunicipal = unicode(self.tcDataEmissaoFazendaMunicipal.GetValue())
            self.contrato.dataValidadeFazendaMunicipal = unicode(self.tcDataVencimentoFazendaMunicipal.GetValue())
            self.contrato.numeroCertidaoFazendaFederal = unicode(self.tcNumeroCertidaoFazendaFederal.GetValue())
            self.contrato.dataCertidaoFazendaFederal = unicode(self.tcDataEmissaoFazendaFederal.GetValue())
            self.contrato.dataValidadeFazendaFederal = unicode(self.tcDataVencimentoFazendaFederal.GetValue())
            self.contrato.numeroCertidaoCNDT = unicode(self.tcNumeroCertidaoCNDT.GetValue())
            self.contrato.dataCertidaoCNDT = unicode(self.tcDataEmissaoCNDT.GetValue())
            self.contrato.dataValidadeCNDT = unicode(self.tcDataVencimentoCNDT.GetValue())
            self.contrato.numeroCertidaoOutras = unicode(self.tcNumeroCertidaoOutras.GetValue())
            self.contrato.dataCertidaoOutras = unicode(self.tcDataEmissaoOutras.GetValue())
            self.contrato.dataValidadeOutras = unicode(self.tcDataVencimentoOutras.GetValue())
            self.contrato.tipoContrato = unicode(self.cbTipoContrato.GetValue())
            self.contrato.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'Contrato foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereContratoListCtrl(None)
            self.contrato = None
            self.windowEditaContrato.Close()

    def excluiContrato(self, event, idContrato):

        if idContrato is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este contrato?', 'Remover - Contrato', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.contrato = Contrato.query.filter_by(id=idContrato).first()
            self.contrato.delete()
            session.commit()
            self.insereContratoListCtrl(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Contrato excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
        else:
            pass

    def editaInsereSiglaContrato(self, event):

        self.message = wx.MessageDialog(None, u'O Número do contrato é alterado quando se muda o Tipo de contrato!', 'Info', wx.OK)
        self.message.ShowModal()
        self.tcNumeroContratado.SetValue("")
        self.tcNumeroContratado.SetValue(unicode(self.siglasContratos[self.cbTipoContrato.GetValue()]))

    def insereSiglaContrato(self, event):

        self.tcNumeroContratado.SetValue("")
        self.tcNumeroContratado.SetValue(unicode(self.siglasContratos[self.cbTipoContrato.GetValue()]))

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

        if self.cbTipoContrato.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo ', 'Info', wx.OK)
            self.cbTipoContrato.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbRecebeValor.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Recebe Valor', 'Info', wx.OK)
            self.cbRecebeValor.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoJuridicoContratado.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Pessoa', 'Info', wx.OK)
            self.cbTipoJuridicoContratado.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoJuridicoContratado.GetSelection() == 0:
            if self.tcCicContratado.GetValue() == "   .   .   -  ":
                self.message = wx.MessageDialog(None, u'O campo CNPJ ou CPF deve ser preenchido', 'Info', wx.OK)
                self.tcCicContratado.SelectAll()
                self.tcCicContratado.SetFocus()
                self.message.ShowModal()
                return 0   

            if not burocracia.CPF(self.tcCicContratado.GetValue()).isValid():
                self.message = wx.MessageDialog(None, u'CPF inválido!', 'Info', wx.OK)
                self.tcCicContratado.SelectAll()
                self.tcCicContratado.SetFocus()
                self.message.ShowModal()
                return 0

        if self.cbTipoJuridicoContratado.GetSelection() == 1:
            if self.tcCicContratado.GetValue() == "  .   .   /    -  ":
                self.message = wx.MessageDialog(None, u'O campo CNPJ ou CPF deve ser preenchido', 'Info', wx.OK)
                self.tcCicContratado.SelectAll()
                self.tcCicContratado.SetFocus()
                self.message.ShowModal()
                return 0

            if not burocracia.CNPJ(self.tcCicContratado.GetValue()).isValid():
                self.message = wx.MessageDialog(None, u'CNPJ inválido!', 'Info', wx.OK)
                self.tcCicContratado.SelectAll()
                self.tcCicContratado.SetFocus()
                self.message.ShowModal()
                return 0

        if self.cbTipoJuridicoContratado.GetSelection() == 2:
            if self.tcCicContratado.GetValue() == '':
                self.message = wx.MessageDialog(None, u'Digite o identificador no campo CNPJ ou CPF', 'Info', wx.OK)
                self.tcCicContratado.SelectAll()
                self.tcCicContratado.SetFocus()
                self.message.ShowModal()
                return 0

        if self.tcNomeContratado.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Nome deve ser preenchido', 'Info', wx.OK)
            self.tcNomeContratado.SelectAll()
            self.tcNomeContratado.SetFocus()
            self.message.ShowModal()
            return 0

        contrato = Contrato.query.filter_by(numeroContrato=self.tcNumeroContratado.GetValue()).first()

        if contrato != None:
            if (unicode(contrato.numeroContrato.upper()) == unicode(self.tcNumeroContratado.GetValue().upper())) and (contrato.id == int(self.tcId.GetValue())):
                pass
            else:
                self.message = wx.MessageDialog(None, u'Já existe um contrato com a numeração: '+self.tcNumeroContratado.GetValue()+u'!', 'Info', wx.OK)
                self.tcNumeroContratado.SelectAll()
                self.tcNumeroContratado.SetFocus()
                self.message.ShowModal()
                return 0

        if self.tcNumeroContratado.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Número deve ser preenchido', 'Info', wx.OK)
            self.tcNumeroContratado.SelectAll()
            self.tcNumeroContratado.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcObjetivoContratado.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Objetivo deve ser preenchido', 'Info', wx.OK)
            self.tcObjetivoContratado.SelectAll()
            self.tcObjetivoContratado.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbRecebeValor.GetValue() == u'S':

            if self.cbCodigoMoeda.GetSelection() == -1:
                self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo de Moeda', 'Info', wx.OK)
                self.cbCodigoMoeda.SetFocus()
                self.message.ShowModal()
                return 0

            if self.tcValorContrato.GetValue() == 0.0:
                self.message = wx.MessageDialog(None, u'O campo Valor não pode ter o valor igual a 0', 'Info', wx.OK)
                self.tcValorContrato.SelectAll()
                self.tcValorContrato.SetFocus()
                self.message.ShowModal()
                return 0

        if not self.validateDate(self.tcDataAssinaturaContrato.GetValue(), u"Data de Assinatura"):
            self.tcDataAssinaturaContrato.SelectAll()
            self.tcDataAssinaturaContrato.SetFocus()
            return 0

        if not self.validateDate(self.tcDataVencimentoContrato.GetValue(), u"Data de Vencimento"):
            self.tcDataVencimentoContrato.SelectAll()
            self.tcDataVencimentoContrato.SetFocus()
            return 0
        
        if self.tcNumeroDiarioOficial.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Número Diário Oficial deve ser preenchido', 'Info', wx.OK)
            self.tcNumeroDiarioOficial.SelectAll()
            self.tcNumeroDiarioOficial.SetFocus()
            self.message.ShowModal()
            return 0

        #if not self.validateDate(self.tcDataPublicacaoContrato.GetValue(), u"Data de Publicação"):
        #    self.tcDataPublicacaoContrato.SelectAll()
        #    self.tcDataPublicacaoContrato.SetFocus()
        #    return 0

        if self.tcNumeroCertidaoINSS.GetValue() != "":
            if not self.validateDate(self.tcDataCertidaoINSS.GetValue(), u"Data Emissão (INSS)"):
                self.tcDataCertidaoINSS.SelectAll()
                self.tcDataCertidaoINSS.SetFocus()
                return 0

            if not self.validateDate(self.tcDataValidadeINSS.GetValue(), u"Data de Vencimento (INSS)"):
                self.tcDataValidadeINSS.SelectAll()
                self.tcDataValidadeINSS.SetFocus()
                return 0

        if self.tcNumeroCertidaoFGTS.GetValue() != "":
            if not self.validateDate(self.tcDataCertidaoFGTS.GetValue(), u"Data Emissão (FGTS)"):
                self.tcDataCertidaoFGTS.SelectAll()
                self.tcDataCertidaoFGTS.SetFocus()
                return 0

            if not self.validateDate(self.tcDataValidadeFGTS.GetValue(), u"Data de Vencimento (FGTS)"):
                self.tcDataValidadeFGTS.SelectAll()
                self.tcDataValidadeFGTS.SetFocus()
                return 0

        if self.tcNumeroCertidaoFazendaEstadual.GetValue() != "":
            if not self.validateDate(self.tcDataEmissaoFazendaEstadual.GetValue(), u"Data Emissão (Fazenda Estadual)"):
                self.tcDataEmissaoFazendaEstadual.SelectAll()
                self.tcDataEmissaoFazendaEstadual.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoFazendaEstadual.GetValue(), u"Data de Vencimento (Fazenda Estadual)"):
                self.tcDataVencimentoFazendaEstadual.SelectAll()
                self.tcDataVencimentoFazendaEstadual.SetFocus()
                return 0

        if self.tcNumeroCertidaoFazendaFederal.GetValue() != "":
            if not self.validateDate(self.tcDataEmissaoFazendaFederal.GetValue(), u"Data Emissão (Fazenda Federal)"):
                self.tcDataEmissaoFazendaEstadual.SelectAll()
                self.tcDataEmissaoFazendaEstadual.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoFazendaFederal.GetValue(), u"Data de Vencimento (Fazenda Federal)"):
                self.tcDataVencimentoFazendaFederal.SelectAll()
                self.tcDataVencimentoFazendaFederal.SetFocus()
                return 0

        if self.tcNumeroCertidaoFazendaMunicipal.GetValue() != "":

            if not self.validateDate(self.tcDataEmissaoFazendaMunicipal.GetValue(), u"Data Emissão (Fazenda Municipal)"):
                self.tcDataEmissaoFazendaMunicipal.SelectAll()
                self.tcDataEmissaoFazendaMunicipal.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoFazendaMunicipal.GetValue(), u"Data de Vencimento (Fazenda Municipal)"):
                self.tcDataVencimentoFazendaMunicipal.SelectAll()
                self.tcDataVencimentoFazendaMunicipal.SetFocus()
                return 0

        if self.tcNumeroCertidaoCNDT.GetValue() != "":

            if not self.validateDate(self.tcDataEmissaoCNDT.GetValue(), u"Data Emissão (CNDT)"):
                self.tcDataEmissaoOutras.SelectAll()
                self.tcDataEmissaoOutras.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoCNDT.GetValue(), u"Data de Vencimento (CNDT)"):
                self.tcDataVencimentoOutras.SelectAll()
                self.tcDataVencimentoOutras.SetFocus()
                return 0

        if self.tcNumeroCertidaoOutras.GetValue() != "":

            if not self.validateDate(self.tcDataEmissaoOutras.GetValue(), u"Data Emissão (Outras)"):
                self.tcDataEmissaoOutras.SelectAll()
                self.tcDataEmissaoOutras.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoOutras.GetValue(), u"Data de Vencimento (Outras)"):
                self.tcDataVencimentoOutras.SelectAll()
                self.tcDataVencimentoOutras.SetFocus()
                return 0

        return 1

    def insereContratoListCtrl(self, event):

        self.contratoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            
            contratos = Contrato.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()
            for contrato in contratos:
                index = self.contratoListCtrl.InsertStringItem(sys.maxint, unicode(contrato.numeroContrato))
                self.contratoListCtrl.SetStringItem(index, 1, contrato.nomeContratado)
                self.contratoListCtrl.SetStringItem(index, 2, contrato.objetivoContrato)
                self.contratoListCtrl.SetStringItem(index, 3, unicode(contrato.id))

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]

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

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Contrato", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        self.tipoContrato = {u'Termo de Contrato' : '1', u'Termo Aditivo ao Contrato' : '2', u'Termo de Re-Ratificação de Contrato' : '3', u'Termo de Distrato de Contrato' : '4',
                                u'Termo de Rescisão de Contrato' : '5', u'Termo Concessão de Uso' : '6', u'Termo de Aditivo de Concessão de Uso' : '7', u'Termo de Permissão de Uso' : '8',
                                u'Termo Aditivo de Permissão de Uso' : '9', u'Termo de Autorização de Uso' : '10', u'Termo Aditivo de Autorização de Uso' : '11', u'Termo de Cessão' : '12',
                                u'Termo Aditivo a Cessão' : '13', u'Termo de Compromisso' : '14', u'Termo Aditivo ao Compromisso' : '15', u'Termo de Direito Real de Uso' : '16',
                                u'Termo Aditivo ao Direito Real de Uso' : '17', u'Termo de Doação' : '18', u'Carta Contrato' : '19', u'Ordem de Serviços' : '20', 
                                u'Termo Aditivo a Ordem de Serviços' : '21', u'Termo de Revogação de Autorização de Uso' : '22', u'Termo de Adesão ao Contrato' : '23', 
                                u'Termo de Outorga' : '24', u'Termo Aditivo de Outorga' : '25', u'Termo de Ex-Ofício' : '26', u'Termo Aditivo de Carta Contrato' : '27', 
                                u'Termo de Cooperação Técnica' : '28', u'Termo Aditivo de Cooperação Técnica' : '29', u'Termo de Ordem de Serviços' : '30', 
                                u'Termo de Recebimento de Auxílio Aluguel' : '31', u'Termo de Recebimento de Cheque Moradia' : '32', u'Termo de Recebimento de Indenização' : '33', 
                                u'Termo de Quitação de Contrato' : '34', u'Protocolo de Intenções' : '35', u'Termo Aditivo de Protocolo de Intenções' : '36', 
                                u'Termo Aditivo de Doação' : '37', u'Apostila de Retificação de Contrato' : '38', u'Termo de Contrato de Gestão' : '39', 
                                u'Termo Aditivo de Contrato de Gestão' : '40', u'Termo de Rescisão de Cessão' : '41', u'Termo de Apostilamento de Contrato' : '42', 
                                u'Apólice de contratação de serviços de seguro': '43', u'Termo Aditivo de Apólice de contratação de serviços de seguro' : '44'}


        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereContratoPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.contratosGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.contratosGeraArquivoListCtrl.InsertColumn(0, u'Número do Contrato', width=130)
        self.contratosGeraArquivoListCtrl.InsertColumn(1, u'Nome Contratado', width=120)
        self.contratosGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.contratosGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensContratosGeraArquivos)

        self.btnIncluiContratoGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiContratoGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveContratoGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveContratoGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.contratosParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.contratosParaArquivoListCtrl.InsertColumn(0, u'Número do Contrato', width=130)
        self.contratosParaArquivoListCtrl.InsertColumn(1, u'Nome Contratado', width=120)
        self.contratosParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.contratosParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensContratosParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)

        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def geraArquivoDialog(self, event):

        if self.contratosParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Contratos para gerar o arquivo!!', u'Info', wx.OK)
            self.message.ShowModal()
            return 0

        dlg = wx.FileDialog(self, message="Salvar ", defaultDir="", defaultFile="CONTRATO", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:

            self.path = dlg.GetPath()
            if os.path.exists(self.path):

                remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                ret = remove_dial.ShowModal()
                if ret == wx.ID_YES:

                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de contratos gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        
            else:
                if self.geraArquivo():
                    self.message = wx.MessageDialog(None, u'Arquivo de contratos gerados com sucesso!', 'Info', wx.OK)
                    self.message.ShowModal()
                
                else:
                    self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                    self.message.ShowModal()
                
    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.contratosParaArquivoListCtrl.GetItemCount()):

            try:

                idContrato = int(self.contratosParaArquivoListCtrl.GetItem(x, 2).GetText())
                contrato = Contrato.query.filter_by(id=idContrato).first()

                f.write(unicode(contrato.numeroContrato.ljust(16).replace("'", "").replace("\"", "")))
                partes = contrato.valorContrato.split('.')
                
                if len(partes[1])> 1:
                    f.write(unicode((contrato.valorContrato).zfill(16).replace(".", ",")))
                else:
                    f.write(unicode((contrato.valorContrato+'0').zfill(16).replace(".", ",")))    
                
                f.write(unicode(self.transformaData(contrato.dataAssinaturaContrato)))
                f.write(unicode(contrato.objetivoContrato.ljust(300).replace("'", "").replace("\"", "")))
                f.write(unicode(contrato.numeroProcessoLicitatorio.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaCodigoMoeda(contrato.codigoMoeda).zfill(3)))
                f.write(unicode(self.transformaTipoJuridico(contrato.tipoJuridicoContratado).zfill(1)))
                f.write(unicode(self.retiraCaracteresCpfCnpj(contrato.cicContratado).zfill(14)))
                f.write(unicode(contrato.nomeContratado.ljust(50).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataVencimentoContrato)))
                f.write(unicode(contrato.numeroDiarioOficial.zfill(6)))
                f.write(unicode(self.transformaData(contrato.dataPublicacaoContrato)))
                f.write(unicode(contrato.recebeValor.zfill(1)))

                f.write(unicode(contrato.numeroCertidaoINSS.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoINSS)))
                f.write(unicode(self.transformaData(contrato.dataValidadeINSS)))

                f.write(unicode(contrato.numeroCertidaoFGTS.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoFGTS)))
                f.write(unicode(self.transformaData(contrato.dataValidadeFGTS)))

                f.write(unicode(contrato.numeroCertidaoFazendaEstadual.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoFazendaEstadual)))
                f.write(unicode(self.transformaData(contrato.dataValidadeFazendaEstadual)))

                f.write(unicode(contrato.numeroCertidaoFazendaMunicipal.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoFazendaMunicipal)))
                f.write(unicode(self.transformaData(contrato.dataValidadeFazendaMunicipal)))

                f.write(unicode(contrato.numeroCertidaoFazendaFederal.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoFazendaFederal)))
                f.write(unicode(self.transformaData(contrato.dataValidadeFazendaFederal)))

                f.write(unicode(contrato.numeroCertidaoCNDT.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoCNDT)))
                f.write(unicode(self.transformaData(contrato.dataValidadeCNDT)))

                f.write(unicode(contrato.numeroCertidaoOutras.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(contrato.dataCertidaoOutras)))
                f.write(unicode(self.transformaData(contrato.dataValidadeOutras)))

                f.write(unicode(self.transformaTipoContrato(contrato.tipoContrato).zfill(2)))

                f.write(u"\n")

            except:
                return 0

        f.close()
        return 1

    def transformaTipoContrato(self, tipo):
        return self.tipoContrato[tipo]

    def transformaTipoJuridico(self, tipo):
        if tipo == u'Física':
            return '1'
        elif tipo == u'Jurídica':
            return '2'
        else:
            return '3'

    def transformaCodigoMoeda(self, moeda):
        if moeda == u"Real":
            return "1"
        elif moeda == u"Dolar":
            return "3"
        else:
            return "9"

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os contratos a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.contratosParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.contratosGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.contratosParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.contratosGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.contratosParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.contratosGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.contratosGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os contratos a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.contratosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.contratosParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.contratosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.contratosParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.contratosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.contratosParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.contratosParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def selecionaItensContratosGeraArquivos(self, event):

        item = self.contratosGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.contratosGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensContratosParaArquivo(self, event):

        item = self.contratosParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.contratosParaArquivoListCtrl.GetNextSelected(item)

    def insereContratoPorCompetencia(self, event):

        contratos = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            contratos = Contrato.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            contratos = Contrato.query.all()

        self.contratosGeraArquivoListCtrl.DeleteAllItems()

        if not contratos:
            self.message = wx.MessageDialog(None, u'Não existe contratos para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(contratos) == self.contratosParaArquivoListCtrl.GetItemCount():
                pass
            else:

                for contrato in contratos:
                    igual = False
                    if self.contratosParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.contratosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(contrato.numeroContrato))
                        self.contratosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(contrato.nomeContratado))
                        self.contratosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(contrato.id))
                        igual = True

                    else:

                        for x in range(self.contratosParaArquivoListCtrl.GetItemCount()):

                            if contrato.numeroContrato == unicode(self.contratosParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.contratosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(contrato.numeroContrato))
                        self.contratosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(contrato.nomeContratado))
                        self.contratosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(contrato.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())
