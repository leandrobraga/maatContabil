# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_CONTA_NOVO = 5001
ID_TOOLBAR_CONTA_EDITAR = 5002
ID_TOOLBAR_CONTA_EXCLUIR = 5003
ID_TOOLBAR_CONTA_CRIAR_ARQUIVO = 504

SHEET_NAME = 'MXM'

class WindowConta(wx.MiniFrame):
    


    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 320), pos=(300, 170), title=u"Contas", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.panelConta = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTA_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova Contas')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTA_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita Conta selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTA_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui Conta selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_CONTA_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de conta')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        
        
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.tiposSaldoConta = [u'Crédito', u'Débito', u'Mista']

        self.tiposConta = [u'Conta Bancária', u'Conta de Receita',u'Conta de Despesa', u'Outras Contas Contábeis']

        planoContas = PlanoConta.query.all()
        
        self.codigosConta = []
        self.nomesConta = []

        for planoConta in planoContas:
            self.codigosConta.append(planoConta.conta)
            self.nomesConta.append(planoConta.descricao)

        self.cbCompetenciaForView = wx.ComboBox(self.panelConta, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.contaListCtrl = wx.ListCtrl(self.panelConta, wx.ID_ANY, pos=(0, 30), size=(525, 230), style=wx.LC_REPORT)
        self.contaListCtrl.InsertColumn(0, u'Conta', width=200)
        self.contaListCtrl.InsertColumn(1, u'Nome', width=300)
        self.contaListCtrl.InsertColumn(2, u'', width=0)
        self.contaListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.contaListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None
        #self.insereInCtrList(None)

        self.hbox1.Add(self.contaListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoConta, id=ID_TOOLBAR_CONTA_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaConta(event, self.idSelecionado), id=ID_TOOLBAR_CONTA_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiConta(event, self.idSelecionado), id=ID_TOOLBAR_CONTA_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_CONTA_CRIAR_ARQUIVO)

        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, importar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_CONTA_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_CONTA_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_CONTA_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_CONTA_CRIAR_ARQUIVO, importar)

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.contaListCtrl.GetItem(event.GetIndex(), 2).GetText()

    def insereInCtrList(self, event):

        self.contaListCtrl.DeleteAllItems()

        contas = Conta.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

        for conta in contas:

            index = self.contaListCtrl.InsertStringItem(sys.maxint, unicode(conta.codigoConta))
            self.contaListCtrl.SetStringItem(index, 1, unicode(conta.nomeConta))
            self.contaListCtrl.SetStringItem(index, 2, unicode(conta.id))
            

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127 or event.GetKeyCode() == 46:
                event.Skip()
        else:
            event.Skip()

    def novoConta(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoConta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(640, 450), pos=(300, 170), title=u'Novo - Contas', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoConta = wx.Panel(self.windowNovoConta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelNovoConta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        wx.StaticBox(self.panelNovoConta, -1, pos=(5, 45), size=(620, 130))

        self.stCompetencia = wx.StaticText(self.panelNovoConta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoConta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        
        self.stCodigoConta = wx.StaticText(self.panelNovoConta, -1, u'Código da Conta', pos=(10, 60))
        self.cbCodigoConta = wx.ComboBox(self.panelNovoConta, -1, pos=(10, 80), size=(110, -1), choices=self.codigosConta, style=wx.CB_READONLY)
        
        self.stNomeConta = wx.StaticText(self.panelNovoConta, -1, u'Nome da Conta', pos=(150, 60))
        self.cbNomeConta = wx.ComboBox(self.panelNovoConta, -1, pos=(150, 80), size=(300, -1), choices=self.nomesConta, style=wx.CB_READONLY)
        
        self.stAnoConta = wx.StaticText(self.panelNovoConta, -1, u'Ano de Criação da Conta', pos=(470, 60))
        self.tcAnoConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(470, 80), size=(122, -1), style=wx.ALIGN_LEFT)
        self.tcAnoConta.SetMaxLength(4)
        self.tcAnoConta.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stNivelConta = wx.StaticText(self.panelNovoConta, -1, u'Nível da Conta no Plano de Contas', pos=(10, 120))
        self.tcNivelConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(10, 140), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcNivelConta.SetMaxLength(2)
        
        wx.StaticBox(self.panelNovoConta, -1, pos=(5, 180), size=(620, 180))
        
        self.stRecebeConta = wx.StaticText(self.panelNovoConta, -1, u'Recebe lançamento ?', pos=(10, 190))
        self.cbRecebeConta = wx.ComboBox(self.panelNovoConta, -1, pos=(10, 210), size=(40, -1), choices=['S','N'], style=wx.CB_READONLY)

        self.stTipoSaldoConta = wx.StaticText(self.panelNovoConta, -1, u'Tipo de Saldo da Conta', pos=(160, 190))
        self.cbTipoSaldoConta = wx.ComboBox(self.panelNovoConta, -1, pos=(160, 210), size=(80, -1), choices=self.tiposSaldoConta, style=wx.CB_READONLY)

        self.stCodigoSuperiorConta = wx.StaticText(self.panelNovoConta, -1, u'Código da Conta Superior', pos=(310, 190))
        self.tcCodigoSuperiorConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(310, 210), size=(125, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoSuperiorConta.SetMaxLength(34)
                
        self.stCodigoReduzidoConta = wx.StaticText(self.panelNovoConta, -1, u'Código Reduzido da Conta', pos=(470, 190))
        self.tcCodigoReduzidoConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(470, 210), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoReduzidoConta.SetMaxLength(8)
        self.tcCodigoReduzidoConta.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stCodigoItemConta = wx.StaticText(self.panelNovoConta, -1, u'Código do Item Orçamentário Ligado a Conta', pos=(10, 250))
        self.tcCodigoItemConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(10, 270), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoItemConta.SetMaxLength(9)
        self.tcCodigoItemConta.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stCodigoBancoConta = wx.StaticText(self.panelNovoConta, -1, u'Código do banco', pos=(250, 250))
        self.tcCodigoBancoConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(250, 270), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoBancoConta.SetMaxLength(4)
        self.tcCodigoBancoConta.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stCodigoAgenciaConta = wx.StaticText(self.panelNovoConta, -1, u'Código da agência', pos=(360, 250))
        self.tcCodigoAgenciaConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(360, 270), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoAgenciaConta.SetMaxLength(6)
        self.tcCodigoAgenciaConta.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stNumeroConta = wx.StaticText(self.panelNovoConta, -1, u'Número conta bancária', pos=(470, 250))
        self.tcNumeroConta = wx.TextCtrl(self.panelNovoConta, -1, pos=(470, 270), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroConta.SetMaxLength(10)
        
        self.stTipoConta = wx.StaticText(self.panelNovoConta, -1, u'Tipo Conta Contábil', pos=(10, 310))
        self.cbTipoConta = wx.ComboBox(self.panelNovoConta, -1, pos=(10, 330), size=(130, -1), choices=self.tiposConta, style=wx.CB_READONLY)

        self.stCodigoContaTc = wx.StaticText(self.panelNovoConta, -1, u'Código Conta TC', pos=(170, 310))
        self.tcCodigoContaTc = wx.TextCtrl(self.panelNovoConta, -1, pos=(170, 330), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoContaTc.SetMaxLength(3)
        self.tcCodigoContaTc.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stAnoContaSuperior = wx.StaticText(self.panelNovoConta, -1, u'Ano de Criação da Conta Superior', pos=(310, 310))
        self.tcAnoContaSuperior = wx.TextCtrl(self.panelNovoConta, -1, pos=(310, 330), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcAnoContaSuperior.SetMaxLength(4)
        self.tcAnoContaSuperior.Bind(wx.EVT_CHAR, self.escapaChar)

        self.btnSalvar = wx.Button(self.panelNovoConta, -1, u"Salvar", pos=(220, 380))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarConta)
        self.btnCancelar = wx.Button(self.panelNovoConta, -1, u"Cancelar", pos=(320, 380))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoConta)      

        #Bind
        self.windowNovoConta.Bind(wx.EVT_CLOSE, self.quitNovoConta)

        self.windowNovoConta.Centre()
        self.windowNovoConta.Show()

    def quitNovoConta(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoConta.Destroy()

    def vizualizaConta(self,event,idConta):
        
        if idConta is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Conta foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.toolBarControler(False, False, False, False)

        self.conta = Conta.query.filter_by(id=idConta).first()

        self.windowEditaConta = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(640, 450), pos=(300, 170), title=u'Editar - Contas', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelEditaConta = wx.Panel(self.windowEditaConta, wx.ID_ANY)
        
        self.tcId = wx.TextCtrl(self.panelEditaConta, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.conta.id))

        wx.StaticBox(self.panelEditaConta, -1, pos=(5, 45), size=(620, 130))

        self.stCompetencia = wx.StaticText(self.panelEditaConta, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelEditaConta, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.conta.competencia)

        self.stCodigoConta = wx.StaticText(self.panelEditaConta, -1, u'Código da Conta', pos=(10, 60))
        self.cbCodigoConta = wx.ComboBox(self.panelEditaConta, -1, pos=(10, 80), size=(110, -1), choices=self.codigosConta, style=wx.CB_READONLY)
        self.cbCodigoConta.SetValue(self.conta.codigoConta)

        self.stNomeConta = wx.StaticText(self.panelEditaConta, -1, u'Nome da Conta', pos=(150, 60))
        self.cbNomeConta = wx.ComboBox(self.panelEditaConta, -1, pos=(150, 80), size=(300, -1), choices=self.nomesConta, style=wx.CB_READONLY)
        self.cbNomeConta.SetValue(self.conta.nomeConta)

        self.stAnoConta = wx.StaticText(self.panelEditaConta, -1, u'Ano de Criação da Conta', pos=(470, 60))
        self.tcAnoConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(470, 80), size=(122, -1), style=wx.ALIGN_LEFT)
        self.tcAnoConta.SetMaxLength(4)
        self.tcAnoConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAnoConta.SetValue(self.conta.anoConta)

        self.stNivelConta = wx.StaticText(self.panelEditaConta, -1, u'Nível da Conta no Plano de Contas', pos=(10, 120))
        self.tcNivelConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(10, 140), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcNivelConta.SetMaxLength(2)
        self.tcNivelConta.SetValue(self.conta.nivelConta)
        
        wx.StaticBox(self.panelEditaConta, -1, pos=(5, 180), size=(620, 180))
        
        self.stRecebeConta = wx.StaticText(self.panelEditaConta, -1, u'Recebe lançamento ?', pos=(10, 190))
        self.cbRecebeConta = wx.ComboBox(self.panelEditaConta, -1, pos=(10, 210), size=(40, -1), choices=['S','N'], style=wx.CB_READONLY)
        self.cbRecebeConta.SetValue(self.conta.recebeLancamento)

        self.stTipoSaldoConta = wx.StaticText(self.panelEditaConta, -1, u'Tipo de Saldo da Conta', pos=(160, 190))
        self.cbTipoSaldoConta = wx.ComboBox(self.panelEditaConta, -1, pos=(160, 210), size=(80, -1), choices=self.tiposSaldoConta, style=wx.CB_READONLY)
        self.cbTipoSaldoConta.SetValue(self.conta.tipoSaldo)

        self.stCodigoSuperiorConta = wx.StaticText(self.panelEditaConta, -1, u'Código da Conta Superior', pos=(310, 190))
        self.tcCodigoSuperiorConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(310, 210), size=(125, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoSuperiorConta.SetMaxLength(34)
        self.tcCodigoSuperiorConta.SetValue(self.conta.codigoContaSuperior)
                
        self.stCodigoReduzidoConta = wx.StaticText(self.panelEditaConta, -1, u'Código Reduzido da Conta', pos=(470, 190))
        self.tcCodigoReduzidoConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(470, 210), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoReduzidoConta.SetMaxLength(8)
        self.tcCodigoReduzidoConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcCodigoReduzidoConta.SetValue(self.conta.codigoReduzido)

        self.stCodigoItemConta = wx.StaticText(self.panelEditaConta, -1, u'Código do Item Orçamentário Ligado a Conta', pos=(10, 250))
        self.tcCodigoItemConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(10, 270), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoItemConta.SetMaxLength(9)
        self.tcCodigoItemConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcCodigoItemConta.SetValue(self.conta.codigoItem)

        self.stCodigoBancoConta = wx.StaticText(self.panelEditaConta, -1, u'Código do banco', pos=(250, 250))
        self.tcCodigoBancoConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(250, 270), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoBancoConta.SetMaxLength(4)
        self.tcCodigoBancoConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcCodigoBancoConta.SetValue(self.conta.codigoBanco)

        self.stCodigoAgenciaConta = wx.StaticText(self.panelEditaConta, -1, u'Código da agência', pos=(360, 250))
        self.tcCodigoAgenciaConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(360, 270), size=(80, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoAgenciaConta.SetMaxLength(6)
        self.tcCodigoAgenciaConta.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcCodigoAgenciaConta.SetValue(self.conta.codigoAgencia)

        self.stNumeroConta = wx.StaticText(self.panelEditaConta, -1, u'Número conta bancária', pos=(470, 250))
        self.tcNumeroConta = wx.TextCtrl(self.panelEditaConta, -1, pos=(470, 270), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcNumeroConta.SetMaxLength(10)
        self.tcNumeroConta.SetValue(self.conta.numeroConta)

        self.stTipoConta = wx.StaticText(self.panelEditaConta, -1, u'Tipo Conta Contábil', pos=(10, 310))
        self.cbTipoConta = wx.ComboBox(self.panelEditaConta, -1, pos=(10, 330), size=(130, -1), choices=self.tiposConta, style=wx.CB_READONLY)
        self.cbTipoConta.SetValue(self.conta.tipoConta)

        self.stCodigoContaTc = wx.StaticText(self.panelEditaConta, -1, u'Código Conta TC', pos=(170, 310))
        self.tcCodigoContaTc = wx.TextCtrl(self.panelEditaConta, -1, pos=(170, 330), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcCodigoContaTc.SetMaxLength(3)
        self.tcCodigoContaTc.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcCodigoContaTc.SetValue(self.conta.codigoTc)

        self.stAnoContaSuperior = wx.StaticText(self.panelEditaConta, -1, u'Ano de Criação da Conta Superior', pos=(310, 310))
        self.tcAnoContaSuperior = wx.TextCtrl(self.panelEditaConta, -1, pos=(310, 330), size=(100, -1), style=wx.ALIGN_LEFT)
        self.tcAnoContaSuperior.SetMaxLength(4)
        self.tcAnoContaSuperior.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAnoContaSuperior.SetValue(self.conta.anoContaSuperior)

        self.btnSalvar = wx.Button(self.panelEditaConta, -1, u"Salvar", pos=(220, 380))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarConta)
        self.btnCancelar = wx.Button(self.panelEditaConta, -1, u"Cancelar", pos=(320, 380))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitContaEdita)      

        #Bind
        self.windowEditaConta.Bind(wx.EVT_CLOSE, self.quitContaEdita)

        self.windowEditaConta.Centre()
        self.windowEditaConta.Show()

        

    def quitContaEdita(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaConta.Destroy()

    def valida(self):

        if self.cbCompetencia.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Competência!', 'Info', wx.OK)
            self.cbCompetencia.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbCodigoConta.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Código da Conta!', 'Info', wx.OK)
            self.cbCodigoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbNomeConta.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Nome da Conta!', 'Info', wx.OK)
            self.cbNomeConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcAnoConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Ano de Criação da Conta deve ser preenchido!', 'Info', wx.OK)
            self.tcAnoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if len(self.tcAnoConta.GetValue()) < 4:
            self.message = wx.MessageDialog(None, u'O campo Ano de Criação da Conta deve possuir 4 dígitos!', 'Info', wx.OK)
            self.tcAnoConta.SetFocus()
            self.message.ShowModal()
            return 0
        

        if self.tcNivelConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Nível da Conta no Plano de Contas deve ser preenchido!', 'Info', wx.OK)
            self.tcNivelConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbRecebeConta.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Recebe lançamento!', 'Info', wx.OK)
            self.cbRecebeConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.cbTipoSaldoConta.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo de Saldo da Conta!', 'Info', wx.OK)
            self.cbTipoSaldoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoSuperiorConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Código da Conta Superior deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoSuperiorConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoReduzidoConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Código Reduzido da Conta deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoReduzidoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoItemConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Código do Item Orçamentário Ligado a Conta deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoItemConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoBancoConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Código do banco deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoBancoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoAgenciaConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Código da agência deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoAgenciaConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcNumeroConta.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Número conta bancária deve ser preenchido!', 'Info', wx.OK)
            self.tcNumeroConta.SetFocus()
            self.message.ShowModal()
            return 0


        if self.cbTipoConta.GetSelection() == -1:
            self.message = wx.MessageDialog(None, u'Selecione uma opção no campo Tipo Conta Contábil!', 'Info', wx.OK)
            self.cbTipoConta.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcCodigoContaTc.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Código Conta TC deve ser preenchido!', 'Info', wx.OK)
            self.tcCodigoContaTc.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcAnoContaSuperior.GetValue() == "":
            self.message = wx.MessageDialog(None, u'O campo Ano de Criação da Conta Superior deve ser prenchido!', 'Info', wx.OK)
            self.tcAnoContaSuperior.SetFocus()
            self.message.ShowModal()
            return 0

        if len(self.tcAnoContaSuperior.GetValue()) < 4:
            self.message = wx.MessageDialog(None, u'O campo Ano de Criação da Conta Superior deve possuir 4 dígitos!', 'Info', wx.OK)
            self.tcAnoContaSuperior.SetFocus()
            self.message.ShowModal()
            return 0


        return 1

    def editarConta(self, event):

        if self.valida():

            self.conta.anoConta = unicode(self.tcAnoConta.GetValue())
            self.conta.codigoConta = unicode(self.cbCodigoConta.GetValue())
            self.conta.nomeConta = unicode(self.cbNomeConta.GetValue())
            self.conta.nivelConta = unicode(self.tcNivelConta.GetValue())
            self.conta.recebeLancamento = unicode(self.cbRecebeConta.GetValue())
            self.conta.tipoSaldo = unicode(self.cbTipoSaldoConta.GetValue())
            self.conta.codigoContaSuperior = unicode(self.tcCodigoSuperiorConta.GetValue())
            self.conta.codigoReduzido = unicode(self.tcCodigoReduzidoConta.GetValue())
            self.conta.codigoItem = unicode(self.tcCodigoItemConta.GetValue())
            self.conta.codigoBanco = unicode(self.tcCodigoBancoConta.GetValue())
            self.conta.codigoAgencia = unicode(self.tcCodigoAgenciaConta.GetValue())
            self.conta.numeroConta = unicode(self.tcNumeroConta.GetValue())
            self.conta.tipoConta = unicode(self.cbTipoConta.GetValue())
            self.conta.codigoTc = unicode(self.tcCodigoContaTc.GetValue())
            self.conta.anoContaSuperior = unicode(self.tcAnoContaSuperior.GetValue())
            self.conta.competencia = unicode(self.cbCompetencia.GetValue())

            session.commit()
            self.message = wx.MessageDialog(None, u'A Conta foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.conta = None
            self.windowEditaConta.Close()

    
    def salvarConta(self, event):

        if self.valida():
            
            try:
                Conta(
                    anoConta = unicode(self.tcAnoConta.GetValue()),
                    codigoConta = unicode(self.cbCodigoConta.GetValue()),
                    nomeConta = unicode(self.cbNomeConta.GetValue()),
                    nivelConta = unicode(self.tcNivelConta.GetValue()),
                    recebeLancamento = unicode(self.cbRecebeConta.GetValue()),
                    tipoSaldo = unicode(self.cbTipoSaldoConta.GetValue()),
                    codigoContaSuperior = unicode(self.tcCodigoSuperiorConta.GetValue()),
                    codigoReduzido = unicode(self.tcCodigoReduzidoConta.GetValue()),
                    codigoItem = unicode(self.tcCodigoItemConta.GetValue()),
                    codigoBanco= unicode(self.tcCodigoBancoConta.GetValue()),
                    codigoAgencia = unicode(self.tcCodigoAgenciaConta.GetValue()),
                    numeroConta = unicode(self.tcNumeroConta.GetValue()),
                    tipoConta = unicode(self.cbTipoConta.GetValue()),
                    codigoTc = unicode(self.tcCodigoContaTc.GetValue()),
                    anoContaSuperior = unicode(self.tcAnoContaSuperior.GetValue()),
                    competencia = unicode(self.cbCompetencia.GetValue()),

                    )
            
                session.commit()
                self.message = wx.MessageDialog(None, u'Conta salva com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
                self.insereInCtrList(None)
                self.windowNovoConta.Close()

            except:
                self.message = wx.MessageDialog(None, u'Houve um erro ao inserir os dados no banco de dados!\nReinicie a aplicação e tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                self.windowNovoConta.Close()

    def editarPlanoConta(self, event):

        if self.valida():

            self.planoConta.conta = unicode(self.tcConta.GetValue())
            self.planoConta.descricao = unicode(self.tcDescricao.GetValue())
            
            session.commit()
            self.message = wx.MessageDialog(None, u'A conta foi alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.toolBarControler(True, True, True, True)
            self.insereInCtrList(None)
            self.planoConta = None
            self.windowEditaPlanoConta.Close()

    def excluiConta(self, event, idConta):

        if idConta is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Conta foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        
        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta Conta?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()

        if ret == wx.ID_YES:
            self.conta = Conta.query.filter_by(id=idConta).first()
            self.conta.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Conta excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()


    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Contas", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereContaPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.contasGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.contasGeraArquivoListCtrl.InsertColumn(0, u'Conta', width=130)
        self.contasGeraArquivoListCtrl.InsertColumn(1, u'Nome', width=120)
        self.contasGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.contasGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoGeraArquivos)

        self.btnGerarComTudo = wx.Button(self.panelGeraArquivo, -1, u">|", pos=(290, 150))
        self.btnGerarComTudo.Bind(wx.EVT_BUTTON, self.insereTudo)
        self.btnGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)
        
        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.contasParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.contasParaArquivoListCtrl.InsertColumn(0, u'Conta', width=130)
        self.contasParaArquivoListCtrl.InsertColumn(1, u'Nome', width=120)
        self.contasParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.contasParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensLicitacaoParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)
        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()


    def selecionaItensLicitacaoGeraArquivos(self, event):

        item = self.contasGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.contasGeraArquivoListCtrl.GetNextSelected(item)

    def insereContaPorCompetencia(self, event):

        contas = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            contas = Conta.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            contas = Conta.query.all()

        self.contasGeraArquivoListCtrl.DeleteAllItems()

        if not contas:
            self.message = wx.MessageDialog(None, u'Não existe Contas para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(contas) == self.contasParaArquivoListCtrl.GetItemCount():
                pass

            else:

                for conta in contas:
                    igual = False
                    if self.contasParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.contasGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(conta.codigoConta))
                        self.contasGeraArquivoListCtrl.SetStringItem(index, 1, unicode(conta.nomeConta))
                        self.contasGeraArquivoListCtrl.SetStringItem(index, 2, unicode(conta.id))
                        igual = True

                    else:

                        for x in range(self.contasParaArquivoListCtrl.GetItemCount()):

                            if conta.codigoConta == unicode(self.contasParaArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.contasGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(conta.codigoConta))
                        self.contasGeraArquivoListCtrl.SetStringItem(index, 1, unicode(conta.nomeConta))
                        self.contasGeraArquivoListCtrl.SetStringItem(index, 2, unicode(conta.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def insereTudo(self, event):
        
        self.contasGeraArquivoListCtrl.SetItemState(-1, wx.LIST_STATE_SELECTED , wx.LIST_STATE_SELECTED)
        item = self.contasGeraArquivoListCtrl.GetFirstSelected()
               
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.contasGeraArquivoListCtrl.GetNextSelected(item)

        self.insereGeraArquivo(None)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Contas a serem inseridas!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.contasParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.contasGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.contasParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.contasGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.contasParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.contasGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.contasGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []


    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as contas a serem removidas!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.contasGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.contasParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.contasGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.contasParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.contasGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.contasParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.contasParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []


    def selecionaItensLicitacaoParaArquivo(self, event):

        item = self.contasParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.contasParaArquivoListCtrl.GetNextSelected(item)

    def geraArquivoDialog(self, event):

        if self.contasParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Contas para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            dlg = wx.FileDialog(self, message=u"Salvar ", defaultDir="", defaultFile="CONTAS.REM", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Contas gerado com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Contas gerado com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()


    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.contasParaArquivoListCtrl.GetItemCount()):

            try:

                idConta = int(self.contasParaArquivoListCtrl.GetItem(x, 2).GetText())
                conta = Conta.query.filter_by(id=idConta).first()


                f.write(unicode('0000'))
                f.write(unicode(conta.anoConta.zfill(4)))
                f.write(unicode(conta.codigoConta.ljust(34).replace("'", "").replace("\"", "")))
                f.write(unicode(conta.nomeConta.ljust(50).replace("'", "").replace("\"", "")))
                f.write(unicode(conta.nivelConta.zfill(2)))
                f.write(unicode(conta.recebeLancamento))
                f.write(unicode(self.transformaTipoSaldo(conta.tipoSaldo)))
                f.write(unicode(conta.codigoContaSuperior.ljust(34).replace("'", "").replace("\"", "")))
                f.write(unicode(conta.codigoReduzido.zfill(8)))
                f.write(unicode(conta.codigoItem.zfill(9)))
                f.write(unicode(conta.codigoBanco.zfill(4)))
                f.write(unicode(conta.codigoAgencia.zfill(6)))
                f.write(unicode(conta.numeroConta.ljust(10).replace("'", "").replace("\"", "")))
                f.write(unicode(self.transformaTipoConta(conta.tipoConta)))
                f.write(unicode(conta.codigoTc.zfill(3)))
                f.write(unicode(conta.anoContaSuperior.zfill(4)))
                f.write(u'\n')
                    

            except:
                return 0

        return 1


    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def transformaTipoSaldo(self, tipoSaldo):

        if unicode(tipoSaldo) == u'Crédito':
            return 'C'
        elif unicode(tipoSaldo) == u'Débito':
            return 'D'
        else:
            return 'M'

    def transformaTipoConta(self, tipoConta):
       
        if unicode(tipoConta) == u'Conta Bancária':
            return 1
        elif unicode(tipoConta) == u'Conta de Receita':
            return 2
        elif unicode(tipoConta) == u'Conta de Despesa':
            return 3
        else:
            return 9         




