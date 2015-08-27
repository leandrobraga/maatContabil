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

ID_TOOLBAR_TRANS_NOVO = 6501
ID_TOOLBAR_TRANS_EDITAR = 6502
ID_TOOLBAR_TRANS_EXCLUIR = 6503
ID_TOOLBAR_TRANS_CRIAR_ARQUIVO = 6504


class WindowTransferencia(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 280), pos=(300, 170), title=u"Transferência Voluntária", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelTransferencia = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_TRANS_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova Transferência')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_TRANS_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita transferência selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_TRANS_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui transferência selecionado')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_TRANS_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de transferência')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']

        self.choicesTipoTransf = [u'Termo de Colaboracao', u'Termo de Fomento', u'Termo de Convenio', u'Termo de Parceria ', 
            u'Contrato de Gestao ', u'Termo de Responsabilidade', u'Termo de Cooperacao Tecnica',
            u'Outras transferencias voluntarias', u'Aditivo – Valor', u'Aditivo – Vigencia', u'Outros aditivos']

        self.choicesAtividadePrincipal = [u'Abastecimento', u'Acao Judiciaria', u'Acao Legislativa', u'Administracao de Concessoes',
            u'Administracao de Receitas', u'Administracao Financeira', u'Administracao Geral', u'Alcool', u'Alimentacao e Nutricao',
            u'Assistencia a Crianca a ao Adolescente', u'Assistencia ao Idoso', u'Assistencia ao Portador de Deficiencia', 
            u'Assistencia aos Povos Indigenas', u'Assistencia Comunitaria', u'Assistencia Hospitalar e Ambulatorial',
            u'Atencao Basica', u'Colonizacao', u'Comercializacao', u'Comercio Exterior', u'Comunicacao Social',
            u'Comunicacoes Postais', u'Conservacao de Energia', u'Controle Ambiental', u'Controle Externo', u'Controle Interno',
            u'Cooperacao Internacional', u'Custodia e Reintegracao Social', u'Defesa Aerea', u'Defesa Civil', 
            u'Defesa da Ordem Juridica', u'Defesa do Interesse Publico no Processo Judiciario', u'Defesa Naval', 
            u'Defesa Sanitaria Animal', u'Defesa Sanitaria Vegetal', u'Defesa Terrestre', u'Desenvolvimento Cientifico', 
            u'Desenvolvimento Tecnologico e Engenharia', u'Desporto Comunitario', u'Desporto de Rendimento', u'Difusao Cultural', 
            u'Difusao do Conhecimento Cientifico e Tecnologico', u'Direitos Individuais, Coletivos Difusos', 
            u'Educacao de Jovens e Adultos', u'Educacao Especial', u'Educacao Infantil', u'Empregabilidade', u'Energia Eletrica',
            u'Ensino Fundamental', u'Ensino Medio', u'Ensino Profissional', u'Ensino Superior', u'Extensao Rural', 
            u'Fomento ao Trabalho', u'Formacao de Recursos Humanos', u'Habitacao Rural', u'Habitacao Urbana',
            u'Informacao e Inteligencia', u'Infraestrutura Urbana', u'Irrigacao', u'Lazer', u'Meteorologia', u'Mineracao', 
            u'Normalizacao e Qualidade', u'Normatizacao e Fiscalizacao', u'Ordenamento Territorial', 
            u'Patrimonio Historico, Artistico e Arqueologico', u'Petroleo', u'Planejamento e Orcamento', u'Policiamento',
            u'Preservacao e Conservacao Ambiental', u'Previdencia Basica', u'Previdencia Complementar', 
            u'Previdencia do Regime Estatutario', u'Previdencia Especial', u'Producao Industrial ', u'Promocao Comercial',
            u'Promocao da Producao Animal', u'Promocao da Producao Vegetal', u'Promocao Industrial', u'Propriedade Industrial',
            u'Protecao e Beneficios ao Trabalhador', u'Recuperacao de areas Degradadas', u'Recursos Hidricos', u'Reforma Agraria',
            u'Relacao de Trabalho', u'Relacoes Diplomaticas', u'Representacao Judicial e Extrajudicial', 
            u'Saneamento Basico Rural', u'Saneamento Basico Urbano', u'Servicos Financeiros', u'Servicos Urbanos', 
            u'Suporte Profilatico e Terapeutico', u'Tecnologia da Informatizacao', u'Transporte Aereo', u'Transporte Escolar',
            u'Transporte Hidroviario', u'Transporte Rodoviario', u'Transportes Coletivos Urbanos', u'Transportes Especiais',
            u'Turismo', u'Vigilancia Epidemiologica', u'Vigilancia Sanitaria']

        self.choicesTipoContrapartida = [u'Financeira', u'Economica', u'Financeira e Economica', u'Nao Exigida']

        self.cbCompetenciaForView = wx.ComboBox(self.panelTransferencia, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereTransferenciaListCtrl)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.transferenciaListCtrl = wx.ListCtrl(self.panelTransferencia, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.transferenciaListCtrl.InsertColumn(0, u"CNPJ", width=115)
        self.transferenciaListCtrl.InsertColumn(1, u"Num Transf", width=155)
        self.transferenciaListCtrl.InsertColumn(2, u"Data celebração", width=250)
        self.transferenciaListCtrl.InsertColumn(3, u"", width=0)
        self.transferenciaListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.transferenciaListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.transferenciaListCtrl, 1, wx.EXPAND)

        #Binds

        self.Bind(wx.EVT_CLOSE, self.quit)
        self.Bind(wx.EVT_MENU, self.novoTrans, id=ID_TOOLBAR_TRANS_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.editaWindowTransf(event, self.idSelecionado), id=ID_TOOLBAR_TRANS_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiTrans(event, self.idSelecionado), id=ID_TOOLBAR_TRANS_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_TRANS_CRIAR_ARQUIVO)

        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.transferenciaListCtrl.GetItem(event.GetIndex(), 3).GetText()

    def insereTransferenciaListCtrl(self, event):
        
        self.transferenciaListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            
            transferencias = Transferencia.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()
            for transferencia in transferencias:
                index = self.transferenciaListCtrl.InsertStringItem(sys.maxint, unicode(transferencia.cnpjConvenente))
                self.transferenciaListCtrl.SetStringItem(index, 1, transferencia.numTransf)
                self.transferenciaListCtrl.SetStringItem(index, 2, transferencia.dataCelebracao)
                self.transferenciaListCtrl.SetStringItem(index, 3, unicode(transferencia.id))

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_TRANS_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_TRANS_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_TRANS_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_TRANS_CRIAR_ARQUIVO, gerar)

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def novoTrans(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoTrans = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(880, 650), pos=(300, 170), title=u"Nova - Transferência", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoTrans = wx.Panel(self.windowNovoTrans, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoTrans, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoTrans, -1, u'Competência', pos=(10, 0), style=wx.ALIGN_LEFT)
        self.cbCompetencia = wx.ComboBox(self.panelNovoTrans, -1, pos=(10, 20), size=(250, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)

        self.stCnpjConvenente = wx.StaticText(self.panelNovoTrans, -1, u'CNPJ do Convenente/OSC', pos=(10, 50), style=wx.ALIGN_LEFT)
        self.tcCnpjConvenente = masked.TextCtrl(self.panelNovoTrans, -1, mask="##.###.###/####-##")
        self.tcCnpjConvenente.SetSize((150, -1))
        self.tcCnpjConvenente.SetPosition((10, 70))

        self.stNumTransf = wx.StaticText(self.panelNovoTrans, -1, u'Número da Tran. Vol. / Aditivo', pos=(190, 50), style=wx.ALIGN_LEFT)
        self.tcNumTransf = wx.TextCtrl(self.panelNovoTrans, -1, pos=(190, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumTransf.SetMaxLength(20)

        self.stTipoTransf = wx.StaticText(self.panelNovoTrans, -1, u'Tipo daTransferência / Aditivo', pos=(420, 50), style=wx.ALIGN_LEFT)
        self.cbTipoTransf = wx.ComboBox(self.panelNovoTrans, -1, pos=(420, 70), size=(180, -1), choices=self.choicesTipoTransf, style=wx.CB_READONLY)
        
        self.stNumTransfSuperior = wx.StaticText(self.panelNovoTrans, -1, u'Número da Tran. Vol. Superior', pos=(650, 50), style=wx.ALIGN_LEFT)
        self.tcNumTransfSuperior = wx.TextCtrl(self.panelNovoTrans, -1, pos=(650, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumTransfSuperior.SetMaxLength(20)

        self.stAnoTransf = wx.StaticText(self.panelNovoTrans, -1, u'Ano da Transf.', pos=(10, 110), style=wx.ALIGN_LEFT)
        self.tcAnoTransf = masked.TextCtrl(self.panelNovoTrans, -1, mask="####")
        self.tcAnoTransf.SetSize((50, -1))
        self.tcAnoTransf.SetPosition((10, 130))

        self.stDataCelebracao = wx.StaticText(self.panelNovoTrans, -1, u'Data de celebração', pos=(110, 110), style=wx.ALIGN_LEFT)
        self.tcDataCelebracao = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataCelebracao.SetSize((80, -1))
        self.tcDataCelebracao.SetPosition((110, 130))

        self.stDataInicio = wx.StaticText(self.panelNovoTrans, -1, u'Data início da vigência', pos=(230, 110), style=wx.ALIGN_LEFT)
        self.tcDataInicio = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataInicio.SetSize((80, -1))
        self.tcDataInicio.SetPosition((230, 130))

        self.stDataFim = wx.StaticText(self.panelNovoTrans, -1, u'Data fim da vigência', pos=(370, 110), style=wx.ALIGN_LEFT)
        self.tcDataFim = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataFim.SetSize((80, -1))
        self.tcDataFim.SetPosition((370, 130))

        self.stAtividadePrincipal = wx.StaticText(self.panelNovoTrans, -1, u'Atividade Principal', pos=(500, 110), style=wx.ALIGN_LEFT)
        self.cbAtividadePrincipal = wx.ComboBox(self.panelNovoTrans, -1, pos=(500, 130), size=(320, -1), choices=self.choicesAtividadePrincipal, style=wx.CB_READONLY)
        
        self.stDataPublicacao = wx.StaticText(self.panelNovoTrans, -1, u'Data de publicação', pos=(10, 170), style=wx.ALIGN_LEFT)
        self.tcDataPublicacao = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((10, 190))

        self.stObjeto = wx.StaticText(self.panelNovoTrans, -1, u'Objeto', pos=(140, 170), style=wx.ALIGN_LEFT)
        self.tcObjeto = wx.TextCtrl(self.panelNovoTrans, -1, pos=(140, 190), size=(500, -1), style=wx.ALIGN_LEFT)
        self.tcObjeto.SetMaxLength(300)

        self.stBanco = wx.StaticText(self.panelNovoTrans, -1, u'Banco', pos=(10, 230), style=wx.ALIGN_LEFT)
        self.tcBanco = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 250), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcBanco.SetMaxLength(3)
        self.tcBanco.Bind(wx.EVT_CHAR, self.escapaChar)

        self.stAgenciaBancaria = wx.StaticText(self.panelNovoTrans, -1, u'Agência Bancária', pos=(110, 230), style=wx.ALIGN_LEFT)
        self.tcAgenciaBancaria = wx.TextCtrl(self.panelNovoTrans, -1, pos=(110, 250), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcAgenciaBancaria.SetMaxLength(7)

        self.stContaBancaria = wx.StaticText(self.panelNovoTrans, -1, u'Conta Bancária', pos=(220, 230), style=wx.ALIGN_LEFT)
        self.tcContaBancaria = wx.TextCtrl(self.panelNovoTrans, -1, pos=(220, 250), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcContaBancaria.SetMaxLength(14)

        self.stValorRepasse = wx.StaticText(self.panelNovoTrans, -1, u'Valor Repasse', pos=(380, 230), style=wx.ALIGN_LEFT)
        self.tcValorRepasse = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoTrans, pos=wx.Point(380, 250), style=0, value=0)
        self.tcValorRepasse.SetFractionWidth(2)
        self.tcValorRepasse.SetGroupChar(u"#")
        self.tcValorRepasse.SetDecimalChar(u",")
        self.tcValorRepasse.SetGroupChar(u".")
        self.tcValorRepasse.SetAllowNegative(False)
        #wx.TextCtrl(self.panelNovoTrans, -1, pos=(380, 250), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcValorRepasse.SetMaxLength(18)

        self.stTipoContraPartida = wx.StaticText(self.panelNovoTrans, -1, u'Tipo da Contrapartida', pos=(540, 230), style=wx.ALIGN_LEFT)
        self.cbTipoContraPartida = wx.ComboBox(self.panelNovoTrans, -1, pos=(540, 250), size=(200, -1), choices= self.choicesTipoContrapartida, style=wx.CB_READONLY)
        
        self.stContraPartida = wx.StaticText(self.panelNovoTrans, -1, u'Contrapartida', pos=(10, 290), style=wx.ALIGN_LEFT)
        self.tcContraPartida = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 310), size=(500, -1), style=wx.ALIGN_LEFT)
        self.tcContraPartida.SetMaxLength(300)

        
        self.stContraPartidaFin = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida financeira', pos=(520, 290), style=wx.ALIGN_LEFT)
        self.tcContraPartidaFin = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoTrans, pos=wx.Point(520, 310), style=0, value=0)
        self.tcContraPartidaFin.SetFractionWidth(2)
        self.tcContraPartidaFin.SetGroupChar(u"#")
        self.tcContraPartidaFin.SetDecimalChar(u",")
        self.tcContraPartidaFin.SetGroupChar(u".")
        self.tcContraPartidaFin.SetAllowNegative(False)
        self.tcContraPartidaFin.SetMaxLength(18)
        
        #self.stContraPartidaFin = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida financeira', pos=(520, 290), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaFin = wx.TextCtrl(self.panelNovoTrans, -1, pos=(520, 310), size=(130, -1), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaFin.SetMaxLength(18)

        self.stContraPartidaEco = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida econômico', pos=(690, 290), style=wx.ALIGN_LEFT)
        self.tcContraPartidaEco = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoTrans, pos=wx.Point(690, 310), style=0, value=0)
        self.tcContraPartidaEco.SetFractionWidth(2)
        self.tcContraPartidaEco.SetGroupChar(u"#")
        self.tcContraPartidaEco.SetDecimalChar(u",")
        self.tcContraPartidaEco.SetGroupChar(u".")
        self.tcContraPartidaEco.SetAllowNegative(False)
        self.tcContraPartidaEco.SetMaxLength(18)
        #self.stContraPartidaEco = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida econômico', pos=(690, 290), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaEco = wx.TextCtrl(self.panelNovoTrans, -1, pos=(690, 310), size=(130, -1), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaEco.SetMaxLength(18)

        self.stNomeFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Fiscalizador/Gestor', pos=(10, 350), style=wx.ALIGN_LEFT)
        self.tcNomeFiscalizador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 370), size=(250, -1), style=wx.ALIGN_LEFT)
        self.tcNomeFiscalizador.SetMaxLength(50)

        self.stEmailFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'Email do Fiscalizador/Gestor', pos=(280, 350), style=wx.ALIGN_LEFT)
        self.tcEmailFiscalizador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(280, 370), size=(250, -1), style=wx.ALIGN_LEFT)
        self.tcEmailFiscalizador.SetMaxLength(60)

        self.stCpfFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'CPF Resp. pela Fiscalização/Gestor', pos=(550, 350), style=wx.ALIGN_LEFT)
        self.tcCpfFiscalizador = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfFiscalizador.SetSize((110, -1))
        self.tcCpfFiscalizador.SetPosition((550, 370))

        self.stCargoFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'Cargo/Função do Resp. pela Fiscalização/Gestor', pos=(10, 410), style=wx.ALIGN_LEFT)
        self.tcCargoFiscalizador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 430), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcCargoFiscalizador.SetMaxLength(50)

        self.stNomeExecucao = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Resp. pela execução/dirigente', pos=(280, 410), style=wx.ALIGN_LEFT)
        self.tcNomeExecucao = wx.TextCtrl(self.panelNovoTrans, -1, pos=(280, 430), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcNomeExecucao.SetMaxLength(50)

        self.stEmailExecucao = wx.StaticText(self.panelNovoTrans, -1, u'Email do Resp. pela execução/dirigente', pos=(500, 410), style=wx.ALIGN_LEFT)
        self.tcEmailExecucao = wx.TextCtrl(self.panelNovoTrans, -1, pos=(500, 430), size=(250, -1), style=wx.ALIGN_LEFT)
        self.tcEmailExecucao.SetMaxLength(60)

        self.stCpfExecucao = wx.StaticText(self.panelNovoTrans, -1, u'CPF do Resp. pela execução/dirigente', pos=(10, 470), style=wx.ALIGN_LEFT)
        self.tcCpfExecucao = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfExecucao.SetSize((110, -1))
        self.tcCpfExecucao.SetPosition((10, 490))

        self.stCargoExecucao = wx.StaticText(self.panelNovoTrans, -1, u'Cargo/Função do Resp. pela execução/dirigente', pos=(260, 470), style=wx.ALIGN_LEFT)
        self.tcCargoExecucao = wx.TextCtrl(self.panelNovoTrans, -1, pos=(260, 490), size=(230, -1), style=wx.ALIGN_LEFT)
        self.tcCargoExecucao.SetMaxLength(50)

        self.stNomeAssinaturaRepassador = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Resp. pela assinatura - órgão repassador', pos=(580, 470), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaRepassador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(580, 490), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaRepassador.SetMaxLength(50)

        self.stCpfAssinaturaRepassador = wx.StaticText(self.panelNovoTrans, -1, u'CPF Resp. pela assinatura/repassador', pos=(10, 530), style=wx.ALIGN_LEFT)
        self.tcCpfAssinaturaRepassador = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfAssinaturaRepassador.SetSize((110, -1))
        self.tcCpfAssinaturaRepassador.SetPosition((10, 550))

        self.stNomeAssinaturaConvenente = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Resp. assinatura/convenente/OSC', pos=(220, 530), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaConvenente = wx.TextCtrl(self.panelNovoTrans, -1, pos=(220, 550), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaConvenente.SetMaxLength(50)

        self.stCpfAssinaturaConvenente = wx.StaticText(self.panelNovoTrans, -1, u'CPF Resp. pela assinatura/repassador', pos=(480, 530), style=wx.ALIGN_LEFT)
        self.tcCpfAssinaturaConvenente = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfAssinaturaConvenente.SetSize((110, -1))
        self.tcCpfAssinaturaConvenente.SetPosition((480, 550))

        self.stDataCompetencia = wx.StaticText(self.panelNovoTrans, -1, u'Data Competência(AAAA/MM)', pos=(700, 530), style=wx.ALIGN_LEFT)
        self.tcDataCompetencia = masked.TextCtrl(self.panelNovoTrans, -1, mask="####/##")
        self.tcDataCompetencia.SetSize((80, -1))
        self.tcDataCompetencia.SetPosition((700, 550))
              
        self.btnSalvar = wx.Button(self.panelNovoTrans, -1, "Salvar", pos=(250, 590),size=(-1,22))
        self.btnCancelar = wx.Button(self.panelNovoTrans, -1, "Cancelar", pos=(370, 590),size=(-1,22))

        self.windowNovoTrans.Centre()
        self.windowNovoTrans.Show()

        #Bind
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitTransNovo)
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarTrans)
        self.windowNovoTrans.Bind(wx.EVT_CLOSE, self.quitTransNovo)
        #Fim Bind

    def quitTransNovo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoTrans.Destroy()

    def salvarTrans(self, event):

        #if self.valida():
        Transferencia(
            cnpjConvenente=unicode(self.tcCnpjConvenente.GetValue()),
            numTransf=unicode(self.tcNumTransf.GetValue()), 
            tipoTransf=unicode(self.cbTipoTransf.GetValue()),
            numTransfSuperior=unicode(self.tcNumTransfSuperior.GetValue()),
            anoTransf=unicode(self.tcAnoTransf.GetValue()),
            dataCelebracao=unicode(self.tcDataCelebracao.GetValue()),
            dataInicio=unicode(self.tcDataInicio.GetValue()),
            dataFim=unicode(self.tcDataFim.GetValue()),
            dataPublicacao=unicode(self.tcDataPublicacao.GetValue()),
            atividadePrincipal=unicode(self.cbAtividadePrincipal.GetValue()),
            objeto=unicode(self.tcObjeto.GetValue()),
            banco=unicode(self.tcBanco.GetValue()),
            agenciaBancaria=unicode(self.tcAgenciaBancaria.GetValue()),
            contaBancaria=unicode(self.tcContaBancaria.GetValue()),
            valorRepasse=unicode(self.tcValorRepasse.GetValue()),
            tipoContraPartida=unicode(self.cbTipoContraPartida.GetValue()),
            contraPartida=unicode(self.tcContraPartida.GetValue()),
            contraPartidaFin=unicode(self.tcContraPartidaFin.GetValue()),
            contraPartidaEco=unicode(self.tcContraPartidaEco.GetValue()),
            nomeFiscalizador=unicode(self.tcNomeFiscalizador.GetValue()),
            emailFiscalizador=unicode(self.tcEmailFiscalizador.GetValue()),
            cpfFiscalizador=unicode(self.tcCpfFiscalizador.GetValue()),
            cargoFiscalizador=unicode(self.tcCargoFiscalizador.GetValue()),
            nomeExecucao=unicode(self.tcNomeExecucao.GetValue()),
            emailExecucao=unicode(self.tcEmailExecucao.GetValue()),
            cpfExecucao=unicode(self.tcCpfExecucao.GetValue()),
            cargoExecucao=unicode(self.tcCargoExecucao.GetValue()),
            nomeAssinaturaRepassador=unicode(self.tcNomeAssinaturaRepassador.GetValue()),
            cpfAssinaturaRepassador=unicode(self.tcCpfAssinaturaRepassador.GetValue()),
            nomeAssinaturaConvenente=unicode(self.tcNomeAssinaturaConvenente.GetValue()),
            cpfAssinaturaConvenente=unicode(self.tcCpfAssinaturaConvenente.GetValue()),
            dataCompetencia=unicode(self.tcDataCompetencia.GetValue()),
            competencia=unicode(self.cbCompetencia.GetValue())
        )
        session.commit()
        self.message = wx.MessageDialog(None, u'Transferência salvo com sucesso!', 'Info', wx.OK)
        self.message.ShowModal()
        self.insereTransferenciaListCtrl(None)
        self.windowNovoTrans.Close()

    def editaWindowTransf(self, event, idTrans):

        if idTrans is None:
            self.message = wx.MessageDialog(None, u'Nenhuma transferência foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.transferencia = Transferencia.query.filter_by(id=idTrans).first()

        self.toolBarControler(False, False, False, False)

        self.windowEditaTrans = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(880, 650), pos=(300, 170), title=u"Editar - Transferência", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoTrans = wx.Panel(self.windowEditaTrans, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoTrans, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.transferencia.id))

        self.stCompetencia = wx.StaticText(self.panelNovoTrans, -1, u'Competência', pos=(10, 0), style=wx.ALIGN_LEFT)
        self.cbCompetencia = wx.ComboBox(self.panelNovoTrans, -1, pos=(10, 20), size=(250, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.SetValue(self.transferencia.competencia)
        
        self.stCnpjConvenente = wx.StaticText(self.panelNovoTrans, -1, u'CNPJ do Convenente/OSC', pos=(10, 50), style=wx.ALIGN_LEFT)
        self.tcCnpjConvenente = masked.TextCtrl(self.panelNovoTrans, -1, mask="##.###.###/####-##")
        self.tcCnpjConvenente.SetSize((150, -1))
        self.tcCnpjConvenente.SetPosition((10, 70))
        self.tcCnpjConvenente.SetValue(self.transferencia.cnpjConvenente)

        self.stNumTransf = wx.StaticText(self.panelNovoTrans, -1, u'Número da Tran. Vol. / Aditivo', pos=(190, 50), style=wx.ALIGN_LEFT)
        self.tcNumTransf = wx.TextCtrl(self.panelNovoTrans, -1, pos=(190, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumTransf.SetMaxLength(20)
        self.tcNumTransf.SetValue(self.transferencia.numTransf)

        self.stTipoTransf = wx.StaticText(self.panelNovoTrans, -1, u'Tipo daTransferência / Aditivo', pos=(420, 50), style=wx.ALIGN_LEFT)
        self.cbTipoTransf = wx.ComboBox(self.panelNovoTrans, -1, pos=(420, 70), size=(180, -1), choices=self.choicesTipoTransf, style=wx.CB_READONLY)
        self.cbTipoTransf.SetValue(self.transferencia.tipoTransf)

        self.stNumTransfSuperior = wx.StaticText(self.panelNovoTrans, -1, u'Número da Tran. Vol. Superior', pos=(650, 50), style=wx.ALIGN_LEFT)
        self.tcNumTransfSuperior = wx.TextCtrl(self.panelNovoTrans, -1, pos=(650, 70), size=(190, -1), style=wx.ALIGN_LEFT)
        self.tcNumTransfSuperior.SetMaxLength(20)
        self.tcNumTransfSuperior.SetValue(self.transferencia.numTransfSuperior)

        self.stAnoTransf = wx.StaticText(self.panelNovoTrans, -1, u'Ano da Transf.', pos=(10, 110), style=wx.ALIGN_LEFT)
        self.tcAnoTransf = masked.TextCtrl(self.panelNovoTrans, -1, mask="####")
        self.tcAnoTransf.SetSize((50, -1))
        self.tcAnoTransf.SetPosition((10, 130))
        self.tcAnoTransf.SetValue(self.transferencia.anoTransf)

        self.stDataCelebracao = wx.StaticText(self.panelNovoTrans, -1, u'Data de celebração', pos=(110, 110), style=wx.ALIGN_LEFT)
        self.tcDataCelebracao = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataCelebracao.SetSize((80, -1))
        self.tcDataCelebracao.SetPosition((110, 130))
        self.tcDataCelebracao.SetValue(self.transferencia.dataCelebracao)

        self.stDataInicio = wx.StaticText(self.panelNovoTrans, -1, u'Data início da vigência', pos=(230, 110), style=wx.ALIGN_LEFT)
        self.tcDataInicio = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataInicio.SetSize((80, -1))
        self.tcDataInicio.SetPosition((230, 130))
        self.tcDataInicio.SetValue(self.transferencia.dataInicio)

        self.stDataFim = wx.StaticText(self.panelNovoTrans, -1, u'Data fim da vigência', pos=(370, 110), style=wx.ALIGN_LEFT)
        self.tcDataFim = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataFim.SetSize((80, -1))
        self.tcDataFim.SetPosition((370, 130))
        self.tcDataFim.SetValue(self.transferencia.dataFim)

        self.stAtividadePrincipal = wx.StaticText(self.panelNovoTrans, -1, u'Atividade Principal', pos=(500, 110), style=wx.ALIGN_LEFT)
        self.cbAtividadePrincipal = wx.ComboBox(self.panelNovoTrans, -1, pos=(500, 130), size=(320, -1), choices=self.choicesAtividadePrincipal, style=wx.CB_READONLY)
        self.cbAtividadePrincipal.SetValue(self.transferencia.atividadePrincipal)

        self.stDataPublicacao = wx.StaticText(self.panelNovoTrans, -1, u'Data de publicação', pos=(10, 170), style=wx.ALIGN_LEFT)
        self.tcDataPublicacao = masked.TextCtrl(self.panelNovoTrans, -1, mask="##/##/####")
        self.tcDataPublicacao.SetSize((80, -1))
        self.tcDataPublicacao.SetPosition((10, 190))
        self.tcDataPublicacao.SetValue(self.transferencia.dataPublicacao)

        self.stObjeto = wx.StaticText(self.panelNovoTrans, -1, u'Objeto', pos=(140, 170), style=wx.ALIGN_LEFT)
        self.tcObjeto = wx.TextCtrl(self.panelNovoTrans, -1, pos=(140, 190), size=(500, -1), style=wx.ALIGN_LEFT)
        self.tcObjeto.SetMaxLength(300)
        self.tcObjeto.SetValue(self.transferencia.objeto)

        self.stBanco = wx.StaticText(self.panelNovoTrans, -1, u'Banco', pos=(10, 230), style=wx.ALIGN_LEFT)
        self.tcBanco = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 250), size=(50, -1), style=wx.ALIGN_LEFT)
        self.tcBanco.SetMaxLength(3)
        self.tcBanco.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcBanco.SetValue(self.transferencia.banco)

        self.stAgenciaBancaria = wx.StaticText(self.panelNovoTrans, -1, u'Agência Bancária', pos=(110, 230), style=wx.ALIGN_LEFT)
        self.tcAgenciaBancaria = wx.TextCtrl(self.panelNovoTrans, -1, pos=(110, 250), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcAgenciaBancaria.SetMaxLength(7)
        self.tcAgenciaBancaria.SetValue(self.transferencia.agenciaBancaria)

        self.stContaBancaria = wx.StaticText(self.panelNovoTrans, -1, u'Conta Bancária', pos=(220, 230), style=wx.ALIGN_LEFT)
        self.tcContaBancaria = wx.TextCtrl(self.panelNovoTrans, -1, pos=(220, 250), size=(130, -1), style=wx.ALIGN_LEFT)
        self.tcContaBancaria.SetMaxLength(14)
        self.tcContaBancaria.SetValue(self.transferencia.contaBancaria)

        self.stValorRepasse = wx.StaticText(self.panelNovoTrans, -1, u'Valor Repasse', pos=(380, 230), style=wx.ALIGN_LEFT)
        self.tcValorRepasse = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoTrans, pos=wx.Point(380, 250), style=0, value=0)
        self.tcValorRepasse.SetFractionWidth(2)
        self.tcValorRepasse.SetGroupChar(u"#")
        self.tcValorRepasse.SetDecimalChar(u",")
        self.tcValorRepasse.SetGroupChar(u".")
        self.tcValorRepasse.SetAllowNegative(False)
        self.tcValorRepasse.SetMaxLength(18)
        #self.stValorRepasse = wx.StaticText(self.panelNovoTrans, -1, u'Valor Repasse', pos=(380, 230), style=wx.ALIGN_LEFT)
        #self.tcValorRepasse = wx.TextCtrl(self.panelNovoTrans, -1, pos=(380, 250), size=(130, -1), style=wx.ALIGN_LEFT)
        #self.tcValorRepasse.SetMaxLength(18)
        self.tcValorRepasse.SetValue(float(self.transferencia.valorRepasse))

        self.stTipoContraPartida = wx.StaticText(self.panelNovoTrans, -1, u'Tipo da Contrapartida', pos=(540, 230), style=wx.ALIGN_LEFT)
        self.cbTipoContraPartida = wx.ComboBox(self.panelNovoTrans, -1, pos=(540, 250), size=(200, -1), choices= self.choicesTipoContrapartida, style=wx.CB_READONLY)
        self.cbTipoContraPartida.SetValue(self.transferencia.tipoContraPartida)

        self.stContraPartida = wx.StaticText(self.panelNovoTrans, -1, u'Contrapartida', pos=(10, 290), style=wx.ALIGN_LEFT)
        self.tcContraPartida = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 310), size=(500, -1), style=wx.ALIGN_LEFT)
        self.tcContraPartida.SetMaxLength(300)
        self.tcContraPartida.SetValue(self.transferencia.contraPartida)

        self.stContraPartidaFin = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida financeira', pos=(520, 290), style=wx.ALIGN_LEFT)
        self.tcContraPartidaFin = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoTrans, pos=wx.Point(520, 310), style=0, value=0)
        self.tcContraPartidaFin.SetFractionWidth(2)
        self.tcContraPartidaFin.SetGroupChar(u"#")
        self.tcContraPartidaFin.SetDecimalChar(u",")
        self.tcContraPartidaFin.SetGroupChar(u".")
        self.tcContraPartidaFin.SetAllowNegative(False)
        self.tcContraPartidaFin.SetMaxLength(18)
        #self.stContraPartidaFin = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida financeira', pos=(520, 290), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaFin = wx.TextCtrl(self.panelNovoTrans, -1, pos=(520, 310), size=(130, -1), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaFin.SetMaxLength(18)
        self.tcContraPartidaFin.SetValue(float(self.transferencia.contraPartidaFin))

        self.stContraPartidaEco = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida econômico', pos=(690, 290), style=wx.ALIGN_LEFT)
        self.tcContraPartidaEco = wx.lib.masked.numctrl.NumCtrl(id=-1, parent=self.panelNovoTrans, pos=wx.Point(690, 310), style=0, value=0)
        self.tcContraPartidaEco.SetFractionWidth(2)
        self.tcContraPartidaEco.SetGroupChar(u"#")
        self.tcContraPartidaEco.SetDecimalChar(u",")
        self.tcContraPartidaEco.SetGroupChar(u".")
        self.tcContraPartidaEco.SetAllowNegative(False)
        self.tcContraPartidaEco.SetMaxLength(18)
        #self.stContraPartidaEco = wx.StaticText(self.panelNovoTrans, -1, u'Valor contrapartida econômico', pos=(690, 290), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaEco = wx.TextCtrl(self.panelNovoTrans, -1, pos=(690, 310), size=(130, -1), style=wx.ALIGN_LEFT)
        #self.tcContraPartidaEco.SetMaxLength(18)
        self.tcContraPartidaEco.SetValue(float(self.transferencia.contraPartidaEco))

        self.stNomeFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Fiscalizador/Gestor', pos=(10, 350), style=wx.ALIGN_LEFT)
        self.tcNomeFiscalizador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 370), size=(250, -1), style=wx.ALIGN_LEFT)
        self.tcNomeFiscalizador.SetMaxLength(50)
        self.tcNomeFiscalizador.SetValue(self.transferencia.nomeFiscalizador)

        self.stEmailFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'Email do Fiscalizador/Gestor', pos=(280, 350), style=wx.ALIGN_LEFT)
        self.tcEmailFiscalizador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(280, 370), size=(250, -1), style=wx.ALIGN_LEFT)
        self.tcEmailFiscalizador.SetMaxLength(60)
        self.tcEmailFiscalizador.SetValue(self.transferencia.emailFiscalizador)

        self.stCpfFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'CPF Resp. pela Fiscalização/Gestor', pos=(550, 350), style=wx.ALIGN_LEFT)
        self.tcCpfFiscalizador = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfFiscalizador.SetSize((110, -1))
        self.tcCpfFiscalizador.SetPosition((550, 370))
        self.tcCpfFiscalizador.SetValue(self.transferencia.cpfFiscalizador)

        self.stCargoFiscalizador = wx.StaticText(self.panelNovoTrans, -1, u'Cargo/Função do Resp. pela Fiscalização/Gestor', pos=(10, 410), style=wx.ALIGN_LEFT)
        self.tcCargoFiscalizador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(10, 430), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcCargoFiscalizador.SetMaxLength(50)
        self.tcCargoFiscalizador.SetValue(self.transferencia.cargoFiscalizador)

        self.stNomeExecucao = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Resp. pela execução/dirigente', pos=(280, 410), style=wx.ALIGN_LEFT)
        self.tcNomeExecucao = wx.TextCtrl(self.panelNovoTrans, -1, pos=(280, 430), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcNomeExecucao.SetMaxLength(50)
        self.tcNomeExecucao.SetValue(self.transferencia.nomeExecucao)

        self.stEmailExecucao = wx.StaticText(self.panelNovoTrans, -1, u'Email do Resp. pela execução/dirigente', pos=(500, 410), style=wx.ALIGN_LEFT)
        self.tcEmailExecucao = wx.TextCtrl(self.panelNovoTrans, -1, pos=(500, 430), size=(250, -1), style=wx.ALIGN_LEFT)
        self.tcEmailExecucao.SetMaxLength(60)
        self.tcEmailExecucao.SetValue(self.transferencia.emailExecucao)

        self.stCpfExecucao = wx.StaticText(self.panelNovoTrans, -1, u'CPF do Resp. pela execução/dirigente', pos=(10, 470), style=wx.ALIGN_LEFT)
        self.tcCpfExecucao = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfExecucao.SetSize((110, -1))
        self.tcCpfExecucao.SetPosition((10, 490))
        self.tcCpfExecucao.SetValue(self.transferencia.cpfExecucao)

        self.stCargoExecucao = wx.StaticText(self.panelNovoTrans, -1, u'Cargo/Função do Resp. pela execução/dirigente', pos=(260, 470), style=wx.ALIGN_LEFT)
        self.tcCargoExecucao = wx.TextCtrl(self.panelNovoTrans, -1, pos=(260, 490), size=(230, -1), style=wx.ALIGN_LEFT)
        self.tcCargoExecucao.SetMaxLength(50)
        self.tcCargoExecucao.SetValue(self.transferencia.cargoExecucao)

        self.stNomeAssinaturaRepassador = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Resp. pela assinatura - órgão repassador', pos=(580, 470), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaRepassador = wx.TextCtrl(self.panelNovoTrans, -1, pos=(580, 490), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaRepassador.SetMaxLength(50)
        self.tcNomeAssinaturaRepassador.SetValue(self.transferencia.nomeAssinaturaRepassador)

        self.stCpfAssinaturaRepassador = wx.StaticText(self.panelNovoTrans, -1, u'CPF Resp. pela assinatura/repassador', pos=(10, 530), style=wx.ALIGN_LEFT)
        self.tcCpfAssinaturaRepassador = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfAssinaturaRepassador.SetSize((110, -1))
        self.tcCpfAssinaturaRepassador.SetPosition((10, 550))
        self.tcCpfAssinaturaRepassador.SetValue(self.transferencia.cpfAssinaturaRepassador)

        self.stNomeAssinaturaConvenente = wx.StaticText(self.panelNovoTrans, -1, u'Nome do Resp. assinatura/convenente/OSC', pos=(220, 530), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaConvenente = wx.TextCtrl(self.panelNovoTrans, -1, pos=(220, 550), size=(180, -1), style=wx.ALIGN_LEFT)
        self.tcNomeAssinaturaConvenente.SetMaxLength(50)
        self.tcNomeAssinaturaConvenente.SetValue(self.transferencia.nomeAssinaturaConvenente)

        self.stCpfAssinaturaConvenente = wx.StaticText(self.panelNovoTrans, -1, u'CPF Resp. pela assinatura/repassador', pos=(480, 530), style=wx.ALIGN_LEFT)
        self.tcCpfAssinaturaConvenente = masked.TextCtrl(self.panelNovoTrans, -1, mask="###.###.###-##")
        self.tcCpfAssinaturaConvenente.SetSize((110, -1))
        self.tcCpfAssinaturaConvenente.SetPosition((480, 550))
        self.tcCpfAssinaturaConvenente.SetValue(self.transferencia.cpfAssinaturaConvenente)

        self.stDataCompetencia = wx.StaticText(self.panelNovoTrans, -1, u'Data Competência(AAAA/MM)', pos=(700, 530), style=wx.ALIGN_LEFT)
        self.tcDataCompetencia = masked.TextCtrl(self.panelNovoTrans, -1, mask="####/##")
        self.tcDataCompetencia.SetSize((80, -1))
        self.tcDataCompetencia.SetPosition((700, 550))
        self.tcDataCompetencia.SetValue(self.transferencia.dataCompetencia)
              
        self.btnSalvar = wx.Button(self.panelNovoTrans, -1, "Alterar", pos=(250, 590),size=(-1,22))
        self.btnCancelar = wx.Button(self.panelNovoTrans, -1, "Cancelar", pos=(370, 590),size=(-1,22))

        self.windowEditaTrans.Centre()
        self.windowEditaTrans.Show()

        #Bind
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitEditarTrans)
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarTrans)
        self.windowEditaTrans.Bind(wx.EVT_CLOSE, self.quitEditarTrans)
        #Fim Bind

    def quitEditarTrans(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowEditaTrans.Destroy()

    def editarTrans(self, event):
        
        self.transferencia.cnpjConvenente=unicode(self.tcCnpjConvenente.GetValue())
        self.transferencia.numTransf=unicode(self.tcNumTransf.GetValue())
        self.transferencia.tipoTransf=unicode(self.cbTipoTransf.GetValue())
        self.transferencia.numTransfSuperior=unicode(self.tcNumTransfSuperior.GetValue())
        self.transferencia.anoTransf=unicode(self.tcAnoTransf.GetValue())
        self.transferencia.dataCelebracao=unicode(self.tcDataCelebracao.GetValue())
        self.transferencia.dataInicio=unicode(self.tcDataInicio.GetValue())
        self.transferencia.dataFim=unicode(self.tcDataFim.GetValue())
        self.transferencia.dataPublicacao=unicode(self.tcDataPublicacao.GetValue())
        self.transferencia.atividadePrincipal=unicode(self.cbAtividadePrincipal.GetValue())
        self.transferencia.objeto=unicode(self.tcObjeto.GetValue())
        self.transferencia.banco=unicode(self.tcBanco.GetValue())
        self.transferencia.agenciaBancaria=unicode(self.tcAgenciaBancaria.GetValue())
        self.transferencia.contaBancaria=unicode(self.tcContaBancaria.GetValue())
        self.transferencia.valorRepasse=unicode(self.tcValorRepasse.GetValue())
        self.transferencia.tipoContraPartida=unicode(self.cbTipoContraPartida.GetValue())
        self.transferencia.contraPartida=unicode(self.tcContraPartida.GetValue())
        self.transferencia.contraPartidaFin=unicode(self.tcContraPartidaFin.GetValue())
        self.transferencia.contraPartidaEco=unicode(self.tcContraPartidaEco.GetValue())
        self.transferencia.nomeFiscalizador=unicode(self.tcNomeFiscalizador.GetValue())
        self.transferencia.emailFiscalizador=unicode(self.tcEmailFiscalizador.GetValue())
        self.transferencia.cpfFiscalizador=unicode(self.tcCpfFiscalizador.GetValue())
        self.transferencia.cargoFiscalizador=unicode(self.tcCargoFiscalizador.GetValue())
        self.transferencia.nomeExecucao=unicode(self.tcNomeExecucao.GetValue())
        self.transferencia.emailExecucao=unicode(self.tcEmailExecucao.GetValue())
        self.transferencia.cpfExecucao=unicode(self.tcCpfExecucao.GetValue())
        self.transferencia.cargoExecucao=unicode(self.tcCargoExecucao.GetValue())
        self.transferencia.nomeAssinaturaRepassador=unicode(self.tcNomeAssinaturaRepassador.GetValue())
        self.transferencia.cpfAssinaturaRepassador=unicode(self.tcCpfAssinaturaRepassador.GetValue())
        self.transferencia.nomeAssinaturaConvenente=unicode(self.tcNomeAssinaturaConvenente.GetValue())
        self.transferencia.cpfAssinaturaConvenente=unicode(self.tcCpfAssinaturaConvenente.GetValue())
        self.transferencia.dataCompetencia=unicode(self.tcDataCompetencia.GetValue())
        self.transferencia.competencia=unicode(self.cbCompetencia.GetValue())
        

        session.commit()
        self.message = wx.MessageDialog(None, u'Transferência foi alterada com sucesso!', 'Info', wx.OK)
        self.message.ShowModal()
        self.insereTransferenciaListCtrl
        (None)
        self.contrato = None
        self.windowEditaTrans.Close()

    def excluiTrans(self, event, idContrato):

        if idContrato is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta transferencia?', u'Remover - Transferência', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.transferencia = Transferencia.query.filter_by(id=idContrato).first()
            self.transferencia.delete()
            session.commit()
            self.insereTransferenciaListCtrl(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Transferência excluído com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
        else:
            pass

    def transformaData(self, data):

        if data == "  /  /    ":
            return '00000000'
        else:
            return data[6:]+data[3:5]+data[0:2]

    def transformaAAAAMM(self, data):

        if data == "    /  ":
            return '000000'
        else:
            return data[0:4]+data[5:7]

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

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereTransPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.transGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.transGeraArquivoListCtrl.InsertColumn(0, u'CNPJ', width=130)
        self.transGeraArquivoListCtrl.InsertColumn(1, u'Num Transf', width=120)
        self.transGeraArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.transGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensTransGeraArquivos)

        self.btnIncluiContratoGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiContratoGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveContratoGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveContratoGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.transParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.transParaArquivoListCtrl.InsertColumn(0, u'CNPJ', width=130)
        self.transParaArquivoListCtrl.InsertColumn(1, u'Num Transf', width=120)
        self.transParaArquivoListCtrl.InsertColumn(2, u'', width=0)
        self.transParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensTransParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)

        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def insereTransPorCompetencia(self, event):

        transferencias = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            transferencias = Transferencia.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            transferencias = Contrato.query.all()

        self.transGeraArquivoListCtrl.DeleteAllItems()

        if not transferencias:
            self.message = wx.MessageDialog(None, u'Não existe transferencias para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(transferencias) == self.transGeraArquivoListCtrl.GetItemCount():
                pass
            else:

                for transferencia in transferencias:
                    igual = False
                    if self.transGeraArquivoListCtrl.GetItemCount() == 0:
                        index = self.transGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(transferencia.cnpjConvenente))
                        self.transGeraArquivoListCtrl.SetStringItem(index, 1, unicode(transferencia.numTransf))
                        self.transGeraArquivoListCtrl.SetStringItem(index, 2, unicode(transferencia.id))
                        igual = True

                    else:

                        for x in range(self.transGeraArquivoListCtrl.GetItemCount()):

                            if transferencia.numeroContrato == unicode(self.transGeraArquivoListCtrl.GetItem(x, 0).GetText()):
                                igual = True

                    if not igual:
                        index = self.transGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(transferencia.cnpjConvenente))
                        self.transGeraArquivoListCtrl.SetStringItem(index, 1, unicode(transferencia.numTransf))
                        self.transGeraArquivoListCtrl.SetStringItem(index, 2, unicode(transferencia.id))

        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensTransGeraArquivos(self, event):

        item = self.transGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.transGeraArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as transferências a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.transParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.transGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.transParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.transGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.transParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.transGeraArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.transGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as transferencias a serem removidas!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.contratosGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.transParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.contratosGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.transParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.contratosGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.transParaArquivoListCtrl.GetItem(item, 2).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.transParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def selecionaItensTransParaArquivo(self, event):

        item = self.transParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.transParaArquivoListCtrl.GetNextSelected(item)

    def geraArquivoDialog(self, event):

        if self.transParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione os Contratos para gerar o arquivo!!', u'Info', wx.OK)
            self.message.ShowModal()
            return 0

        dlg = wx.FileDialog(self, message="Salvar ", defaultDir="", defaultFile="TRANSFERENCIAVOLUNTARIA", wildcard="Arquivo de Remessa (*.REM)|*.REM", style=wx.SAVE)
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
                    self.message = wx.MessageDialog(None, u'Arquivo de transferências gerado com sucesso!', 'Info', wx.OK)
                    self.message.ShowModal()
                
                else:
                    self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                    self.message.ShowModal()
                
    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.transParaArquivoListCtrl.GetItemCount()):
            
            

            id = int(self.transParaArquivoListCtrl.GetItem(x, 2).GetText())
            transferencia = Transferencia.query.filter_by(id=id).first()

            f.write(unicode(self.retiraCaracteresCpfCnpj(transferencia.cnpjConvenente).zfill(14)))
            f.write(unicode(transferencia.numTransf.ljust(20).replace("'", "").replace("\"", "")))
            f.write(unicode(self.selecionaTipo(transferencia.tipoTransf)).zfill(3))
            f.write(unicode(transferencia.numTransfSuperior.ljust(20).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.anoTransf).zfill(4))
            f.write(unicode(self.transformaData(transferencia.dataCelebracao)).zfill(8))
            f.write(unicode(self.transformaData(transferencia.dataInicio)).zfill(8))
            f.write(unicode(self.transformaData(transferencia.dataFim)).zfill(8))
            f.write(unicode(self.transformaData(transferencia.dataPublicacao)).zfill(8))
            f.write(unicode(self.selecionAtividade(transferencia.atividadePrincipal)).zfill(3))
            f.write(unicode(transferencia.objeto.ljust(300).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.banco).zfill(3))
            f.write(unicode(transferencia.agenciaBancaria.ljust(7).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.contaBancaria).ljust(14).replace("'", "").replace("\"", ""))
            
            partes = transferencia.valorRepasse.split('.')
            
            if len(partes[1])> 1:
                f.write(unicode((transferencia.valorRepasse)).zfill(18).replace(".", ","))
                print unicode((transferencia.valorRepasse)).zfill(18).replace(".", ",")
            else:
                f.write(unicode((transferencia.valorRepasse+'0')).zfill(18).replace(".", ","))  
                print unicode((transferencia.valorRepasse+'0')).zfill(18).replace(".", ",")
            
            f.write(unicode(self.selecionaTipoContra(transferencia.tipoContraPartida)).zfill(1))
            f.write(unicode(transferencia.contraPartida.ljust(300).replace("'", "").replace("\"", "")))
            
            partes = transferencia.contraPartidaFin.split('.')
            
            if len(partes[1])> 1:
                f.write(unicode((transferencia.contraPartidaFin)).zfill(18).replace(".", ","))
            else:
                f.write(unicode((transferencia.contraPartidaFin+'0')).zfill(18).replace(".", ","))

            partes = transferencia.contraPartidaEco.split('.')
            
            if len(partes[1])> 1:
                f.write(unicode((transferencia.contraPartidaEco)).zfill(18).replace(".", ","))
            else:
                f.write(unicode((transferencia.contraPartidaEco+'0')).zfill(18).replace(".", ","))  

            f.write(unicode(transferencia.nomeFiscalizador.ljust(50).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.emailFiscalizador.ljust(60).replace("'", "").replace("\"", "")))
            f.write(unicode(self.retiraCaracteresCpfCnpj(transferencia.cpfFiscalizador)).zfill(11))
            f.write(unicode(transferencia.cargoFiscalizador.ljust(50).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.nomeExecucao.ljust(50).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.emailExecucao.ljust(60).replace("'", "").replace("\"", "")))
            f.write(unicode(self.retiraCaracteresCpfCnpj(transferencia.cpfExecucao)).zfill(11))
            f.write(unicode(transferencia.cargoExecucao.ljust(50).replace("'", "").replace("\"", "")))
            f.write(unicode(transferencia.nomeAssinaturaRepassador.ljust(50).replace("'", "").replace("\"", "")))
            f.write(unicode(self.retiraCaracteresCpfCnpj(transferencia.cpfAssinaturaRepassador)).zfill(11))
            f.write(unicode(transferencia.nomeAssinaturaConvenente.ljust(50).replace("'", "").replace("\"", "")))
            f.write(unicode(self.retiraCaracteresCpfCnpj(transferencia.cpfAssinaturaConvenente)).zfill(11))
            f.write(unicode(self.transformaAAAAMM(transferencia.dataCompetencia)).ljust(6).replace("'", "").replace("\"", ""))
            
            f.write(u"\n")
            #except:
            #    return 0

        f.close()
        return 1


    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def selecionaTipo(self, tipo):
        return self.choicesTipoTransf.index(unicode(tipo))+1

    def selecionAtividade(self, atividade):
        return self.choicesAtividadePrincipal.index(atividade)+1

    def selecionaTipoContra(self, tipo):
        return self.choicesTipoContrapartida.index(tipo)+1