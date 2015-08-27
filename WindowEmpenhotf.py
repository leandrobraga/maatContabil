# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_EMPENHOTV_NOVO = 3001
ID_TOOLBAR_EMPENHOTV_EDITAR = 3002
ID_TOOLBAR_EMPENHOTV_EXCLUIR = 3003
ID_TOOLBAR_EMPENHO_CRIARTV_ARQUIVO = 3004


class WindowEmpenhotf(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelConvenio = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHOTV_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHOTV_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHOTV_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui  selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_EMPENHO_CRIARTV_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo ')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesTipoTransf = [u'Termo de Colaboracao', u'Termo de Fomento',
            u'Termo de Convenio', u'Termo de Parceria ', u'Contrato de Gestao ', u'Termo de Responsabilidade',
            u'Termo de Cooperacao Tecnica', u'Outras transferencias voluntarias', u'Aditivo – Valor', u'Aditivo – Vigencia', 
            u'Outros aditivos']

        self.choicestipoParticipacao = [u'Concendente/Repassador', u'Convenente/OSC']

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro', 
            u'Outubro', u'Novembro',u'Dezembro']


        self.cbCompetenciaForView = wx.ComboBox(self.panelConvenio, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.convenioListCtrl = wx.ListCtrl(self.panelConvenio, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.convenioListCtrl.InsertColumn(0, u"Número Transferencia", width=120)
        self.convenioListCtrl.InsertColumn(1, u"Numero Empenho", width=180)
        self.convenioListCtrl.InsertColumn(2, u"Ano", width=220)
        self.convenioListCtrl.InsertColumn(3, u'', width=0)
        self.convenioListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.convenioListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.convenioListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoConvenio, id=ID_TOOLBAR_EMPENHOTV_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaConvenio(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHOTV_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiConvenio(event, self.idSelecionado), id=ID_TOOLBAR_EMPENHOTV_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_EMPENHO_CRIARTV_ARQUIVO)
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

        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHOTV_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHOTV_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHOTV_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_EMPENHO_CRIARTV_ARQUIVO, gerar)

    def novoConvenio(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoConvenio = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(450, 510), pos=(300, 170), title=u"Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoConvenio = wx.Panel(self.windowNovoConvenio, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoConvenio, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)

        self.stNumTransf = wx.StaticText(self.panelNovoConvenio, -1, u'Número da Transferência Voluntária', pos=(10, 50), style=wx.ALIGN_LEFT)
        self.tcNumTransf = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumTransf.SetMaxLength(20)

        self.stNumeroEmpenho = wx.StaticText(self.panelNovoConvenio, -1, u'Número da nota de empenho', pos=(220, 50), style=wx.ALIGN_LEFT)
        self.tcNumeroEmpenho = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(220, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroEmpenho.SetMaxLength(10)

        self.stAno = wx.StaticText(self.panelNovoConvenio, -1, u'Ano do Empenho', pos=(10, 110), style=wx.ALIGN_LEFT)
        self.tcAno = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 130), size=(90, -1), style=wx.ALIGN_LEFT)
        self.tcAno.SetMaxLength(4)
        self.tcAno.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stCodigo = wx.StaticText(self.panelNovoConvenio, -1, u'Código da un. orçamentaria', pos=(140, 110), style=wx.ALIGN_LEFT)
        self.tcCodigo = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(140, 130), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigo.SetMaxLength(6)

        self.stTipoPart = wx.StaticText(self.panelNovoConvenio, -1, u'Tipo de participação na Transf. Vol.', pos=(10, 170))
        self.cbTipoPart = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 190), size=(180, -1), choices=self.choicestipoParticipacao, style=wx.CB_READONLY)

        self.stTipoInstrumento = wx.StaticText(self.panelNovoConvenio, -1, u'Tipo do Instrumento de Transferência', pos=(210, 170))
        self.cbTipoInstrumento = wx.ComboBox(self.panelNovoConvenio, -1, pos=(210, 190), size=(200, -1), choices=self.choicesTipoTransf, style=wx.CB_READONLY)

        self.stAnoTansf = wx.StaticText(self.panelNovoConvenio, -1, u'Ano do Transferencia', pos=(10,230), style=wx.ALIGN_LEFT)
        self.tcAnoTansf = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 250), size=(90, -1), style=wx.ALIGN_LEFT)
        self.tcAnoTansf.SetMaxLength(4)
        self.tcAnoTansf.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stCnpj = wx.StaticText(self.panelNovoConvenio, -1, u'CNPJ do Convenente/OSC', pos=(200, 230), style=wx.ALIGN_LEFT)
        self.tcCnpj = masked.TextCtrl(self.panelNovoConvenio, -1, mask="##.###.###/####-##")
        self.tcCnpj.SetSize((150, -1))
        self.tcCnpj.SetPosition((200, 250))

        self.btnSalvar = wx.Button(self.panelNovoConvenio, -1, u'Salvar', pos=(150, 350))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarConvenio)
        self.btnCancelar = wx.Button(self.panelNovoConvenio, -1, u'Cancelar', pos=(250, 350))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitConvenioNovo)
        self.windowNovoConvenio.Bind(wx.EVT_CLOSE, self.quitConvenioNovo)

        self.windowNovoConvenio.Centre()
        self.windowNovoConvenio.Show()

    def vizualizaConvenio(self, event, idConvenio):

        if idConvenio is None:
            self.message = wx.MessageDialog(None, u'Nenhum convênio foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.empenho = EmpenhoTV.query.filter_by(id=idConvenio).first()

        self.toolBarControler(False, False, False, False)

        self.windowEditaConvenio = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(450, 510), pos=(300, 170), title=u"Empenho", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoConvenio = wx.Panel(self.windowEditaConvenio, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.empenho.id))

        self.stCompetencia = wx.StaticText(self.panelNovoConvenio, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.empenho.competencia)

        self.stNumTransf = wx.StaticText(self.panelNovoConvenio, -1, u'Número da Transferência Voluntária', pos=(10, 50), style=wx.ALIGN_LEFT)
        self.tcNumTransf = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumTransf.SetMaxLength(20)
        self.tcNumTransf.SetValue(self.empenho.numTransf)

        self.stNumeroEmpenho = wx.StaticText(self.panelNovoConvenio, -1, u'Número da nota de empenho', pos=(220, 50), style=wx.ALIGN_LEFT)
        self.tcNumeroEmpenho = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(220, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroEmpenho.SetMaxLength(10)
        self.tcNumeroEmpenho.SetValue(self.empenho.numeroEmpenho)

        self.stAno = wx.StaticText(self.panelNovoConvenio, -1, u'Ano do Empenho', pos=(10, 110), style=wx.ALIGN_LEFT)
        self.tcAno = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 130), size=(90, -1), style=wx.ALIGN_LEFT)
        self.tcAno.SetMaxLength(4)
        self.tcAno.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAno.SetValue(self.empenho.ano)

        self.stCodigo = wx.StaticText(self.panelNovoConvenio, -1, u'Código da un. orçamentaria', pos=(140, 110), style=wx.ALIGN_LEFT)
        self.tcCodigo = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(140, 130), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigo.SetMaxLength(6)
        self.tcCodigo.SetValue(self.empenho.codigo)

        self.stTipoPart = wx.StaticText(self.panelNovoConvenio, -1, u'Tipo de participação na Transf. Vol.', pos=(10, 170))
        self.cbTipoPart = wx.ComboBox(self.panelNovoConvenio, -1, pos=(10, 190), size=(180, -1), choices=self.choicestipoParticipacao, style=wx.CB_READONLY)
        self.cbTipoPart.SetValue(self.empenho.tipoPart)

        self.stTipoInstrumento = wx.StaticText(self.panelNovoConvenio, -1, u'Tipo do Instrumento de Transferência', pos=(210, 170))
        self.cbTipoInstrumento = wx.ComboBox(self.panelNovoConvenio, -1, pos=(210, 190), size=(200, -1), choices=self.choicesTipoTransf, style=wx.CB_READONLY)
        self.cbTipoInstrumento.SetValue(self.empenho.tipoInstrumento)

        self.stAnoTansf = wx.StaticText(self.panelNovoConvenio, -1, u'Ano do Transferencia', pos=(10,230), style=wx.ALIGN_LEFT)
        self.tcAnoTansf = wx.TextCtrl(self.panelNovoConvenio, -1, pos=(10, 250), size=(90, -1), style=wx.ALIGN_LEFT)
        self.tcAnoTansf.SetMaxLength(4)
        self.tcAnoTansf.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAnoTansf.SetValue(self.empenho.anoTansf)

        self.stCnpj = wx.StaticText(self.panelNovoConvenio, -1, u'CNPJ do Convenente/OSC', pos=(200, 230), style=wx.ALIGN_LEFT)
        self.tcCnpj = masked.TextCtrl(self.panelNovoConvenio, -1, mask="##.###.###/####-##")
        self.tcCnpj.SetSize((150, -1))
        self.tcCnpj.SetPosition((200, 250))
        self.tcCnpj.SetValue(self.empenho.cnpj)

        self.btnSalvar = wx.Button(self.panelNovoConvenio, -1, u'Salvar', pos=(150, 350))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarConvenio)
        self.btnCancelar = wx.Button(self.panelNovoConvenio, -1, u'Cancelar', pos=(250, 350))
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

        #if self.valida():

        self.empenho.numTransf = unicode(self.tcNumTransf.GetValue())
        self.empenho.numeroEmpenho = unicode(self.tcNumeroEmpenho.GetValue())
        self.empenho.ano = unicode(self.tcAno.GetValue())
        self.empenho.codigo = unicode(self.tcCodigo.GetValue())
        self.empenho.tipoPart = unicode(self.cbTipoPart.GetValue())
        self.empenho.tipoInstrumento = unicode(self.cbTipoInstrumento.GetValue())
        self.empenho.anoTansf = unicode(self.tcAnoTansf.GetValue())
        self.empenho.cnpj = unicode(self.tcCnpj.GetValue())
        self.empenho.competencia = unicode(self.cbCompetencia.GetValue())

        session.commit()
        self.message = wx.MessageDialog(None, u'Empenho foi alterado com sucesso!', 'Info', wx.OK)
        self.message.ShowModal()
        self.insereInCtrList(None)
        self.empenho = None
        self.windowEditaConvenio.Close()

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

        #if self.valida():

        try:
            EmpenhoTV(

                numTransf=unicode(self.tcNumTransf.GetValue()),
                numeroEmpenho=unicode(self.tcNumeroEmpenho.GetValue()),
                ano=unicode(self.tcAno.GetValue()),
                codigo=unicode(self.tcCodigo.GetValue()),
                tipoPart=unicode(self.cbTipoPart.GetValue()),
                tipoInstrumento=unicode(self.cbTipoInstrumento.GetValue()),
                anoTansf=unicode(self.tcAnoTansf.GetValue()),
                cnpj=unicode(self.tcCnpj.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue())
            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Empenho salvo com sucesso!', 'Info', wx.OK)
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
            convenentes = EmpenhoTV.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for empenho in convenentes:

                index = self.convenioListCtrl.InsertStringItem(sys.maxint, unicode(empenho.numTransf))
                self.convenioListCtrl.SetStringItem(index, 1, empenho.numeroEmpenho)
                self.convenioListCtrl.SetStringItem(index, 2, empenho.ano)
                self.convenioListCtrl.SetStringItem(index, 3, unicode(empenho.id))

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.convenioListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def excluiConvenio(self, event, idConvenio):

        if idConvenio is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este Empenho?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.empenho = EmpenhoTV.query.filter_by(id=idConvenio).first()
            self.empenho.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Empenho excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
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
        self.conveniosGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.conveniosGeraArquivoListCtrl.InsertColumn(0, u'Numero Transf.', width=130)
        self.conveniosGeraArquivoListCtrl.InsertColumn(1, u'Numero EMpenho', width=120)
        self.conveniosGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.conveniosGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensConveniosGeraArquivos)

        self.btnIncluiGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.conveniosParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.conveniosParaArquivoListCtrl.InsertColumn(0, u'Numero Transf.', width=130)
        self.conveniosParaArquivoListCtrl.InsertColumn(1, u'Numero EMpenho', width=120)
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

            convenios = EmpenhoTV.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
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

                for empenho in convenios:
                    igual = False

                    if self.conveniosParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.conveniosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.numTransf))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(empenho.numeroEmpenho))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(empenho.id))
                        igual = True

                    else:

                        for x in range(self.conveniosParaArquivoListCtrl.GetItemCount()):

                            if convenio.numeroConvenio == unicode(self.conveniosParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.conveniosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(empenho.numTransf))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(empenho.numeroEmpenho))
                        self.conveniosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(empenho.id))

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

            self.message = wx.MessageDialog(None, u'Selecione os convenentes para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="TRANSFERENCIAVOLUNTARIAEMPENHO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                       

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de empenhos gerados com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de empenhos gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        
    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.conveniosParaArquivoListCtrl.GetItemCount()):

            try:

                idConvenio = int(self.conveniosParaArquivoListCtrl.GetItem(x, 2).GetText())
                empenho = EmpenhoTV.query.filter_by(id=idConvenio).first()

                f.write(unicode(empenho.numTransf).ljust(20).replace("'", "").replace("\"", ""))
                f.write(unicode(empenho.numeroEmpenho).ljust(10).replace("'", "").replace("\"", ""))
                f.write(unicode(empenho.ano).zfill(4))
                f.write(unicode(empenho.codigo).ljust(6).replace("'", "").replace("\"", ""))
                f.write(unicode(self.getTipo(empenho.tipoPart)).zfill(1))
                f.write(unicode(self.tipoInstrumento(empenho.tipoInstrumento)).zfill(3))
                f.write(unicode(empenho.anoTansf).zfill(4))
                f.write(unicode(self.retiraCaracteresCpfCnpj(empenho.cnpj)).zfill(14))

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


    def getTipo(self, tipo):
        return self.choicestipoParticipacao.index(tipo)+1

    def tipoInstrumento(self, tipo):
        return self.choicesTipoTransf.index(tipo)+1