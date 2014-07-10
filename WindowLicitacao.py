# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_LICITACAO_NOVO = 5001
ID_TOOLBAR_LICITACAO_EDITAR = 5002
ID_TOOLBAR_LICITACAO_EXCLUIR = 5003
ID_TOOLBAR_LICITACAO_CRIAR_ARQUIVO = 5004


class WindowLicitacao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelLicitacao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova licitação')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita licitação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui licitação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_LICITACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de licitação')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
            u'Outubro', u'Novembro',u'Dezembro']

        self.modalidadeLicitacao = [u'Dispensa p/Compra e Serviços (Compra direta)', u'Convite p/ Compras e Serviços',
            u'Convite p/ Obras e Serviços de Engenharia', u'Tomada de Preços p/ Compras e Serviços',
            u'Tomada de Preços p/ Obras e Serviços Engenharia', u'Concorrência p/ Compras e Serviços',
            u'Concorrência p/ Obras e Serviços de Engenharia', u'Leilão', u'Dispensa de Licitação',
            u'Inexigibilidade de Licitação', u'Concurso', u'Pregão Eletrônico',u'Pregão Presencial',
            u'Concorrência para concessão adm. de uso', u'Concorrência para concessão de dir. uso', u'Anulada', 
            u'Deserta', u'Fracassada', u'Internacional']

        self.siglaModalidadeLicitacao = {u'Dispensa p/Compra e Serviços (Compra direta)': u'', u'Convite p/ Compras e Serviços': u'CC',
            u'Convite p/ Obras e Serviços de Engenharia': u'CC', u'Tomada de Preços p/ Compras e Serviços': u'TP',
            u'Tomada de Preços p/ Obras e Serviços Engenharia': u'TP', u'Concorrência p/ Compras e Serviços': u'CO',
            u'Concorrência p/ Obras e Serviços de Engenharia': u'CO', u'Leilão': u'LE', u'Dispensa de Licitação': u'DL',
            u'Inexigibilidade de Licitação': u'IL', u'Concurso': u'CP', u'Pregão Eletrônico': u'PE',u'Pregão Presencial': u'PR',
            u'Concorrência para concessão adm. de uso': u'CO', u'Concorrência para concessão de dir. uso': u'CO', u'Anulada': u'LA', 
            u'Deserta': u'LD', u'Fracassada': u'LF', u'Internacional': u'IN'}

        self.cbCompetenciaForView = wx.ComboBox(self.panelLicitacao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.licitacaoListCtrl = wx.ListCtrl(self.panelLicitacao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.licitacaoListCtrl.InsertColumn(0, u'Proc. Licitatório', width=100)
        self.licitacaoListCtrl.InsertColumn(1, u'Modalidade', width=200)
        self.licitacaoListCtrl.InsertColumn(2, u'Descrição', width=220)
        self.licitacaoListCtrl.InsertColumn(3, u'', width=0)
        self.licitacaoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.licitacaoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.licitacaoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoLicitacao, id=ID_TOOLBAR_LICITACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaLicitacao(event, self.idSelecionado), id=ID_TOOLBAR_LICITACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiLicitacao(event, self.idSelecionado), id=ID_TOOLBAR_LICITACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_LICITACAO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.licitacaoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def insereInCtrList(self, event):

        self.licitacaoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            licitacoes = Licitacao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for licitacao in licitacoes:

                index = self.licitacaoListCtrl.InsertStringItem(sys.maxint, unicode(licitacao.numeroProcessoLicitatorio))
                self.licitacaoListCtrl.SetStringItem(index, 1, licitacao.modalidadeLicitacao)
                self.licitacaoListCtrl.SetStringItem(index, 2, licitacao.descricaoLicitacao)
                self.licitacaoListCtrl.SetStringItem(index, 3, unicode(licitacao.id))

    def novoLicitacao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoLicitacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 380), pos=(300, 170), title=u'Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoLicitacao = wx.Panel(self.windowNovoLicitacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoLicitacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoLicitacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoLicitacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)

        wx.StaticBox(self.panelNovoLicitacao, -1, pos=(5, 50), size=(480, 250))

        self.stTipoLicitacao = wx.StaticText(self.panelNovoLicitacao, -1, u'Tipo Licitação', pos=(10, 70))
        self.cbTipoLicitacao = wx.ComboBox(self.panelNovoLicitacao, -1, pos=(10, 90), size=(70, -1), choices=[u'Item', u'Lote'], style=wx.CB_READONLY)

        self.stModalidadeLicitacao = wx.StaticText(self.panelNovoLicitacao, -1, u'Modalidade', pos=(120, 70))
        self.cbModalidadeLicitacao = wx.ComboBox(self.panelNovoLicitacao, -1, pos=(120, 90), size=(280, -1), choices=self.modalidadeLicitacao, style=wx.CB_READONLY)
        self.cbModalidadeLicitacao.Bind(wx.EVT_COMBOBOX, self.insereSiglaLicitacao)

        self.stNumeroProcesso = wx.StaticText(self.panelNovoLicitacao, -1, u'Número Proc. Licitatório', pos=(10, 130))
        self.tcNumeroProcesso = wx.TextCtrl(self.panelNovoLicitacao, -1, pos=(10, 150), size=(120, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroProcesso.SetMaxLength(18)

        self.stDescricaoLicitacao = wx.StaticText(self.panelNovoLicitacao, -1, u'Descrição da Licitação', pos=(150, 130))
        self.tcDescricaoLicitacao = wx.TextCtrl(self.panelNovoLicitacao, -1, pos=(150, 150), size=(320, -1), style=wx.ALIGN_LEFT)
        self.tcDescricaoLicitacao.SetMaxLength(300)

        self.stNumeroEdital = wx.StaticText(self.panelNovoLicitacao, -1, u'Num. Edital Licitação', pos=(10, 190))
        self.tcNumeroEdital = wx.TextCtrl(self.panelNovoLicitacao, -1, pos=(10, 210), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroEdital.SetMaxLength(16)

        self.stDataPublicacao = wx.StaticText(self.panelNovoLicitacao, -1, u'Data de Public. Edital', pos=(200, 190))
        self.tcDataPublicacao = masked.TextCtrl(self.panelNovoLicitacao, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((200, 210))

        self.stValorDespesa = wx.StaticText(self.panelNovoLicitacao, -1, u'Valor', pos=(350, 190))
        self.tcValorDespesa = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoLicitacao, pos=wx.Point(350, 210), style=0, value=0)
        self.tcValorDespesa.SetFractionWidth(2)
        self.tcValorDespesa.SetGroupChar(u"#")
        self.tcValorDespesa.SetDecimalChar(u",")
        self.tcValorDespesa.SetGroupChar(u".")
        self.tcValorDespesa.SetAllowNegative(False)

        self.stDiarioOficial = wx.StaticText(self.panelNovoLicitacao, -1, u'Num. Diário Oficial', pos=(10, 250))
        self.tcDiarioOficial = wx.TextCtrl(self.panelNovoLicitacao, -1, pos=(10, 270), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcDiarioOficial.SetMaxLength(6)
        self.tcDiarioOficial.Bind(wx.EVT_CHAR, self.escapaChar)

        self.btnSalvar = wx.Button(self.panelNovoLicitacao, -1, u"Salvar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarLicitacao)
        self.btnCancelar = wx.Button(self.panelNovoLicitacao, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoLicitacao)

        #Bind
        self.windowNovoLicitacao.Bind(wx.EVT_CLOSE, self.quitNovoLicitacao)

        self.windowNovoLicitacao.Centre()
        self.windowNovoLicitacao.Show()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_LICITACAO_CRIAR_ARQUIVO, gerar)

    def quitNovoLicitacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoLicitacao.Destroy()

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def insereSiglaLicitacao(self, event):

        self.tcNumeroProcesso.SetValue("")
        self.tcNumeroProcesso.SetValue(unicode(self.siglaModalidadeLicitacao[self.cbModalidadeLicitacao.GetValue()]))

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

        if self.cbTipoLicitacao.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Licitação', 'Info', wx.OK)
            self.cbTipoLicitacao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbModalidadeLicitacao.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Modalidade', 'Info', wx.OK)
            self.cbModalidadeLicitacao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroProcesso.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Número Proc. Licitatório deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroProcesso.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcDescricaoLicitacao.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Descrição da Licitação deve ser preenchido!', 'Info', wx.OK)
            self.tcDescricaoLicitacao.SetFocus()
            self.message.ShowModal()
            return 0

        #if self.tcNumeroEdital.GetValue() == '':

        #    self.message = wx.MessageDialog(None, u'O campo Num. Edital Licitação deve ser preenchido!', 'Info', wx.OK)
        #    self.tcNumeroEdital.SetFocus()
        #    self.message.ShowModal()
        #    return 0

        #if self.validateDate(self.tcDataPublicacao.GetValue(), u'Data de Public. Edital'):

        #    self.tcDataPublicacao.SelectAll()
        #    self.tcDataPublicacao.SetFocus()

        #if self.tcValorDespesa.GetValue() == 0.0:

        #    self.message = wx.MessageDialog(None, u'O campo Valor não pode ter o valor igual a 0 !', 'Info', wx.OK)
        #    self.tcValorDespesa.SetFocus()
        #    self.message.ShowModal()
        #    return 0

        #if self.tcDiarioOficial.GetValue() == '':

        #    self.message = wx.MessageDialog(None, u'O campo Num. Diário Oficial não pode ter o valor igual a 0 !', 'Info', wx.OK)
        #    self.tcDiarioOficial.SetFocus()
        #    self.message.ShowModal()
        #    return 0

        licitacao = Licitacao.query.filter_by(numeroProcessoLicitatorio=self.tcNumeroProcesso.GetValue()).first()

        if licitacao != None:
            if (unicode(licitacao.numeroProcessoLicitatorio.upper()) == unicode(self.tcNumeroProcesso.GetValue().upper())) and (licitacao.id == int(self.tcId.GetValue())):
                pass
            else:
                self.message = wx.MessageDialog(None, u'Já existe uma Licitação com o Número de Processo Licitatório: '+self.tcNumeroProcesso.GetValue()+u'!', 'Info', wx.OK)
                self.tcNumeroProcesso.SelectAll()
                self.tcNumeroProcesso.SetFocus()
                self.message.ShowModal()
                return 0

        #verificar se os campos lei autorizativa e diario oficial e respectivas datas são obrigatórios

        return 1

    def salvarLicitacao(self, event):

        if self.valida():
            Licitacao(
                numeroProcessoLicitatorio=unicode(self.tcNumeroProcesso.GetValue()),
                numeroDiarioOficial=unicode(self.tcDiarioOficial.GetValue()),
                dataLicitacao=unicode(self.tcDataPublicacao.GetValue()),
                modalidadeLicitacao=unicode(self.cbModalidadeLicitacao.GetValue()),
                descricaoLicitacao=unicode(self.tcDescricaoLicitacao.GetValue()),
                valorDespesa=unicode(self.tcValorDespesa.GetValue()),
                numeroEditalLicitacao=unicode(self.tcNumeroEdital.GetValue()),
                tipoLicitacao=unicode(self.cbTipoLicitacao.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue())

            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Licitação salva com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.windowNovoLicitacao.Close()

    def vizualizaLicitacao(self, event, idLicitacao):

        if idLicitacao is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Licitação foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.licitacao = Licitacao.query.filter_by(id=idLicitacao).first()

        self.windowEditaLicitacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 380), pos=(300, 170), title=u'Licitação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaLicitacao = wx.Panel(self.windowEditaLicitacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelEditaLicitacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.licitacao.id))

        self.stCompetencia = wx.StaticText(self.panelEditaLicitacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaLicitacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.licitacao.competencia)

        wx.StaticBox(self.panelEditaLicitacao, -1, pos=(5, 50), size=(480, 250))

        self.stTipoLicitacao = wx.StaticText(self.panelEditaLicitacao, -1, u'Tipo Licitação', pos=(10, 70))
        self.cbTipoLicitacao = wx.ComboBox(self.panelEditaLicitacao, -1, pos=(10, 90), size=(70, -1), choices=[u'Item', u'Lote'], style=wx.CB_READONLY)
        self.cbTipoLicitacao.SetValue(self.licitacao.tipoLicitacao)

        self.stModalidadeLicitacao = wx.StaticText(self.panelEditaLicitacao, -1, u'Modalidade', pos=(120, 70))
        self.cbModalidadeLicitacao = wx.ComboBox(self.panelEditaLicitacao, -1, pos=(120, 90), size=(280, -1), choices=self.modalidadeLicitacao, style=wx.CB_READONLY)
        self.cbModalidadeLicitacao.Bind(wx.EVT_COMBOBOX, self.editaInsereSiglaLicitacao)
        self.cbModalidadeLicitacao.SetValue(self.licitacao.modalidadeLicitacao)

        self.stNumeroProcesso = wx.StaticText(self.panelEditaLicitacao, -1, u'Número Proc. Licitatório', pos=(10, 130))
        self.tcNumeroProcesso = wx.TextCtrl(self.panelEditaLicitacao, -1, pos=(10, 150), size=(120, -1), style= wx.ALIGN_LEFT)
        self.tcNumeroProcesso.SetMaxLength(18)
        self.tcNumeroProcesso.SetValue(self.licitacao.numeroProcessoLicitatorio)

        self.stDescricaoLicitacao = wx.StaticText(self.panelEditaLicitacao, -1, u'Descrição da Licitação', pos=(150, 130))
        self.tcDescricaoLicitacao = wx.TextCtrl(self.panelEditaLicitacao, -1, pos=(150, 150), size=(320, -1), style=wx.ALIGN_LEFT)
        self.tcDescricaoLicitacao.SetMaxLength(300)
        self.tcDescricaoLicitacao.SetValue(self.licitacao.descricaoLicitacao)

        self.stNumeroEdital = wx.StaticText(self.panelEditaLicitacao, -1, u'Num. Edital Licitação', pos=(10, 190))
        self.tcNumeroEdital = wx.TextCtrl(self.panelEditaLicitacao, -1, pos=(10, 210), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroEdital.SetMaxLength(16)
        self.tcNumeroEdital.SetValue(self.licitacao.numeroEditalLicitacao)

        self.stDataPublicacao = wx.StaticText(self.panelEditaLicitacao, -1, u'Data de Public. Edital', pos=(200, 190))
        self.tcDataPublicacao = masked.TextCtrl(self.panelEditaLicitacao, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((200, 210))
        self.tcDataPublicacao.SetValue(self.licitacao.dataLicitacao)

        self.stValorDespesa = wx.StaticText(self.panelEditaLicitacao, -1, u'Valor', pos=(350, 190))
        self.tcValorDespesa = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaLicitacao, pos=wx.Point(350, 210), style=0, value=0)
        self.tcValorDespesa.SetFractionWidth(2)
        self.tcValorDespesa.SetGroupChar(u"#")
        self.tcValorDespesa.SetDecimalChar(u",")
        self.tcValorDespesa.SetGroupChar(u".")
        self.tcValorDespesa.SetAllowNegative(False)
        self.tcValorDespesa.SetValue(float(self.licitacao.valorDespesa))

        self.stDiarioOficial = wx.StaticText(self.panelEditaLicitacao, -1, u'Num. Diário Oficial', pos=(10, 250))
        self.tcDiarioOficial = wx.TextCtrl(self.panelEditaLicitacao, -1, pos=(10, 270), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcDiarioOficial.SetMaxLength(6)
        self.tcDiarioOficial.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcDiarioOficial.SetValue(self.licitacao.numeroDiarioOficial)

        self.btnSalvar = wx.Button(self.panelEditaLicitacao, -1, u"Alterar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarLicitacao)
        self.btnCancelar = wx.Button(self.panelEditaLicitacao, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEditaLicitacao)

        #Bind
        self.windowEditaLicitacao.Bind(wx.EVT_CLOSE, self.quitEditaLicitacao)

        self.windowEditaLicitacao.Centre()
        self.windowEditaLicitacao.Show()

    def quitEditaLicitacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaLicitacao.Destroy()

    def editaInsereSiglaLicitacao(self, event):

        self.message = wx.MessageDialog(None, u'O Número do Processo Licitatório é alterado quando se muda a Modalidade de licitação!', 'Info', wx.OK)
        self.message.ShowModal()
        self.insereSiglaLicitacao(None)

    def editarLicitacao(self, event):

        if self.valida():

            self.licitacao.numeroProcessoLicitatorio = unicode(self.tcNumeroProcesso.GetValue())
            self.licitacao.numeroDiarioOficial = unicode(self.tcDiarioOficial.GetValue())
            self.licitacao.dataLicitacao = unicode(self.tcDataPublicacao.GetValue())
            self.licitacao.modalidadeLicitacao = unicode(self.cbModalidadeLicitacao.GetValue())
            self.licitacao.descricaoLicitacao = unicode(self.tcDescricaoLicitacao.GetValue())
            self.licitacao.valorDespesa = unicode(self.tcValorDespesa.GetValue())
            self.licitacao.numeroEditalLicitacao = unicode(self.tcNumeroEdital.GetValue())
            self.licitacao.tipoLicitacao = unicode(self.cbTipoLicitacao.GetValue())
            self.licitacao.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'A Licitação foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.licitacao = None
            self.windowEditaLicitacao.Close()

    def excluiLicitacao(self, event, idLicitacao):

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta licitação?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.licitacao = Licitacao.query.filter_by(id=idLicitacao).first()
            self.licitacao.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Licitação excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Licitação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        self.modalidadeCodigo = {u'Dispensa p/Compra e Serviços (Compra direta)': u'0', u'Convite p/ Compras e Serviços': u'1',
            u'Convite p/ Obras e Serviços de Engenharia': u'2', u'Tomada de Preços p/ Compras e Serviços': u'3',
            u'Tomada de Preços p/ Obras e Serviços Engenharia': u'4', u'Concorrência p/ Compras e Serviços': u'5',
            u'Concorrência p/ Obras e Serviços de Engenharia': u'6', u'Leilão': u'7', u'Dispensa de Licitação': u'8',
            u'Inexigibilidade de Licitação': u'9', u'Concurso': u'10', u'Pregão Eletrônico': u'11',u'Pregão Presencial': u'12',
            u'Concorrência para concessão adm. de uso': u'13', u'Concorrência para concessão de dir. uso': u'14', u'Anulada': u'15', 
            u'Deserta': u'16', u'Fracassada': u'17', u'Internacional': u'18'}

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
        self.licitacaoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.licitacaoGeraArquivoListCtrl.InsertColumn(0, u'Num. Processo Licit.', width=130)
        self.licitacaoGeraArquivoListCtrl.InsertColumn(1, u'Descrição', width=120)
        self.licitacaoGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.licitacaoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.licitacaoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.licitacaoParaArquivoListCtrl.InsertColumn(0, u'Num. Processo Licit.', width=130)
        self.licitacaoParaArquivoListCtrl.InsertColumn(1, u'Descrição', width=120)
        self.licitacaoParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.licitacaoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereConvenioPorCompetencia(self, event):

        licitacoes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            licitacoes = Licitacao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            licitacoes = Licitacao.query.all()

        self.licitacaoGeraArquivoListCtrl.DeleteAllItems()

        if not licitacoes:
            self.message = wx.MessageDialog(None, u'Não existe Licitações para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(licitacoes) == self.licitacaoParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for licitacao in licitacoes:
                    igual = False
                    if self.licitacaoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.licitacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(licitacao.numeroProcessoLicitatorio))
                        self.licitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(licitacao.descricaoLicitacao))
                        self.licitacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(licitacao.id))
                        igual = True

                    else:

                        for x in range(self.licitacaoParaArquivoListCtrl.GetItemCount()):

                            if licitacao.numeroProcessoLicitatorio == unicode(self.licitacaoParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.licitacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(licitacao.numeroProcessoLicitatorio))
                        self.licitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(licitacao.descricaoLicitacao))
                        self.licitacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(licitacao.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensLicitacaoGeraArquivos(self, event):

        item = self.licitacaoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.licitacaoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensLicitacaoParaArquivo(self, event):

        item = self.licitacaoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.licitacaoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Licitações a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.licitacaoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.licitacaoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.licitacaoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.licitacaoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.licitacaoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.licitacaoGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.licitacaoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as licitações a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.licitacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.licitacaoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.licitacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.licitacaoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.licitacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.licitacaoParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.licitacaoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.licitacaoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Licitações para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="LICITACAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de Licitações gerados com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Licitações gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.licitacaoParaArquivoListCtrl.GetItemCount()):

            try:

                idLicitacao = int(self.licitacaoParaArquivoListCtrl.GetItem(x, 2).GetText())
                licitacao = Licitacao.query.filter_by(id=idLicitacao).first()

                f.write(unicode(licitacao.numeroProcessoLicitatorio.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(licitacao.numeroDiarioOficial.zfill(6)))
                f.write(unicode(self.transformaData(licitacao.dataLicitacao)))
                f.write(unicode(self.transformaModalidade(licitacao.modalidadeLicitacao).zfill(2)))
                f.write(unicode(licitacao.descricaoLicitacao.ljust(300).replace("'", "").replace("\"", "")))
                
                partes = licitacao.valorDespesa.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((licitacao.valorDespesa).zfill(16).replace(".", ",")))
                
                else:
                    f.write(unicode((licitacao.valorDespesa+'0').zfill(16).replace(".", ",")))
                
                f.write(unicode(licitacao.numeroEditalLicitacao.ljust(16).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaTipo(licitacao.tipoLicitacao)))
                f.write(u'\n')

            except:
                return 0

        return 1

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]

    def transformaModalidade(self, modalidade):

        return self.modalidadeCodigo[modalidade]

    def transformaTipo(self, tipo):

        if tipo == 'Item':
            return 'I'
        else:
            return 'L'
