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

ID_TOOLBAR_PARTICIPANTE_CONVENIO_NOVO = 4001
ID_TOOLBAR_PARTICIPANTE_CONVENIO_EDITAR = 4002
ID_TOOLBAR_PARTICIPANTE_CONVENIO_EXCLUIR = 4003
ID_TOOLBAR_PARTICIPANTE_CONVENIO_CRIAR_ARQUIVO = 4004


class WindowParticipanteConvenio(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Participantes de Convênios", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelParticipante = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona novo convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui convênio selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de convênio')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.choicesTipoJuridico = [u'Física', u'Jurídica', u'Outros']

        self.choicesEsferaConvenio = [u'Federal', u'Estadual', u'Municipal', u'ONGs', u'Outros']

        self.cbCompetenciaForView = wx.ComboBox(self.panelParticipante, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.participanteListCtrl = wx.ListCtrl(self.panelParticipante, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.participanteListCtrl.InsertColumn(0, u"Nome do Participante", width=200)
        self.participanteListCtrl.InsertColumn(1, u"CPF/CNPJ", width=145)
        self.participanteListCtrl.InsertColumn(2, u"Número do Convênio", width=180)
        self.participanteListCtrl.InsertColumn(3, u'', width=0)
        self.participanteListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.participanteListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.capturaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.participanteListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoParticipante, id=ID_TOOLBAR_PARTICIPANTE_CONVENIO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaParticipante(event, self.idSelecionado), id=ID_TOOLBAR_PARTICIPANTE_CONVENIO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiParticipante(event, self.idSelecionado), id=ID_TOOLBAR_PARTICIPANTE_CONVENIO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_PARTICIPANTE_CONVENIO_CRIAR_ARQUIVO)
        #Fim Binds

        self.Centre()
        self.Show()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_PARTICIPANTE_CONVENIO_CRIAR_ARQUIVO, gerar)

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.participanteListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def novoParticipante(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoParticipante = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(380, 710), pos=(300, 170), title=u"Participante de Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoParticipante = wx.Panel(self.windowNovoParticipante, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoParticipante, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.inserNumeroConvenio)

        wx.StaticBox(self.panelNovoParticipante, -1, pos=(3, 50), size=(360, 220))

        self.stNumeroConvenio = wx.StaticText(self.panelNovoParticipante, -1, u'Número do Convênio', pos=(10, 65))
        self.cbNumeroConvenio = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 85), size=(120, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroConvenio.Disable()

        self.stEsferaConveniado = wx.StaticText(self.panelNovoParticipante, -1, u'Esfera do Conveniado', pos=(180, 65))
        self.cbEsferaConveniado = wx.ComboBox(self.panelNovoParticipante, -1,  pos=(180, 85), size=(120, -1), choices=self.choicesEsferaConvenio, style=wx.CB_READONLY)
        
        self.stTipoJuridicoParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'Tipo Pessoa', pos=(10, 115), style=wx.ALIGN_LEFT)
        self.cbTipoJuridicoParticipante = wx.ComboBox(self.panelNovoParticipante, -1, pos=(10, 135), size=(150, -1), choices=self.choicesTipoJuridico, style=wx.CB_READONLY)
        self.cbTipoJuridicoParticipante.Bind(wx.EVT_COMBOBOX, self.definirCampoCic)

        self.stCicParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'CNPJ ou CPF', pos=(180, 115), style=wx.ALIGN_LEFT)
        self.tcCicParticipante = masked.TextCtrl(self.panelNovoParticipante, -1, mask="")
        self.tcCicParticipante.SetSize((140, -1))
        self.tcCicParticipante.SetPosition((180, 135))
        self.tcCicParticipante.SetEditable(False)

        self.stNomeParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'Nome', pos=(10, 165), style=wx.ALIGN_LEFT)
        self.tcNomeParticipante = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 185), size=(310, -1), style=wx.ALIGN_LEFT)
        self.tcNomeParticipante.SetMaxLength(50)

        self.stValorParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'Valor de Participação', pos=(10, 215), style=wx.ALIGN_LEFT)
        self.tcValorParticipante = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoParticipante, pos=wx.Point(10, 235), style=0, value=0)
        self.tcValorParticipante.SetFractionWidth(2)
        self.tcValorParticipante.SetGroupChar(u"#")
        self.tcValorParticipante.SetDecimalChar(u",")
        self.tcValorParticipante.SetGroupChar(u".")
        self.tcValorParticipante.SetAllowNegative(False)

        self.stPercentualParticipante = wx.StaticText(self.panelNovoParticipante, -1, u'Percentual de Participação(%)', pos=(200, 215), style=wx.ALIGN_LEFT)
        self.tcPercentualParticipante = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoParticipante, pos=wx.Point(200, 235), style=0, value=0)
        self.tcPercentualParticipante.SetFractionWidth(2)
        self.tcPercentualParticipante.SetGroupChar(u"#")
        self.tcPercentualParticipante.SetDecimalChar(u",")
        self.tcPercentualParticipante.SetGroupChar(u".")
        self.tcValorParticipante.SetAllowNegative(False)
        self.tcPercentualParticipante.Bind(wx.EVT_KILL_FOCUS, self.verificaPercentagem)

        wx.StaticBox(self.panelNovoParticipante, -1, pos=(3, 275), size=(360, 360))

        self.stCertidaoINSS = wx.StaticText(self.panelNovoParticipante, -1, u'INSS', pos=(10, 285))
        self.tcCertidaoINSS = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 305), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoINSS.SetMaxLength(60)

        self.stDataINSS = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 285))
        self.tcDataINSS = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataINSS.SetSize((80, -1))
        self.tcDataINSS.SetPosition((150, 305))

        self.stDataVencimentoINSS = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 285))
        self.tcDataVencimentoINSS = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoINSS.SetSize((80, -1))
        self.tcDataVencimentoINSS.SetPosition((260, 305))

        self.stCertidaoFGTS = wx.StaticText(self.panelNovoParticipante, -1, u'FGTS', pos=(10, 335))
        self.tcCertidaoFGTS = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 355), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoFGTS.SetMaxLength(60)

        self.stDataFGTS = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 335))
        self.tcDataFGTS = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataFGTS.SetSize((80, -1))
        self.tcDataFGTS.SetPosition((150, 355))

        self.stDataVencimentoFGTS = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 335))
        self.tcDataVencimentoFGTS = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoFGTS.SetSize((80, -1))
        self.tcDataVencimentoFGTS.SetPosition((260, 355))

        self.stCertidaoFederal = wx.StaticText(self.panelNovoParticipante, -1, u'Fazenda Federal', pos=(10, 385))
        self.tcCertidaoFederal = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 405), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoFederal.SetMaxLength(60)
        
        self.stDataFederal = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 385))
        self.tcDataFederal = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataFederal.SetSize((80, -1))
        self.tcDataFederal.SetPosition((150, 405))

        self.stDataVencimentoFederal = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 385))
        self.tcDataVencimentoFederal = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoFederal.SetSize((80, -1))
        self.tcDataVencimentoFederal.SetPosition((260, 405))

        self.stCertidaoEstadual = wx.StaticText(self.panelNovoParticipante, -1, u'Fazenda Estadual', pos=(10, 435))
        self.tcCertidaoEstadual = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 455), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoEstadual.SetMaxLength(60)
        
        self.stDataEstadual = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 435))
        self.tcDataEstadual = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataEstadual.SetSize((80, -1))
        self.tcDataEstadual.SetPosition((150, 455))

        self.stDataVencimentoEstadual = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 435))
        self.tcDataVencimentoEstadual = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoEstadual.SetSize((80, -1))
        self.tcDataVencimentoEstadual.SetPosition((260, 455))

        self.stCertidaoMunicipal = wx.StaticText(self.panelNovoParticipante, -1, u'Fazenda Municipal', pos=(10, 485))
        self.tcCertidaoMunicipal = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 505), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoMunicipal.SetMaxLength(60)
        
        self.stDataMunicipal = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 485))
        self.tcDataMunicipal = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataMunicipal.SetSize((80, -1))
        self.tcDataMunicipal.SetPosition((150, 505))

        self.stDataVencimentoMunicipal = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 485))
        self.tcDataVencimentoMunicipal = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoMunicipal.SetSize((80, -1))
        self.tcDataVencimentoMunicipal.SetPosition((260, 505))

        self.stCertidaoCNDT = wx.StaticText(self.panelNovoParticipante, -1, u'CNDT', pos=(10, 535))
        self.tcCertidaoCNDT = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 555), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoCNDT.SetMaxLength(60)
        
        self.stDataCNDT = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 535))
        self.tcDataCNDT = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataCNDT.SetSize((80, -1))
        self.tcDataCNDT.SetPosition((150, 555))

        self.stDataVencimentoCNDT = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 535))
        self.tcDataVencimentoCNDT = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoCNDT.SetSize((80, -1))
        self.tcDataVencimentoCNDT.SetPosition((260, 555))

        self.stCertidaoOutras = wx.StaticText(self.panelNovoParticipante, -1, u'Outras', pos=(10, 585))
        self.tcCertidaoOutras = wx.TextCtrl(self.panelNovoParticipante, -1, pos=(10, 605), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoOutras.SetMaxLength(60)
        
        self.stDataOutras = wx.StaticText(self.panelNovoParticipante, -1, u'Data Emissão', pos=(150, 585))
        self.tcDataOutras = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataOutras.SetSize((80, -1))
        self.tcDataOutras.SetPosition((150, 605))

        self.stDataVencimentoOutras = wx.StaticText(self.panelNovoParticipante, -1, u'Data Vencimento', pos=(260, 585))
        self.tcDataVencimentoOutras = masked.TextCtrl(self.panelNovoParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoOutras.SetSize((80, -1))
        self.tcDataVencimentoOutras.SetPosition((260, 605))

        self.btnSalvar = wx.Button(self.panelNovoParticipante, -1, "Salvar", pos=(80, 650))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarParticipante)
        self.btnCancelar = wx.Button(self.panelNovoParticipante, -1, "Cancelar", pos=(200, 650))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoParticipante)

        self.windowNovoParticipante.Bind(wx.EVT_CLOSE, self.quitNovoParticipante)

        self.windowNovoParticipante.Centre()
        self.windowNovoParticipante.Show()

    def insereInCtrList(self, event):

        self.participanteListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            participantes = ParticipanteConvenio.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for participante in participantes:

                index = self.participanteListCtrl.InsertStringItem(sys.maxint, unicode(participante.nomeParticipante))
                self.participanteListCtrl.SetStringItem(index, 1, participante.cicParticipante)
                self.participanteListCtrl.SetStringItem(index, 2, participante.numeroConvenio)
                self.participanteListCtrl.SetStringItem(index, 3, unicode(participante.id))

    def inserNumeroConvenio(self, event):

        self.cbNumeroConvenio.Clear()

        convenios = Convenio.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()
        if not convenios:
            self.message = wx.MessageDialog(None, u'Não existe Convênios para a competência selecionada!', 'Info', wx.OK)
            self.message.ShowModal()
        else:
            for convenio in convenios:

                self.cbNumeroConvenio.Append(unicode(convenio.numeroConvenio))

            self.cbNumeroConvenio.Enable()

    def definirCampoCic(self, event):

        if event.GetString() == u"Física":

            self.tcCicParticipante.SetValue('')
            self.tcCicParticipante.SetMask(("###.###.###-##"))
            self.tcCicParticipante.SetEditable(True)

        elif event.GetString() == u"Jurídica":

            self.tcCicParticipante.SetValue('')
            self.tcCicParticipante.SetMask(("##.###.###/####-##"))
            self.tcCicParticipante.SetEditable(True)
        else:

            self.tcCicParticipante.SetValue('')
            self.tcCicParticipante.SetMask(("###############"))
            self.tcCicParticipante.SetMask(("##############"))
            self.tcCicParticipante.SetEditable(True)

    def verificaPercentagem(self, event):

        if self.tcPercentualParticipante.GetValue() > 100:
            self.message = wx.MessageDialog(None, u'O campo Percentual de Participação(%) deve ter valor entre 0 e 100', 'Info', wx.OK)
            self.message.ShowModal()
            self.tcPercentualParticipante.SetValue(0)
            self.tcPercentualParticipante.SetFocus()

    def quitNovoParticipante(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoParticipante.Destroy()

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

        if self.cbNumeroConvenio.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Número do Convênio', 'Info', wx.OK)
            self.cbNumeroConvenio.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoJuridicoParticipante.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Pessoa', 'Info', wx.OK)
            self.cbTipoJuridicoParticipante.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoJuridicoParticipante.GetSelection() == 0:
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

        if self.cbTipoJuridicoParticipante.GetSelection() == 1:
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

        if self.cbTipoJuridicoParticipante.GetSelection() == 2:
            if self.tcCicParticipante.GetValue() == '              ':
                self.message = wx.MessageDialog(None, u'Digite o identificador no campo CNPJ ou CPF', 'Info', wx.OK)
                self.tcCicParticipante.SelectAll()
                self.tcCicParticipante.SetFocus()
                self.message.ShowModal()
                return 0

        if self.tcNomeParticipante.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Nome deve ser preenchido', 'Info', wx.OK)
            self.tcNomeParticipante.SelectAll()
            self.tcNomeParticipante.SetFocus()
            self.message.ShowModal()
            return 0

        participante = ParticipanteConvenio.query.filter_by(cicParticipante=self.tcCicParticipante.GetValue()).first()

        if participante != None:

            if (unicode(participante.cicParticipante.upper()) == unicode(self.tcCicParticipante.GetValue().upper())) and (participante.id == int(self.tcId.GetValue())) and (participante.numeroConvenio == self.cbNumeroConvenio.GetValue()):
                pass

            elif (unicode(participante.cicParticipante.upper()) == unicode(self.tcCicParticipante.GetValue().upper())) and (participante.id != int(self.tcId.GetValue())) and (participante.numeroConvenio == self.cbNumeroConvenio.GetValue()):
                self.message = wx.MessageDialog(None, u'Já existe um Participante com este CPF/CNPJ cadastrado para este Número de Convênio!', 'Info', wx.OK)
                self.cbNumeroConvenio.SetFocus()
                self.message.ShowModal()
                return 0

        if self.tcCertidaoINSS.GetValue() != "":
            if not self.validateDate(self.tcDataINSS.GetValue(), u"Data Emissão (INSS)"):
                self.tcDataINSS.SelectAll()
                self.tcDataINSS.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoINSS.GetValue(), u"Data de Vencimento (INSS)"):
                self.tcDataVencimentoINSS.SelectAll()
                self.tcDataVencimentoINSS.SetFocus()
                return 0

        if self.tcCertidaoFGTS.GetValue() != "":
            if not self.validateDate(self.tcDataFGTS.GetValue(), u"Data Emissão (FGTS)"):
                self.tcDataFGTS.SelectAll()
                self.tcDataFGTS.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoFGTS.GetValue(), u"Data de Vencimento (FGTS)"):
                self.tcDataVencimentoFGTS.SelectAll()
                self.tcDataVencimentoFGTS.SetFocus()
                return 0

        if self.tcCertidaoEstadual.GetValue() != "":
            if not self.validateDate(self.tcDataEstadual.GetValue(), u"Data Emissão (Fazenda Estadual)"):
                self.tcDataEstadual.SelectAll()
                self.tcDataEstadual.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoEstadual.GetValue(), u"Data de Vencimento (Fazenda Estadual)"):
                self.tcDataVencimentoEstadual.SelectAll()
                self.tcDataVencimentoEstadual.SetFocus()
                return 0

        if self.tcCertidaoFederal.GetValue() != "":
            if not self.validateDate(self.tcDataFederal.GetValue(), u"Data Emissão (Fazenda Federal)"):
                self.tcDataFederal.SelectAll()
                self.tcDataFederal.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoFederal.GetValue(), u"Data de Vencimento (Fazenda Federal)"):
                self.tcDataVencimentoFederal.SelectAll()
                self.tcDataVencimentoFederal.SetFocus()
                return 0

        if self.tcCertidaoMunicipal.GetValue() != "":

            if not self.validateDate(self.tcDataMunicipal.GetValue(), u"Data Emissão (Fazenda Municipal)"):
                self.tcDataMunicipal.SelectAll()
                self.tcDataMunicipal.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoMunicipal.GetValue(), u"Data de Vencimento (Fazenda Municipal)"):
                self.tcDataVencimentoMunicipal.SelectAll()
                self.tcDataVencimentoMunicipal.SetFocus()
                return 0

        if self.tcCertidaoCNDT.GetValue() != "":

            if not self.validateDate(self.tcDataCNDT.GetValue(), u"Data Emissão (CNDT)"):
                self.tcDataCNDT.SelectAll()
                self.tcDataCNDT.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoCNDT.GetValue(), u"Data de Vencimento (CNDT)"):
                self.tcDataVencimentoCNDT.SelectAll()
                self.tcDataVencimentoCNDT.SetFocus()
                return 0

        if self.tcCertidaoOutras.GetValue() != "":

            if not self.validateDate(self.tcDataOutras.GetValue(), u"Data Emissão (Outras)"):
                self.tcDataOutras.SelectAll()
                self.tcDataOutras.SetFocus()
                return 0

            if not self.validateDate(self.tcDataVencimentoOutras.GetValue(), u"Data de Vencimento (Outras)"):
                self.tcDataVencimentoOutras.SelectAll()
                self.tcDataVencimentoOutras.SetFocus()
                return 0

        return 1

    def salvarParticipante(self, event):

        if self.valida():
            ParticipanteConvenio(cicParticipante=unicode(self.tcCicParticipante.GetValue()),
                pessoaParticipante=unicode(self.cbTipoJuridicoParticipante.GetValue()),
                nomeParticipante=unicode(self.tcNomeParticipante.GetValue()),
                valorParticipacao=unicode(self.tcValorParticipante.GetValue()),
                percentualParticipacao=unicode(self.tcPercentualParticipante.GetValue()),
                certidaoINSS=unicode(self.tcCertidaoINSS.GetValue()),
                dataINSS=unicode(self.tcDataINSS.GetValue()),
                dataValidadeINSS=unicode(self.tcDataVencimentoINSS.GetValue()),
                certidaoFGTS=unicode(self.tcCertidaoFGTS.GetValue()),
                dataFGTS=unicode(self.tcDataFGTS.GetValue()),
                dataValidadeFGTS=unicode(self.tcDataVencimentoFGTS.GetValue()),
                certidaoFazendaEstadual=unicode(self.tcCertidaoEstadual.GetValue()),
                dataFazendaEstadual=unicode(self.tcDataEstadual.GetValue()),
                dataValidadeFazendaEstadual=unicode(self.tcDataVencimentoEstadual.GetValue()),
                certidaoFazendaMunicipal=unicode(self.tcCertidaoMunicipal.GetValue()),
                dataFazendaMunicipal=unicode(self.tcDataMunicipal.GetValue()),
                dataValidadeFazendaMunicipal=unicode(self.tcDataVencimentoMunicipal.GetValue()),
                certidaoFazendaFederal=unicode(self.tcCertidaoFederal.GetValue()),
                dataFazendaFederal=unicode(self.tcDataFederal.GetValue()),
                dataValidadeFazendaFederal=unicode(self.tcDataVencimentoFederal.GetValue()),
                certidaoCNDT=unicode(self.tcCertidaoCNDT.GetValue()),
                dataCNDT=unicode(self.tcDataCNDT.GetValue()),
                dataValidadeCNDT=unicode(self.tcDataVencimentoCNDT.GetValue()),
                certidaoOutras=unicode(self.tcCertidaoOutras.GetValue()),
                dataOutras=unicode(self.tcDataOutras.GetValue()),
                dataValidadeOutras=unicode(self.tcDataVencimentoOutras.GetValue()),
                numeroConvenio=unicode(self.cbNumeroConvenio.GetValue()),
                esferaConvenio=unicode(self.cbEsferaConveniado.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue())
            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Participante de convênio salvo com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.windowNovoParticipante.Close()

    def vizualizaParticipante(self, event, idParticipante=None):

        if idParticipante is None:
            self.message = wx.MessageDialog(None, u'Nenhum Participante de convênio foi selecionado! Selecione um na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.participante = ParticipanteConvenio.query.filter_by(id=idParticipante).first()

        self.toolBarControler(False, False, False, False)

        self.windowEditaParticipante = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(380, 710), pos=(300, 170), title=u"Participante de Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaParticipante = wx.Panel(self.windowEditaParticipante, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.participante.id))

        self.stCompetencia = wx.StaticText(self.panelEditaParticipante, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaParticipante, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.inserNumeroConvenio)
        self.cbCompetencia.SetValue(self.participante.competencia)

        wx.StaticBox(self.panelEditaParticipante, -1, pos=(3, 50), size=(360, 220))

        self.stNumeroConvenio = wx.StaticText(self.panelEditaParticipante, -1, u'Número do Convênio', pos=(10, 65))
        self.cbNumeroConvenio = wx.ComboBox(self.panelEditaParticipante, -1, pos=(10, 85), size=(120, -1), choices=[], style=wx.CB_READONLY)
        self.inserNumeroConvenio(None)
        self.cbNumeroConvenio.SetValue(self.participante.numeroConvenio)

        self.stEsferaConveniado = wx.StaticText(self.panelEditaParticipante, -1, u'Esfera do Conveniado', pos=(180, 65))
        self.cbEsferaConveniado = wx.ComboBox(self.panelEditaParticipante, -1,  pos=(180, 85), size=(120, -1), choices=self.choicesEsferaConvenio, style=wx.CB_READONLY)
        self.participante.esferaConvenio
        self.cbEsferaConveniado.SetValue(self.participante.esferaConvenio)

        self.stTipoJuridicoParticipante = wx.StaticText(self.panelEditaParticipante, -1, u'Tipo Pessoa', pos=(10, 115), style=wx.ALIGN_LEFT)
        self.cbTipoJuridicoParticipante = wx.ComboBox(self.panelEditaParticipante, -1, pos=(10, 135), size=(150, -1), choices=self.choicesTipoJuridico, style=wx.CB_READONLY)
        self.cbTipoJuridicoParticipante.Bind(wx.EVT_COMBOBOX, self.definirCampoCic)
        self.cbTipoJuridicoParticipante.SetValue(self.participante.pessoaParticipante)

        self.stCicParticipante = wx.StaticText(self.panelEditaParticipante, -1, u'CNPJ ou CPF', pos=(180, 115), style=wx.ALIGN_LEFT)
        self.tcCicParticipante = masked.TextCtrl(self.panelEditaParticipante, -1, mask="")
        self.tcCicParticipante.SetSize((140, -1))
        self.tcCicParticipante.SetPosition((180, 135))
        self.tcCicParticipante.SetValue(self.participante.cicParticipante)

        self.stNomeParticipante = wx.StaticText(self.panelEditaParticipante, -1, u'Nome', pos=(10, 165), style=wx.ALIGN_LEFT)
        self.tcNomeParticipante = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 185), size=(310, -1), style=wx.ALIGN_LEFT)
        self.tcNomeParticipante.SetMaxLength(50)
        self.tcNomeParticipante.SetValue(self.participante.nomeParticipante)

        self.stValorParticipante = wx.StaticText(self.panelEditaParticipante, -1, u'Valor de Participação', pos=(10, 215), style=wx.ALIGN_LEFT)
        self.tcValorParticipante = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaParticipante, pos=wx.Point(10, 235), style=0, value=0)
        self.tcValorParticipante.SetFractionWidth(2)
        self.tcValorParticipante.SetGroupChar(u"#")
        self.tcValorParticipante.SetDecimalChar(u",")
        self.tcValorParticipante.SetGroupChar(u".")
        self.tcValorParticipante.SetAllowNegative(False)
        self.tcValorParticipante.SetValue(float(self.participante.valorParticipacao))

        self.stPercentualParticipante = wx.StaticText(self.panelEditaParticipante, -1, u'Percentual de Participação(%)', pos=(200, 215), style=wx.ALIGN_LEFT)
        self.tcPercentualParticipante = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelEditaParticipante, pos=wx.Point(200, 235), style=0, value=0)
        self.tcPercentualParticipante.SetFractionWidth(2)
        self.tcPercentualParticipante.SetGroupChar(u"#")
        self.tcPercentualParticipante.SetDecimalChar(u",")
        self.tcPercentualParticipante.SetGroupChar(u".")
        self.tcValorParticipante.SetAllowNegative(False)
        self.tcPercentualParticipante.Bind(wx.EVT_KILL_FOCUS, self.verificaPercentagem)
        self.tcPercentualParticipante.SetValue(self.participante.percentualParticipacao)

        wx.StaticBox(self.panelEditaParticipante, -1, pos=(3, 275), size=(360, 360))

        self.stCertidaoINSS = wx.StaticText(self.panelEditaParticipante, -1, u'INSS', pos=(10, 285))
        self.tcCertidaoINSS = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 305), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoINSS.SetMaxLength(60)
        self.tcCertidaoINSS.SetValue(self.participante.certidaoINSS)

        self.stDataINSS = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 285))
        self.tcDataINSS = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataINSS.SetSize((80, -1))
        self.tcDataINSS.SetPosition((150, 305))
        self.tcDataINSS.SetValue(self.participante.dataINSS)

        self.stDataVencimentoINSS = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 285))
        self.tcDataVencimentoINSS = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoINSS.SetSize((80, -1))
        self.tcDataVencimentoINSS.SetPosition((260, 305))
        self.tcDataVencimentoINSS.SetValue(self.participante.dataValidadeINSS)

        self.stCertidaoFGTS = wx.StaticText(self.panelEditaParticipante, -1, u'FGTS', pos=(10, 335))
        self.tcCertidaoFGTS = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 355), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoFGTS.SetMaxLength(60)
        self.tcCertidaoFGTS.SetValue(self.participante.certidaoFGTS)

        self.stDataFGTS = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 335))
        self.tcDataFGTS = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataFGTS.SetSize((80, -1))
        self.tcDataFGTS.SetPosition((150, 355))
        self.tcDataFGTS.SetValue(self.participante.dataFGTS)

        self.stDataVencimentoFGTS = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 335))
        self.tcDataVencimentoFGTS = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoFGTS.SetSize((80, -1))
        self.tcDataVencimentoFGTS.SetPosition((260, 355))
        self.tcDataVencimentoFGTS.SetValue(self.participante.dataValidadeFGTS)

        self.stCertidaoFederal = wx.StaticText(self.panelEditaParticipante, -1, u'Fazenda Federal', pos=(10, 385))
        self.tcCertidaoFederal = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 405), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoFederal.SetMaxLength(60)
        self.tcCertidaoFederal.SetValue(self.participante.certidaoFazendaFederal)

        self.stDataFederal = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 385))
        self.tcDataFederal = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataFederal.SetSize((80, -1))
        self.tcDataFederal.SetPosition((150, 405))
        self.tcDataFederal.SetValue(self.participante.dataValidadeFazendaFederal)

        self.stDataVencimentoFederal = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 385))
        self.tcDataVencimentoFederal = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoFederal.SetSize((80, -1))
        self.tcDataVencimentoFederal.SetPosition((260, 405))
        self.tcDataVencimentoFederal.SetValue(self.participante.dataValidadeFazendaFederal)

        self.stCertidaoEstadual = wx.StaticText(self.panelEditaParticipante, -1, u'Fazenda Estadual', pos=(10, 435))
        self.tcCertidaoEstadual = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 455), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoEstadual.SetMaxLength(60)
        self.tcCertidaoEstadual.SetValue(self.participante.certidaoFazendaEstadual)

        self.stDataEstadual = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 435))
        self.tcDataEstadual = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataEstadual.SetSize((80, -1))
        self.tcDataEstadual.SetPosition((150, 455))
        self.tcDataEstadual.SetValue(self.participante.dataFazendaEstadual)

        self.stDataVencimentoEstadual = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 435))
        self.tcDataVencimentoEstadual = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoEstadual.SetSize((80, -1))
        self.tcDataVencimentoEstadual.SetPosition((260, 455))
        self.tcDataVencimentoEstadual.SetValue(self.participante.dataValidadeFazendaEstadual)

        self.stCertidaoMunicipal = wx.StaticText(self.panelEditaParticipante, -1, u'Fazenda Municipal', pos=(10, 485))
        self.tcCertidaoMunicipal = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 505), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoMunicipal.SetMaxLength(60)
        self.tcCertidaoMunicipal.SetValue(self.participante.certidaoFazendaMunicipal)

        self.stDataMunicipal = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 485))
        self.tcDataMunicipal = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataMunicipal.SetSize((80, -1))
        self.tcDataMunicipal.SetPosition((150, 505))
        self.tcDataMunicipal.SetValue(self.participante.dataFazendaMunicipal)

        self.stDataVencimentoMunicipal = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 485))
        self.tcDataVencimentoMunicipal = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoMunicipal.SetSize((80, -1))
        self.tcDataVencimentoMunicipal.SetPosition((260, 505))
        self.tcDataVencimentoMunicipal.SetValue(self.participante.dataValidadeFazendaMunicipal)

        self.stCertidaoCNDT = wx.StaticText(self.panelEditaParticipante, -1, u'CNDT', pos=(10, 535))
        self.tcCertidaoCNDT = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 555), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoCNDT.SetMaxLength(60)
        self.tcCertidaoCNDT.SetValue(self.participante.certidaoCNDT)
        
        self.stDataCNDT = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 535))
        self.tcDataCNDT = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataCNDT.SetSize((80, -1))
        self.tcDataCNDT.SetPosition((150, 555))
        self.tcDataCNDT.SetValue(self.participante.dataCNDT)

        self.stDataVencimentoCNDT = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 535))
        self.tcDataVencimentoCNDT = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoCNDT.SetSize((80, -1))
        self.tcDataVencimentoCNDT.SetPosition((260, 555))
        self.tcDataVencimentoCNDT.SetValue(self.participante.dataValidadeCNDT)

        self.stCertidaoOutras = wx.StaticText(self.panelEditaParticipante, -1, u'Outras', pos=(10, 585))
        self.tcCertidaoOutras = wx.TextCtrl(self.panelEditaParticipante, -1, pos=(10, 605), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCertidaoOutras.SetMaxLength(60)
        self.tcCertidaoOutras.SetValue(self.participante.certidaoOutras)
        
        self.stDataOutras = wx.StaticText(self.panelEditaParticipante, -1, u'Data Emissão', pos=(150, 585))
        self.tcDataOutras = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataOutras.SetSize((80, -1))
        self.tcDataOutras.SetPosition((150, 605))
        self.tcDataOutras.SetValue(self.participante.dataOutras)

        self.stDataVencimentoOutras = wx.StaticText(self.panelEditaParticipante, -1, u'Data Vencimento', pos=(260, 585))
        self.tcDataVencimentoOutras = masked.TextCtrl(self.panelEditaParticipante, -1, mask="##/##/####")
        self.tcDataVencimentoOutras.SetSize((80, -1))
        self.tcDataVencimentoOutras.SetPosition((260, 605))
        self.tcDataVencimentoOutras.SetValue(self.participante.dataValidadeOutras)

        self.btnSalvar = wx.Button(self.panelEditaParticipante, -1, "Alterar", pos=(80, 650))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarParticipante)
        self.btnCancelar = wx.Button(self.panelEditaParticipante, -1, "Cancelar", pos=(200, 650))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEditaParticipante)
        self.windowEditaParticipante.Bind(wx.EVT_CLOSE, self.quitEditaParticipante)

        self.windowEditaParticipante.Centre()
        self.windowEditaParticipante.Show()

    def quitEditaParticipante(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaParticipante.Destroy()

    def editarParticipante(self, event):

        if self.valida():

            self.participante.cicParticipante = unicode(self.tcCicParticipante.GetValue())
            self.participante.pessoaParticipante = unicode(self.cbTipoJuridicoParticipante.GetValue())
            self.participante.nomeParticipante = unicode(self.tcNomeParticipante.GetValue())
            self.participante.valorParticipacao = unicode(self.tcValorParticipante.GetValue())
            self.participante.percentualParticipacao = unicode(self.tcValorParticipante.GetValue())
            self.participante.certidaoINSS = unicode(self.tcCertidaoINSS.GetValue())
            self.participante.dataINSS = unicode(self.tcDataINSS.GetValue())
            self.participante.dataValidadeINSS = unicode(self.tcDataVencimentoINSS.GetValue())
            self.participante.certidaoFGTS = unicode(self.tcCertidaoFGTS.GetValue())
            self.participante.dataFGTS = unicode(self.tcDataFGTS.GetValue())
            self.participante.dataValidadeFGTS = unicode(self.tcDataVencimentoFGTS.GetValue())
            self.participante.certidaoFazendaEstadual = unicode(self.tcCertidaoEstadual.GetValue())
            self.participante.dataFazendaEstadual = unicode(self.tcDataEstadual.GetValue())
            self.participante.dataValidadeFazendaEstadual = unicode(self.tcDataVencimentoEstadual.GetValue())
            self.participante.certidaoFazendaMunicipal = unicode(self.tcCertidaoMunicipal.GetValue())
            self.participante.dataFazendaMunicipal = unicode(self.tcDataMunicipal.GetValue())
            self.participante.dataValidadeFazendaMunicipal = unicode(self.tcDataVencimentoMunicipal.GetValue())
            self.participante.certidaoFazendaFederal = unicode(self.tcCertidaoFederal.GetValue())
            self.participante.dataFazendaFederal = unicode(self.tcDataFederal.GetValue())
            self.participante.dataValidadeFazendaFederal = unicode(self.tcDataVencimentoFederal.GetValue())
            self.participante.certidaoCNDT = unicode(self.tcCertidaoCNDT.GetValue())
            self.participante.dataCNDT = unicode(self.tcDataCNDT.GetValue())
            self.participante.dataValidadeCNDT = unicode(self.tcDataVencimentoCNDT.GetValue())
            self.participante.certidaoOutras = unicode(self.tcCertidaoOutras.GetValue())
            self.participante.dataOutras = unicode(self.tcDataOutras.GetValue())
            self.participante.dataValidadeOutras = unicode(self.tcDataVencimentoOutras.GetValue())
            self.participante.numeroConvenio = unicode(self.cbNumeroConvenio.GetValue())
            self.participante.esferaConvenio = unicode(self.cbEsferaConveniado.GetValue())
            self.participante.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'Participante de convênio foi alterado com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.participante = None
            self.windowEditaParticipante.Close()

    def excluiParticipante(self, none, idContrato):

        if idContrato is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este Participante?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.participante = ParticipanteConvenio.query.filter_by(id=idContrato).first()
            self.participante.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Participante do convênio excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
        else:
            pass

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Participante de Convênio", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereParticipantesPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.participantesGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.participantesGeraArquivoListCtrl.InsertColumn(0, u'Nome do Participante', width=130)
        self.participantesGeraArquivoListCtrl.InsertColumn(1, u'Número do Convênio', width=120)
        self.participantesGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.participantesGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParticipantesGeraArquivos)

        self.btnIncluiGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.participantesParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.participantesParaArquivoListCtrl.InsertColumn(0, u'Nome do Participante', width=130)
        self.participantesParaArquivoListCtrl.InsertColumn(1, u'Número do Convênio', width=120)
        self.participantesParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.participantesParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParticipantesParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)

        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereParticipantesPorCompetencia(self, event):

        participantes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            participantes = ParticipanteConvenio.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            participantes = ParticipanteConvenio.query.all()

        self.participantesGeraArquivoListCtrl.DeleteAllItems()

        if not participantes:
            self.message = wx.MessageDialog(None, u'Não existe Participantes de Convênio para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(participantes) == self.participantesParaArquivoListCtrl.GetItemCount():
                pass
            else:

                for participante in participantes:
                    igual = False

                    if self.participantesParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.participantesGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(participante.nomeParticipante))
                        self.participantesGeraArquivoListCtrl.SetStringItem(index, 1, unicode(participante.numeroConvenio))
                        self.participantesGeraArquivoListCtrl.SetStringItem(index, 2, unicode(participante.id))

                        igual = True
                    else:

                        for x in range(self.participantesParaArquivoListCtrl.GetItemCount()):

                            if participante.nomeParticipante == unicode(self.participantesParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.participantesGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(participante.nomeParticipante))
                        self.participantesGeraArquivoListCtrl.SetStringItem(index, 1, unicode(participante.numeroConvenio))
                        self.participantesGeraArquivoListCtrl.SetStringItem(index, 2, unicode(participante.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensParticipantesGeraArquivos(self, event):

        item = self.participantesGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.participantesGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensParticipantesParaArquivo(self, event):

        item = self.participantesParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.participantesParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione os Participantes a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.participantesParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.participantesGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.participantesParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.participantesGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.participantesParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.participantesGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.participantesGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione os convênios a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.participantesGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.participantesParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.participantesGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.participantesParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.participantesGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.participantesParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.participantesParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.participantesParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Participantes do Convênio para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u'Salvar ', defaultDir="", defaultFile='PARTICIPANTECONVENIO.REM', wildcard='Arquivo de Remessa (*.REM)|*.REM', style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Participantes de Convênios gerados com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Participantes de Convênios gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        dlg.Destroy()
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.participantesParaArquivoListCtrl.GetItemCount()):

            try:

                idParticipante = int(self.participantesParaArquivoListCtrl.GetItem(x, 2).GetText())
                participante = ParticipanteConvenio.query.filter_by(id=idParticipante).first()

                f.write(unicode(self.retiraCaracteresCpfCnpj(participante.cicParticipante).zfill(14)))
                f.write(unicode(self.transformaTipoJuridico(participante.pessoaParticipante)))
                f.write(unicode(participante.nomeParticipante.ljust(50).replace("'", "").replace("\"", "")))
                
                partes = participante.valorParticipacao.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((participante.valorParticipacao).zfill(16).replace(".", ",")))
                
                else:
                    f.write(unicode((participante.valorParticipacao+'0').zfill(16).replace(".", ",")))
                
                
                partes = participante.percentualParticipacao.split('.')
                if len(partes[1])> 1:
                    f.write(unicode((participante.percentualParticipacao).zfill(7).replace(".", ",")))
                
                else:
                    f.write(unicode((participante.percentualParticipacao+'0').zfill(7).replace(".", ",")))
                                                
                               
                f.write(unicode(participante.certidaoINSS.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataINSS)))
                f.write(unicode(self.transformaData(participante.dataValidadeINSS)))

                f.write(unicode(participante.certidaoFGTS.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataValidadeFGTS)))
                f.write(unicode(self.transformaData(participante.dataValidadeFGTS)))

                f.write(unicode(participante.certidaoFazendaEstadual.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataFazendaEstadual)))
                f.write(unicode(self.transformaData(participante.dataValidadeFazendaEstadual)))

                f.write(unicode(participante.certidaoFazendaMunicipal.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataFazendaMunicipal)))
                f.write(unicode(self.transformaData(participante.dataValidadeFazendaMunicipal)))

                f.write(unicode(participante.certidaoFazendaFederal.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataFazendaFederal)))
                f.write(unicode(self.transformaData(participante.dataValidadeFazendaFederal)))

                f.write(unicode(participante.certidaoCNDT.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataValidadeCNDT)))
                f.write(unicode(self.transformaData(participante.dataValidadeCNDT)))

                f.write(unicode(participante.certidaoOutras.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(participante.dataValidadeOutras)))
                f.write(unicode(self.transformaData(participante.dataValidadeOutras)))

                f.write(unicode(participante.numeroConvenio.ljust(16).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaEsferaConvenio(participante.esferaConvenio).zfill(1)))
                f.write(u"\n")

            except:
                return 0

        f.close()
        return 1

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

    def transformaTipoJuridico(self, tipo):
        if tipo == u'Física':
            return '1'
        elif tipo == u'Jurídica':
            return '2'
        else:
            return '3'

    def transformaEsferaConvenio(self, esferaConvenio):
        
        if esferaConvenio == u'Federal':
            return "1"
        elif esferaConvenio == u'Estadual':
            return "2"
        elif esferaConvenio == u'Municipal':
            return "3"
        elif esferaConvenio == 'ONGs':
            return "4"
        else:
            return "5"