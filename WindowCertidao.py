# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_CERTIDAO_NOVO = 5001
ID_TOOLBAR_CERTIDAO_EDITAR = 5002
ID_TOOLBAR_CERTIDAO_EXCLUIR = 5003
ID_TOOLBAR_CERTIDAO_CRIAR_ARQUIVO = 5004


class WindowCertidao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Certidão", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelCertidao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_CERTIDAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova Certidão')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CERTIDAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Certidão selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CERTIDAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Certidão selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CERTIDAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de Certidão')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelCertidao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.certidaoListCtrl = wx.ListCtrl(self.panelCertidao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.certidaoListCtrl.InsertColumn(0, u'Proc. Licitatório', width=100)
        self.certidaoListCtrl.InsertColumn(1, u'Num. Certidão', width=200)
        self.certidaoListCtrl.InsertColumn(2, u'Participante', width=220)
        self.certidaoListCtrl.InsertColumn(3, u'', width=0)
        self.certidaoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.certidaoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.certidaoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoCertidao, id=ID_TOOLBAR_CERTIDAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaCertidao(event, self.idSelecionado), id=ID_TOOLBAR_CERTIDAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiCertidao(event, self.idSelecionado), id=ID_TOOLBAR_CERTIDAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_CERTIDAO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_CERTIDAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_CERTIDAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_CERTIDAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_CERTIDAO_CRIAR_ARQUIVO, gerar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.certidaoListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def novoCertidao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoCertidao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(440, 380), pos=(300, 170), title=u'Novo - Certidão', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoCertidao = wx.Panel(self.windowNovoCertidao, wx.ID_ANY)

        self.tipoCertidao = [u'INSS', u'Federal', u'Estadual', u'Municipal', u'FGTS', u'CAM', u'CNDT', u'Outras certidões']

        self.tcId = wx.TextCtrl(self.panelNovoCertidao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoCertidao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoCertidao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)

        wx.StaticBox(self.panelNovoCertidao, -1, pos=(5, 50), size=(420, 80))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoCertidao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoCertidao, -1, pos=(10, 90), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroProcesso.Disable()
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.insereParticipante)

        self.stCicParticipante = wx.StaticText(self.panelNovoCertidao, -1, u'CPF/CNPJ Participante', pos=(170, 70))
        self.cbCicParticipante = wx.ComboBox(self.panelNovoCertidao, -1, pos=(170, 90), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbCicParticipante.Disable()
        self.cbCicParticipante.Bind(wx.EVT_COMBOBOX, self.insereTipoPessoa)

        self.stTipoPessoa = wx.StaticText(self.panelNovoCertidao, -1, u'Tipo Pessoa', pos=(320, 70))
        self.tcTipoPessoa = wx.TextCtrl(self.panelNovoCertidao, -1, pos=(320, 90), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcTipoPessoa.SetEditable(False)

        wx.StaticBox(self.panelNovoCertidao, -1, pos=(5, 130), size=(420, 140))

        self.stTipoCertidao = wx.StaticText(self.panelNovoCertidao, -1, u'Tipo Certidão', pos=(10, 150))
        self.cbTipoCertidao = wx.ComboBox(self.panelNovoCertidao, -1, pos=(10, 170), size=(100, -1), choices=self.tipoCertidao, style=wx.CB_READONLY)
        
        
        self.stNumeroCertidao = wx.StaticText(self.panelNovoCertidao, -1, u'Número Certidão', pos=(170, 150))
        self.tcNumeroCertidao = wx.TextCtrl(self.panelNovoCertidao, -1, pos=(170, 170), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroCertidao.SetMaxLength(60)

        self.stDataEmissao = wx.StaticText(self.panelNovoCertidao, -1, u'Data de Emissão', pos=(10, 210), style=wx.ALIGN_LEFT)
        self.tcdataEmissao = masked.TextCtrl(self.panelNovoCertidao, -1, mask="##/##/####")
        self.tcdataEmissao.SetSize((80, -1))
        self.tcdataEmissao.SetPosition((10, 230))

        self.stDataValidade = wx.StaticText(self.panelNovoCertidao, -1, u'Data de Validade', pos=(170, 210), style=wx.ALIGN_LEFT)
        self.tcDataValidade = masked.TextCtrl(self.panelNovoCertidao, -1, mask="##/##/####")
        self.tcDataValidade.SetSize((80, -1))
        self.tcDataValidade.SetPosition((170, 230))

        self.btnSalvar = wx.Button(self.panelNovoCertidao, -1, u"Salvar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarCertidao)
        self.btnCancelar = wx.Button(self.panelNovoCertidao, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoCertidao)      

        #Bind
        self.windowNovoCertidao.Bind(wx.EVT_CLOSE, self.quitNovoCertidao)



        self.windowNovoCertidao.Centre()
        self.windowNovoCertidao.Show()

    def quitNovoCertidao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoCertidao.Destroy()

    def insereTipoPessoa(self, event):

        participante = ParticipanteLicitacao.query.filter_by(cicParticipante=self.cbCicParticipante.GetValue()).first()

        if not participante:
            pass
        else:
            self.tcTipoPessoa.SetValue(participante.tipoJuridicoParticipante)

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

    def insereParticipante(self, event):

        licitacao = Licitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).first()
        
        if licitacao.modalidadeLicitacao == u'Deserta' or licitacao.modalidadeLicitacao == u'Fracassada':
            
            self.cbCicParticipante.SetSelection(-1)
            self.cbCicParticipante.Disable()
            self.tcTipoPessoa.SetValue("")
            self.tcTipoPessoa.Disable()
            self.cbTipoCertidao.SetSelection(-1)
            self.cbTipoCertidao.Disable()
            self.tcNumeroCertidao.SetValue("")
            self.tcNumeroCertidao.Disable()
            self.tcdataEmissao.SetValue("")
            self.tcdataEmissao.Disable()
            self.tcDataValidade.SetValue("")
            self.tcDataValidade.Disable()
            self.btnSalvar.Disable()

            self.message = wx.MessageDialog(None, u'Esta licitação não necessita de Certidão.\n Esta licitação pertence a modalidade de licitação: Deserta ou Fracassada.', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            self.cbCicParticipante.Enable()
            self.tcTipoPessoa.Enable()
            self.cbTipoCertidao.Enable()
            self.tcNumeroCertidao.Enable()
            self.tcdataEmissao.Enable()
            self.tcDataValidade.Enable()
            self.btnSalvar.Enable()

            self.cbCicParticipante.Clear()

            participantes = ParticipanteLicitacao.query.filter_by(numeroProcessoLicitatorio=self.cbNumeroProcesso.GetValue()).all()

            if not participantes:
                self.message = wx.MessageDialog(None, u'Não existe Participantes de Licitação para a licitação selecionada!', 'Info', wx.OK)
                self.message.ShowModal()
                self.cbCicParticipante.Disable()
                self.tcTipoPessoa.SetValue("")
            else:
                for participante in participantes:
                    self.cbCicParticipante.Append(unicode(participante.cicParticipante))

                self.cbCicParticipante.Enable()

    def insereInCtrList(self, event):

        self.certidaoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            certidoes = Certidao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for certidao in certidoes:

                index = self.certidaoListCtrl.InsertStringItem(sys.maxint, unicode(certidao.numeroProcesso))
                self.certidaoListCtrl.SetStringItem(index, 1, certidao.numeroCertidao)
                self.certidaoListCtrl.SetStringItem(index, 2, certidao.cicParticipante)
                self.certidaoListCtrl.SetStringItem(index, 3, unicode(certidao.id))


       
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

        # Não faz validação se certidão já foi cadastrada. Não sei direito as regras de como um cedrtidão pode ser considerada igual.

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

        if self.cbCicParticipante.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo CPF/CNPJ Participante', 'Info', wx.OK)
            self.cbCicParticipante.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoCertidao.GetSelection() == -1:

            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Certidão', 'Info', wx.OK)
            self.cbTipoCertidao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroCertidao.GetValue() == "":

            self.message = wx.MessageDialog(None, u'O campo Número certidão deve ser preenchido', 'Info', wx.OK)
            self.tcNumeroCertidao.SetFocus()
            self.message.ShowModal()
            return 0

        if not self.validateDate(self.tcdataEmissao.GetValue(), u"Data de Emissão"):
            self.tcdataEmissao.SelectAll()
            self.tcdataEmissao.SetFocus()
            return 0

        if not self.validateDate(self.tcDataValidade.GetValue(), u"Data de Validade"):
            self.tcDataValidade.SelectAll()
            self.tcDataValidade.SetFocus()
            return 0

        certidoes = Certidao.query.filter_by(numeroCertidao=self.tcNumeroCertidao.GetValue()).all()

        if certidoes:
            for certidao in certidoes:
                if unicode(certidao.numeroCertidao) == self.tcNumeroCertidao.GetValue() and certidao.id != int(self.tcId.GetValue()) and certidao.tipoCertidao == self.cbTipoCertidao.GetValue():
                    self.message = wx.MessageDialog(None, u'Certidão já cadastrada!', 'Info', wx.OK)
                    self.tcNumeroCertidao.SetFocus()
                    self.message.ShowModal()
                    return 0    
        return 1

    def salvarCertidao(self, event):
        
        if self.valida():
            
            Certidao(
                numeroProcesso=unicode(self.cbNumeroProcesso.GetValue()), 
                cicParticipante=unicode(self.cbCicParticipante.GetValue()), 
                tipoCertidao=unicode(self.cbTipoCertidao.GetValue()), 
                tipoJuridico=unicode(self.tcTipoPessoa.GetValue()), 
                numeroCertidao=unicode(self.tcNumeroCertidao.GetValue()),
                dataEmissao=unicode(self.tcdataEmissao.GetValue()),
                dataValidade=unicode(self.tcDataValidade.GetValue()),
                competencia=unicode(self.cbCompetencia.GetValue())

            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Certidão salva com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitNovoCertidao(None)

    def vizualizaCertidao(self, event, idCertidao):

        if idCertidao is None:

            self.message = wx.MessageDialog(None, u'Nenhuma Certidão foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.certidao = Certidao.query.filter_by(id=idCertidao).first()

        self.toolBarControler(False, False, False, False)

        self.windowVizualizaCertidao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(440, 380), pos=(300, 170), title=u'Novo - Certidão', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelvizualizaCertidao = wx.Panel(self.windowVizualizaCertidao, wx.ID_ANY)

        self.tipoCertidao = [u'INSS', u'Federal', u'Estadual', u'Municipal', u'FGTS', u'CAM', u'Outras certidões']

        self.tcId = wx.TextCtrl(self.panelvizualizaCertidao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.certidao.id))

        self.stCompetencia = wx.StaticText(self.panelvizualizaCertidao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelvizualizaCertidao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)
        self.cbCompetencia.SetValue(self.certidao.competencia)

        wx.StaticBox(self.panelvizualizaCertidao, -1, pos=(5, 50), size=(420, 80))

        self.stNumeroProcesso = wx.StaticText(self.panelvizualizaCertidao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelvizualizaCertidao, -1, pos=(10, 90), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbNumeroProcesso.Bind(wx.EVT_COMBOBOX, self.insereParticipante)
        self.insereNumeroProcesso(None)
        self.cbNumeroProcesso.SetValue(self.certidao.numeroProcesso)

        self.stCicParticipante = wx.StaticText(self.panelvizualizaCertidao, -1, u'CPF/CNPJ Participante', pos=(170, 70))
        self.cbCicParticipante = wx.ComboBox(self.panelvizualizaCertidao, -1, pos=(170, 90), size=(140, -1), choices=[], style=wx.CB_READONLY)
        self.cbCicParticipante.Bind(wx.EVT_COMBOBOX, self.insereTipoPessoa)
        
        self.stTipoPessoa = wx.StaticText(self.panelvizualizaCertidao, -1, u'Tipo Pessoa', pos=(320, 70))
        self.tcTipoPessoa = wx.TextCtrl(self.panelvizualizaCertidao, -1, pos=(320, 90), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcTipoPessoa.SetEditable(False)
        self.tcTipoPessoa.SetValue(self.certidao.tipoJuridico)

        wx.StaticBox(self.panelvizualizaCertidao, -1, pos=(5, 130), size=(420, 140))

        self.stTipoCertidao = wx.StaticText(self.panelvizualizaCertidao, -1, u'Tipo Certidão', pos=(10, 150))
        self.cbTipoCertidao = wx.ComboBox(self.panelvizualizaCertidao, -1, pos=(10, 170), size=(100, -1), choices=self.tipoCertidao, style=wx.CB_READONLY)
        self.cbTipoCertidao.SetValue(self.certidao.tipoCertidao)
        
        self.stNumeroCertidao = wx.StaticText(self.panelvizualizaCertidao, -1, u'Número Certidão', pos=(170, 150))
        self.tcNumeroCertidao = wx.TextCtrl(self.panelvizualizaCertidao, -1, pos=(170, 170), size=(120, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroCertidao.SetMaxLength(25)
        self.tcNumeroCertidao.SetValue(self.certidao.numeroCertidao)

        self.stDataEmissao = wx.StaticText(self.panelvizualizaCertidao, -1, u'Data de Emissão', pos=(10, 210), style=wx.ALIGN_LEFT)
        self.tcdataEmissao = masked.TextCtrl(self.panelvizualizaCertidao, -1, mask="##/##/####")
        self.tcdataEmissao.SetSize((80, -1))
        self.tcdataEmissao.SetPosition((10, 230))
        self.tcdataEmissao.SetValue(self.certidao.dataEmissao)

        self.stDataValidade = wx.StaticText(self.panelvizualizaCertidao, -1, u'Data de Validade', pos=(170, 210), style=wx.ALIGN_LEFT)
        self.tcDataValidade = masked.TextCtrl(self.panelvizualizaCertidao, -1, mask="##/##/####")
        self.tcDataValidade.SetSize((80, -1))
        self.tcDataValidade.SetPosition((170, 230))
        self.tcDataValidade.SetValue(self.certidao.dataValidade)


        self.btnSalvar = wx.Button(self.panelvizualizaCertidao, -1, u"Alterar", pos=(150, 320))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarCertidao)
        self.btnCancelar = wx.Button(self.panelvizualizaCertidao, -1, u"Cancelar", pos=(250, 320))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaCertidao)      

        self.insereParticipante(None)
        self.cbCicParticipante.SetValue(self.certidao.cicParticipante)

        #Bind
        self.windowVizualizaCertidao.Bind(wx.EVT_CLOSE, self.quitVizualizaCertidao)



        self.windowVizualizaCertidao.Centre()
        self.windowVizualizaCertidao.Show()

    def quitVizualizaCertidao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowVizualizaCertidao.Destroy()

    def editarCertidao(self, event):

        if self.valida():
            
            self.certidao.numeroProcesso = unicode(self.cbNumeroProcesso.GetValue())
            self.certidao.cicParticipante = unicode(self.cbCicParticipante.GetValue())
            self.certidao.tipoCertidao = unicode(self.cbTipoCertidao.GetValue())
            self.certidao.tipoJuridico = unicode(self.tcTipoPessoa.GetValue())
            self.certidao.numeroCertidao = unicode(self.tcNumeroCertidao.GetValue())
            self.certidao.dataEmissao = unicode(self.tcdataEmissao.GetValue())
            self.certidao.dataValidade = unicode(self.tcDataValidade.GetValue())
            self.certidao.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'A certidão foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.certidao = None
            self.quitVizualizaCertidao(None)

    def excluiCertidao(self, event, idCertidao):

        if idCertidao is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Certidão?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.certidao = Certidao.query.filter_by(id=idCertidao).first()
            self.certidao.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Certidão excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal() 

    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(710, 470), pos=(300, 170), title=u"Gerar Arquivo de Certidão", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
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
        self.certidaoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(300, 300), style=wx.LC_REPORT)
        self.certidaoGeraArquivoListCtrl.InsertColumn(0, u'Licitação', width=100)
        self.certidaoGeraArquivoListCtrl.InsertColumn(1, u'Certidão', width=80)
        self.certidaoGeraArquivoListCtrl.InsertColumn(2, u'Tipo', width=80)
        self.certidaoGeraArquivoListCtrl.InsertColumn(3, u'Partic.', width=70)
        self.certidaoGeraArquivoListCtrl.InsertColumn(4, u'', width=0)
        self.certidaoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensCotacaoGeraArquivos)

        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(310, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(310, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.certidaoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(300, 300), style=wx.LC_REPORT)
        self.certidaoParaArquivoListCtrl.InsertColumn(0, u'Licitação', width=100)
        self.certidaoParaArquivoListCtrl.InsertColumn(1, u'Certidão', width=80)
        self.certidaoParaArquivoListCtrl.InsertColumn(2, u'Tipo', width=80)
        self.certidaoParaArquivoListCtrl.InsertColumn(3, u'Partic.', width=70)
        self.certidaoParaArquivoListCtrl.InsertColumn(4, u'', width=0)
        self.certidaoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensCotacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereCotacaoPorCompetencia(self, event):

        certidoes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            certidoes = Certidao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            certidoes = Certidao.query.all()

        self.certidaoGeraArquivoListCtrl.DeleteAllItems()

        if not certidoes:
            self.message = wx.MessageDialog(None, u'Não existe Cotações para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(certidoes) == self.certidaoParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for certidao in certidoes:
                    igual = False
                    if self.certidaoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.certidaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(certidao.numeroProcesso))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(certidao.numeroCertidao))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(certidao.tipoCertidao))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(certidao.cicParticipante))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(certidao.id))
                        igual = True

                    else:

                        for x in range(self.certidaoParaArquivoListCtrl.GetItemCount()):

                            if certidao.tipoCertidao == unicode(self.certidaoParaArquivoListCtrl.GetItem(x, 2).GetText()) and certidao.numeroCertidao == unicode(self.certidaoParaArquivoListCtrl.GetItem(x, 1).GetText()):
                                igual = True

                    if not igual:

                        index = self.certidaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(certidao.numeroProcesso))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(certidao.numeroCertidao))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(certidao.tipoCertidao))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(certidao.cicParticipante))
                        self.certidaoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(certidao.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensCotacaoGeraArquivos(self, event):

        item = self.certidaoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.certidaoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensCotacaoParaArquivo(self, event):

        item = self.certidaoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.certidaoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Licitações a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.certidaoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.certidaoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.certidaoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.certidaoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.certidaoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.certidaoGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.certidaoParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.certidaoGeraArquivoListCtrl.GetItem(item, 3).GetText()))
                self.certidaoParaArquivoListCtrl.SetStringItem(index, 4, unicode(self.certidaoGeraArquivoListCtrl.GetItem(item, 4).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.certidaoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as licitações a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.certidaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.certidaoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.certidaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.certidaoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.certidaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.certidaoParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.certidaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.certidaoParaArquivoListCtrl.GetItem(item, 3).GetText()))
                self.certidaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.certidaoParaArquivoListCtrl.GetItem(item, 4).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.certidaoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.certidaoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as certidões para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="CERTIDAO.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                            self.message = wx.MessageDialog(None, u'Arquivo de certidões gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de certidões gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.certidaoParaArquivoListCtrl.GetItemCount()):

            try:

                idCertidao = int(self.certidaoParaArquivoListCtrl.GetItem(x, 4).GetText())
                certidao = Certidao.query.filter_by(id=idCertidao).first()

                f.write(unicode(certidao.numeroProcesso.ljust(18).replace("'", "").replace("\"", "")))
                f.write(unicode(self.retiraCaracteresCpfCnpj(certidao.cicParticipante).zfill(14)))
                f.write(unicode(self.transformaTipoCertidao(certidao.tipoCertidao).zfill(2)))
                f.write(unicode(self.transformaTipoJuridico(certidao.tipoJuridico)))
                f.write(unicode(certidao.numeroCertidao.ljust(60).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaData(certidao.dataEmissao)))
                f.write(unicode(self.transformaData(certidao.dataValidade)))
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
 

    def transformaTipoCertidao(self, tipo):

        if tipo == u'INSS':
            return '1'
        elif tipo == u'Federal':
            return '2'
        elif tipo == u'Estadual':
            return '3'
        elif tipo == u'Municipal':
            return '4'
        elif tipo == u'FGTS':
            return '5'
        elif tipo == u'CAM':
            return '6'
        elif tipo == u'CNDT':
            return '7'
        else:
            return '99'

    def transformaTipoJuridico(self, tipo):
        if tipo == u'Física':
            return '1'
        elif tipo == u'Jurídica':
            return '2'
        else:
            return '3'

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]




