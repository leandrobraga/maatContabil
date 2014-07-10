# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_CONVENIO_NOVO = 3001
ID_TOOLBAR_CONVENIO_EDITAR = 3002
ID_TOOLBAR_CONVENIO_EXCLUIR = 3003
ID_TOOLBAR_CONVENIO_CRIAR_ARQUIVO = 3004


class WindowConvenio(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelConvenio = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_CONVENIO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONVENIO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONVENIO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONVENIO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesTipoConvenios = [u'Delegação de recursos e encargos', u'Transferência voluntária', u'Termo de Convênio', u'Termo de Denúncia', 
            u'Termo de Cooperação Técnico e Científico', u'Termo de Cooperação Técnico e Financeiro', u'Termo de Parceria', u'Termo Aditivo de Convênio',
            u'Termo Aditivo de Cooperação Técnico e Científico', u'Termo Aditivo de Cooperação Técnico e Financeiro', u'Termo Aditivo de Parceria', u'Cessão', u'Aditivo de cessão',
            u'Termo de Responsabilidade', u'Termo Aditivo de Responsabilidade']

        self.choicesSiglasConvenios = {u'Delegação de recursos e encargos' : 'DRE', u'Transferência voluntária' : 'TRV', u'Termo de Convênio' : 'TCON', 
            u'Termo de Denúncia' : 'TDEN', u'Termo de Cooperação Técnico e Científico' : 'TCTC', u'Termo de Cooperação Técnico e Financeiro' : 'TCTF', 
            u'Termo de Parceria' : 'TPAR', u'Termo Aditivo de Convênio' : 'TACON', u'Termo Aditivo de Cooperação Técnico e Científico' : 'TACTC', 
            u'Termo Aditivo de Cooperação Técnico e Financeiro' : 'TACTF', u'Termo Aditivo de Parceria' : 'TAPAR', u'Termo de Responsabilidade': '', 
            u'Termo Aditivo de Responsabilidade' : ''}

        self.choicesEsferaConvenio = [u'Federal', u'Estadual', u'Municipal', u'ONGs']

        self.choicesMoedas = [u'', u'Real', u'Dólar', u'Outra Moeda']

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro', 
            u'Outubro', u'Novembro',u'Dezembro']


        self.cbCompetenciaForView = wx.ComboBox(self.panelConvenio, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.convenioListCtrl = wx.ListCtrl(self.panelConvenio, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.convenioListCtrl.InsertColumn(0, u"Número do Convênio", width=120)
        self.convenioListCtrl.InsertColumn(1, u"Tipo do Convênio", width=180)
        self.convenioListCtrl.InsertColumn(2, u"Objetivo do Convênio", width=220)
        self.convenioListCtrl.InsertColumn(3, u'', width=0)
        self.convenioListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.convenioListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.convenioListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoConvenio, id=ID_TOOLBAR_CONVENIO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaConvenio(event, self.idSelecionado), id=ID_TOOLBAR_CONVENIO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiConvenio(event, self.idSelecionado), id=ID_TOOLBAR_CONVENIO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_CONVENIO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_CONVENIO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_CONVENIO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_CONVENIO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_CONVENIO_CRIAR_ARQUIVO, gerar)

    def novoConvenio(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoConvenio = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 480), pos=(300, 170), title=u"Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoConvenio = wx.Panel(self.windowNovoConvenio, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoConvenio, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)

        wx.StaticBox(self.panelNovoConvenio, -1, pos=(2, 50), size=(490, 180))

        self.stTipoConvenio = wx.StaticText(self.panelNovoConvenio, -1, u'Tipo', pos=(10, 70))
        self.cbTipoConvenio = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 90), size=(265, -1), choices=self.choicesTipoConvenios, style=wx.CB_READONLY)
        self.cbTipoConvenio.Bind(wx.EVT_COMBOBOX, self.insereSiglaConvenio)

        self.stNumeroConvenio = wx.StaticText(self.panelNovoConvenio, -1, u'Número', pos=(300, 70))
        self.tcNumeroConvenio = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(300, 90), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroConvenio.SetMaxLength(16)

        self.stRecebeValor = wx.StaticText(self.panelNovoConvenio, -1, u'Recebe Valor?', pos=(10, 120))
        self.cbRecebeValor = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 140), size=(50, -1), choices=[u'S', u'N'], style=wx.CB_READONLY)
        self.cbRecebeValor.Bind(wx.EVT_COMBOBOX, self.liberaMoedaValor)

        self.stMoedaConvenio = wx.StaticText(self.panelNovoConvenio, -1, u'Tipo de Moeda', pos=(150, 120))
        self.cbMoedaConvenio = wx.ComboBox(self.panelNovoConvenio, -1, pos=(150, 140), size=(90, -1), choices=self.choicesMoedas, style=wx.CB_READONLY)
        self.cbMoedaConvenio.Disable()

        self.stValorConvenio = wx.StaticText(self.panelNovoConvenio, -1, u'Valor', pos=(300, 120))
        self.tcValorConvenio = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoConvenio, pos=wx.Point(300, 140), style=0, value=0)
        self.tcValorConvenio.SetFractionWidth(2)
        self.tcValorConvenio.SetGroupChar(u"#")
        self.tcValorConvenio.SetDecimalChar(u",")
        self.tcValorConvenio.SetGroupChar(u".")
        self.tcValorConvenio.SetAllowNegative(False)
        self.tcValorConvenio.Disable()

        self.stObjeticoConvenio = wx.StaticText(self.panelNovoConvenio, -1, u'Objetivo', pos=(10, 170))
        self.tcObjetivoConvenio = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 190), size=(350, -1), style=wx.ALIGN_LEFT)
        self.tcObjetivoConvenio.SetMaxLength(300)
        
        self.stDataAssinatura = wx.StaticText(self.panelNovoConvenio, -1, u'Data da Assinatura', pos=(10, 250))
        self.tcDataAssinatura = masked.TextCtrl(self.panelNovoConvenio, -1, mask="##/##/####")
        self.tcDataAssinatura.SetSize((80, -1))
        self.tcDataAssinatura.SetPosition((10, 270))

        self.stDataVencimento = wx.StaticText(self.panelNovoConvenio, -1, u'Data de Vencimento', pos=(200, 250))
        self.tcDataVencimento = masked.TextCtrl(self.panelNovoConvenio, -1, mask="##/##/####")
        self.tcDataVencimento.SetSize((80, -1))
        self.tcDataVencimento.SetPosition((200, 270))

        self.stLeiAtutorizativa = wx.StaticText(self.panelNovoConvenio, -1, u'Num. da Lei Autorizativa', pos=(10, 300))
        self.tcLeiAutorizativa = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 320), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcLeiAutorizativa.SetMaxLength(6)
        self.tcLeiAutorizativa.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stDataLeiAutorizativa = wx.StaticText(self.panelNovoConvenio, -1, u'Data da Lei Autorizativa', pos=(200, 300))
        self.tcDataLeiAutorizativa = masked.TextCtrl(self.panelNovoConvenio, -1, mask="##/##/####")
        self.tcDataLeiAutorizativa.SetSize((80, -1))
        self.tcDataLeiAutorizativa.SetPosition((200, 320))

        self.stNumeroDiarioOficial = wx.StaticText(self.panelNovoConvenio, -1, u'Num. Diário Oficial Est./Mun.', pos=(10, 350), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 370), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial.SetMaxLength(6)
        self.tcNumeroDiarioOficial.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stDataPublicacao = wx.StaticText(self.panelNovoConvenio, -1, u'Data de publicação', pos=(200, 350))
        self.tcDataPublicacao = masked.TextCtrl(self.panelNovoConvenio, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((200, 370))

        self.btnSalvar = wx.Button(self.panelNovoConvenio, -1, u'Salvar', pos=(150, 420))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarConvenio)
        self.btnCancelar = wx.Button(self.panelNovoConvenio, -1, u'Cancelar', pos=(250, 420))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitConvenioNovo)
        self.windowNovoConvenio.Bind(wx.EVT_CLOSE, self.quitConvenioNovo)

        self.windowNovoConvenio.Centre()
        self.windowNovoConvenio.Show()

    def vizualizaConvenio(self, event, idConvenio):

        if idConvenio is None:
            self.message = wx.MessageDialog(None, u'Nenhum convênio foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.convenio = Convenio.query.filter_by(id=idConvenio).first()

        self.windowEditaConvenio = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 480), pos=(300, 170), title=u"Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaConvenio = wx.Panel(self.windowEditaConvenio, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelEditaConvenio, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.convenio.id))

        self.stCompetencia = wx.StaticText(self.panelEditaConvenio, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaConvenio, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.convenio.competencia)

        wx.StaticBox(self.panelEditaConvenio, -1, pos=(2, 50), size=(490, 180))

        self.stTipoConvenio = wx.StaticText(self.panelEditaConvenio, -1, u'Tipo', pos=(10, 70))
        self.cbTipoConvenio = wx.ComboBox(self.panelEditaConvenio, -1, pos=(10, 90), size=(265, -1), choices=self.choicesTipoConvenios, style=wx.CB_READONLY)
        self.cbTipoConvenio.Bind(wx.EVT_COMBOBOX, self.editaInsereSiglaConvenio)
        self.cbTipoConvenio.SetValue(self.convenio.tipoConvenio)

        self.stNumeroConvenio = wx.StaticText(self.panelEditaConvenio, -1, u'Número', pos=(300, 70))
        self.tcNumeroConvenio = wx.TextCtrl(self.panelEditaConvenio, -1, pos=(300, 90), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroConvenio.SetMaxLength(16)
        self.tcNumeroConvenio.SetValue(self.convenio.numeroConvenio)

        self.stRecebeValor = wx.StaticText(self.panelEditaConvenio, -1, u'Recebe Valor?', pos=(10, 120))
        self.cbRecebeValor = wx.ComboBox(self.panelEditaConvenio, -1, pos=(10, 140), size=(50, -1), choices=[u'S', u'N'], style=wx.CB_READONLY)
        self.cbRecebeValor.Bind(wx.EVT_COMBOBOX, self.liberaMoedaValor)
        self.cbRecebeValor.SetValue(self.convenio.recebeValor)

        self.stMoedaConvenio = wx.StaticText(self.panelEditaConvenio, -1, u'Tipo de Moeda', pos=(150, 120))
        self.cbMoedaConvenio = wx.ComboBox(self.panelEditaConvenio, -1, pos=(150, 140), size=(90, -1), choices=self.choicesMoedas, style=wx.CB_READONLY)
        self.cbMoedaConvenio.Disable()
        self.cbMoedaConvenio.SetValue(self.convenio.moedaConvenio)

        self.stValorConvenio = wx.StaticText(self.panelEditaConvenio, -1, u'Valor', pos=(300, 120))
        self.tcValorConvenio = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaConvenio, pos=wx.Point(300, 140), style=0, value=0)
        self.tcValorConvenio.SetFractionWidth(2)
        self.tcValorConvenio.SetGroupChar(u"#")
        self.tcValorConvenio.SetDecimalChar(u",")
        self.tcValorConvenio.SetGroupChar(u".")
        self.tcValorConvenio.Disable()
        self.tcValorConvenio.SetAllowNegative(False)
        self.tcValorConvenio.SetValue(float(self.convenio.valorConvenio))

        if self.convenio.recebeValor == 'S':
            self.tcValorConvenio.Enable()
            self.cbMoedaConvenio.Enable()

        self.stObjeticoConvenio = wx.StaticText(self.panelEditaConvenio, -1, u'Objetivo', pos=(10, 170))
        self.tcObjetivoConvenio = wx.TextCtrl(self.panelEditaConvenio, -1, pos=(10, 190), size=(350, -1), style=wx.ALIGN_LEFT)
        self.tcObjetivoConvenio.SetMaxLength(300)
        self.tcObjetivoConvenio.SetValue(self.convenio.objetivoConvenio)
        
        self.stDataAssinatura = wx.StaticText(self.panelEditaConvenio, -1, u'Data da Assinatura', pos=(10, 250))
        self.tcDataAssinatura = masked.TextCtrl(self.panelEditaConvenio, -1, mask="##/##/####")
        self.tcDataAssinatura.SetSize((80, -1))
        self.tcDataAssinatura.SetPosition((10, 270))
        self.tcDataAssinatura.SetValue(self.convenio.dataAssinaturaConvenio)

        self.stDataVencimento = wx.StaticText(self.panelEditaConvenio, -1, u'Data de Vencimento', pos=(200, 250))
        self.tcDataVencimento = masked.TextCtrl(self.panelEditaConvenio, -1, mask="##/##/####")
        self.tcDataVencimento.SetSize((80, -1))
        self.tcDataVencimento.SetPosition((200, 270))
        self.tcDataVencimento.SetValue(self.convenio.dataVencimentoConvenio)

        self.stLeiAtutorizativa = wx.StaticText(self.panelEditaConvenio, -1, u'Num. da Lei Autorizativa', pos=(10, 300))
        self.tcLeiAutorizativa = wx.TextCtrl(self.panelEditaConvenio, -1, pos=(10, 320), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcLeiAutorizativa.SetMaxLength(6)
        self.tcLeiAutorizativa.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcLeiAutorizativa.SetValue(self.convenio.leiAutorizativa)

        self.stDataLeiAutorizativa = wx.StaticText(self.panelEditaConvenio, -1, u'Data da Lei Autorizativa', pos=(200, 300))
        self.tcDataLeiAutorizativa = masked.TextCtrl(self.panelEditaConvenio, -1, mask="##/##/####")
        self.tcDataLeiAutorizativa.SetSize((80, -1))
        self.tcDataLeiAutorizativa.SetPosition((200, 320))
        self.tcDataLeiAutorizativa.SetValue(self.convenio.dataLeiAutorizativa)

        self.stNumeroDiarioOficial = wx.StaticText(self.panelEditaConvenio, -1, u'Num. Diário Oficial Est./Mun.', pos=(10, 350), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial = wx.TextCtrl(self.panelEditaConvenio, -1, pos=(10, 370), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroDiarioOficial.SetMaxLength(6)
        self.tcNumeroDiarioOficial.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcNumeroDiarioOficial.SetValue(self.convenio.numeroDiarioOficial)

        self.stDataPublicacao = wx.StaticText(self.panelEditaConvenio, -1, u'Data de publicação', pos=(200, 350))
        self.tcDataPublicacao = masked.TextCtrl(self.panelEditaConvenio, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((200, 370))
        self.tcDataPublicacao.SetValue(self.convenio.dataPublicacaoConvenio)

        self.btnSalvar = wx.Button(self.panelEditaConvenio, -1, u'Alterar', pos=(150, 420))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarConvenio)
        self.btnCancelar = wx.Button(self.panelEditaConvenio, -1, u'Cancelar', pos=(250, 420))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitConvenioEdita)
        self.windowEditaConvenio.Bind(wx.EVT_CLOSE, self.quitConvenioEdita)

        self.windowEditaConvenio.Centre()
        self.windowEditaConvenio.Show()

    def quitConvenioEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaConvenio.Destroy()

    def editaInsereSiglaConvenio(self, event):

        self.message = wx.MessageDialog(None, u'O Número do convênio é alterado quando se muda o Tipo de convênio!', 'Info', wx.OK)
        self.message.ShowModal()
        self.tcNumeroConvenio.SetValue("")
        self.tcNumeroConvenio.SetValue(unicode(self.choicesSiglasConvenios[self.cbTipoConvenio.GetValue()]))

    def insereSiglaConvenio(self, event):

        self.tcNumeroConvenio.SetValue("")
        self.tcNumeroConvenio.SetValue(unicode(self.choicesSiglasConvenios[self.cbTipoConvenio.GetValue()]))

    def editarConvenio(self, event):

        if self.valida():

            self.convenio.recebeValor = unicode(self.cbRecebeValor.GetValue())
            self.convenio.numeroConvenio = unicode(self.tcNumeroConvenio.GetValue())
            self.convenio.valorConvenio = unicode(self.tcValorConvenio.GetValue())
            self.convenio.moedaConvenio = unicode(self.cbMoedaConvenio.GetValue())
            self.convenio.dataAssinaturaConvenio = unicode(self.tcDataAssinatura.GetValue())
            self.convenio.objetivoConvenio = unicode(self.tcObjetivoConvenio.GetValue())
            self.convenio.dataVencimentoConvenio = unicode(self.tcDataVencimento.GetValue())
            self.convenio.leiAutorizativa = unicode(self.tcLeiAutorizativa.GetValue())
            self.convenio.dataLeiAutorizativa = unicode(self.tcDataLeiAutorizativa.GetValue())
            self.convenio.numeroDiarioOficial = unicode(self.tcNumeroDiarioOficial.GetValue())
            self.convenio.dataPublicacaoConvenio = unicode(self.tcDataPublicacao.GetValue())
            self.convenio.tipoConvenio = unicode(self.cbTipoConvenio.GetValue())
            self.convenio.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'Convênio foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.convenio = None
            self.windowEditaConvenio.Close()

    def liberaMoedaValor(self, event):

        if event.GetString() == 'S':

            self.cbMoedaConvenio.Enable()
            self.tcValorConvenio.Enable()
        else:

            self.cbMoedaConvenio.SetSelection(0)
            self.tcValorConvenio.SetValue(0)
            self.cbMoedaConvenio.Disable()
            self.tcValorConvenio.Disable()

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

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

        if self.cbTipoConvenio.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo ', 'Info', wx.OK)
            self.cbTipoConvenio.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroConvenio.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número deve ser preenchido', 'Info', wx.OK)
            self.tcNumeroConvenio.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbRecebeValor.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Recebe Valor ', 'Info', wx.OK)
            self.cbRecebeValor.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbRecebeValor.GetValue() == u'S':

            if self.cbMoedaConvenio.GetSelection() == -1:

                self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Moeda', 'Info', wx.OK)
                self.cbMoedaConvenio.SetFocus()
                self.message.ShowModal()
                return 0

            if self.tcValorConvenio.GetValue() == 0.0:

                self.message = wx.MessageDialog(None, u'O campo Valor não pode ter o valor igual a 0', 'Info', wx.OK)
                self.tcValorConvenio.SetFocus()
                self.message.ShowModal()
                return 0

        if self.tcObjetivoConvenio.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Objetivo deve ser preenchido', 'Info', wx.OK)
            self.tcObjetivoConvenio.SetFocus()
            self.message.ShowModal()
            return 0

        
        if not self.validateDate(self.tcDataAssinatura.GetValue(), u'Data da Assinatura'):
            self.tcDataAssinatura.SelectAll()
            self.tcDataAssinatura.SetFocus()
            return 0

        if not self.validateDate(self.tcDataVencimento.GetValue(), u'Data de Vencimento'):
            self.tcDataVencimento.SelectAll()
            self.tcDataVencimento.SetFocus()
            return 0

        convenio = Convenio.query.filter_by(numeroConvenio=self.tcNumeroConvenio.GetValue()).first()

        if convenio != None:
            if (unicode(convenio.numeroConvenio.upper()) == unicode(self.tcNumeroConvenio.GetValue().upper())) and (convenio.id == int(self.tcId.GetValue())):
                pass
            else:
                self.message = wx.MessageDialog(None, u'Já existe um convênio com a numeração: '+self.tcNumeroConvenio.GetValue()+u'!', 'Info', wx.OK)
                self.tcNumeroConvenio.SelectAll()
                self.tcNumeroConvenio.SetFocus()
                self.message.ShowModal()
                return 0

        #verificar se os campos lei autorizativa e diario oficial e respectivas datas são obrigatórios

        return 1

    def salvarConvenio(self, event):

        if self.valida():

            try:
                Convenio(recebeValor=unicode(self.cbRecebeValor.GetValue()),
                    numeroConvenio=unicode(self.tcNumeroConvenio.GetValue()), valorConvenio=unicode(self.tcValorConvenio.GetValue()),
                    moedaConvenio=unicode(self.cbMoedaConvenio.GetValue()), dataAssinaturaConvenio=unicode(self.tcDataAssinatura.GetValue()),
                    objetivoConvenio=unicode(self.tcObjetivoConvenio.GetValue()), dataVencimentoConvenio=unicode(self.tcDataVencimento.GetValue()),
                    leiAutorizativa=unicode(self.tcLeiAutorizativa.GetValue()), dataLeiAutorizativa=unicode(self.tcDataLeiAutorizativa.GetValue()),
                    numeroDiarioOficial=unicode(self.tcNumeroDiarioOficial.GetValue()), dataPublicacaoConvenio=unicode(self.tcDataPublicacao.GetValue()),
                    tipoConvenio=unicode(self.cbTipoConvenio.GetValue()), competencia=unicode(self.cbCompetencia.GetValue())
                )

                session.commit()
                self.message = wx.MessageDialog(None, u'Convênio salvo com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoConvenio.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoConvenio.Close()

    def quitConvenioNovo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoConvenio.Destroy()

    def insereInCtrList(self, event):

        self.convenioListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            convenios = Convenio.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for convenio in convenios:

                index = self.convenioListCtrl.InsertStringItem(sys.maxint, unicode(convenio.numeroConvenio))
                self.convenioListCtrl.SetStringItem(index, 1, convenio.tipoConvenio)
                self.convenioListCtrl.SetStringItem(index, 2, convenio.objetivoConvenio)
                self.convenioListCtrl.SetStringItem(index, 3, unicode(convenio.id))

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.convenioListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def excluiConvenio(self, event, idConvenio):

        if idConvenio is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este convênio?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.convenio = Convenio.query.filter_by(id=idConvenio).first()
            self.convenio.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Convênio excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        self.tipoConvenio = {u'Delegação de recursos e encargos' : '1', u'Transferência voluntária' : '2', u'Termo de Convênio' : '3', 
            u'Termo de Denúncia' : '4', u'Termo de Cooperação Técnico e Científico' : '5', u'Termo de Cooperação Técnico e Financeiro' : '6', 
            u'Termo de Parceria' : '7', u'Termo Aditivo de Convênio' : '8', u'Termo Aditivo de Cooperação Técnico e Científico' : '9', 
            u'Termo Aditivo de Cooperação Técnico e Financeiro' : '10', u'Termo Aditivo de Parceria' : '11', u'Cessão' : '12', u'Aditivo de cessão' : '13',
            u'Termo de Responsabilidade' : '14', u'Termo Aditivo de Responsabilidade' : '15'}


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
        self.conveniosGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.conveniosGeraArquivoListCtrl.InsertColumn(0, u'Número do Convênio', width=130)
        self.conveniosGeraArquivoListCtrl.InsertColumn(1, u'Objetivo Convênio', width=120)
        self.conveniosGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.conveniosGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensConveniosGeraArquivos)

        self.btnIncluiGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.conveniosParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.conveniosParaArquivoListCtrl.InsertColumn(0, u'Número do Convênio', width=130)
        self.conveniosParaArquivoListCtrl.InsertColumn(1, u'Objetivo Convênio', width=120)
        self.conveniosParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.conveniosParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensConveniosParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereConvenioPorCompetencia(self, event):

        convenios = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            convenios = Convenio.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            convenios = Convenio.query.all()

        self.conveniosGeraArquivoListCtrl.DeleteAllItems()

        if not convenios:
            self.message = wx.MessageDialog(None, u'Não existe convênios para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(convenios) == self.conveniosParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for convenio in convenios:
                    igual = False

                    if self.conveniosParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.conveniosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(convenio.numeroConvenio))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(convenio.objetivoConvenio))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(convenio.id))
                        igual = True

                    else:

                        for x in range(self.conveniosParaArquivoListCtrl.GetItemCount()):

                            if convenio.numeroConvenio == unicode(self.conveniosParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.conveniosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(convenio.numeroConvenio))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(convenio.objetivoConvenio))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(convenio.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensConveniosGeraArquivos(self, event):

        item = self.conveniosGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.conveniosGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensConveniosParaArquivo(self, event):

        item = self.conveniosParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.conveniosParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os convênios a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.conveniosParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.conveniosGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.conveniosParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.conveniosGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.conveniosParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.conveniosGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.conveniosGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os convênios a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.conveniosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.conveniosParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.conveniosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.conveniosParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.conveniosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.conveniosParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.conveniosParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.conveniosParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os convênios para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="CONVENIO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        self.message = wx.MessageDialog(None, u'Após criar o arquivo de convênios é necessário gerar o arquivo de Participantes de Convênio!\n', 'Info', wx.OK | wx.ICON_EXCLAMATION)
                        self.message.ShowModal()

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de convênios gerados com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de convênios gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.conveniosParaArquivoListCtrl.GetItemCount()):

            try:

                idConvenio = int(self.conveniosParaArquivoListCtrl.GetItem(x, 2).GetText())
                convenio = Convenio.query.filter_by(id=idConvenio).first()

                f.write(unicode(convenio.recebeValor.zfill(1)))
                f.write(unicode(convenio.numeroConvenio.ljust(16).replace("'", "").replace("\"", "")))
                
                partes = convenio.valorConvenio.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((convenio.valorConvenio).zfill(16).replace(".", ",")))
                else:
                    f.write(unicode((convenio.valorConvenio+'0').zfill(16).replace(".", ",")))
                
                f.write(unicode(self.transformaCodigoMoeda(convenio.moedaConvenio).zfill(3)))
                f.write(unicode(self.transformaData(convenio.dataAssinaturaConvenio)))
                f.write(unicode(convenio.objetivoConvenio.ljust(300).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(convenio.dataVencimentoConvenio)))
                f.write(unicode(convenio.leiAutorizativa.zfill(6)))
                f.write(unicode(self.transformaData(convenio.dataLeiAutorizativa)))
                f.write(unicode(convenio.numeroDiarioOficial.zfill(6)))
                f.write(unicode(self.transformaData(convenio.dataPublicacaoConvenio)))
                f.write(unicode(self.transformaTipoConvenio(convenio.tipoConvenio).zfill(2)))
                f.write(u"\n")

            except:
                return 0

        f.close()
        return 1

    
    def transformaCodigoMoeda(self, moeda):
        if moeda == u"Real":
            return "1"
        elif moeda == u"Dolar":
            return "3"
        else:
            return "9"

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]

    def transformaTipoConvenio(self, convenio):

        return self.tipoConvenio[convenio]
