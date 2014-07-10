# -*- coding: utf-8 -*-

import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs
from sqlalchemy import func

setup_all()

ID_TOOLBAR_DOTACAO_NOVO = 6001
ID_TOOLBAR_DOTACAO_EDITAR = 6002
ID_TOOLBAR_DOTACAO_EXCLUIR = 6003
ID_TOOLBAR_DOTACAO_CRIAR_ARQUIVO = 6004


class WindowDotacao(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(530, 300), pos=(300, 170), title=u"Dotação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelDotacao = wx.Panel(self, wx.ID_ANY)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)

        self.toolBar = wx.ToolBar(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_DOTACAO_NOVO, "Novo", wx.Bitmap("./imagens/add.png"), shortHelp=u'Adiciona nova dotação')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_DOTACAO_EDITAR, "Editar", wx.Bitmap("./imagens/edit.png"), shortHelp=u'Edita dotação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_DOTACAO_EXCLUIR, "Remover", wx.Bitmap("./imagens/remove.png"), shortHelp=u'Exclui dotação selecionada')
        self.toolBar.AddSeparator()
        self.toolBar.AddLabelTool(ID_TOOLBAR_DOTACAO_CRIAR_ARQUIVO, "Gerar Arquivo", wx.Bitmap("./imagens/file.png"), shortHelp=u'Gera arquivo de dotação')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()
        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro'
                                    ]

        self.cbCompetenciaForView = wx.ComboBox(self.panelDotacao, -1, pos=(1, 5), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetenciaForView.Bind(wx.EVT_COMBOBOX, self.insereInCtrList)

        #ListCtrl
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.dotacaoListCtrl = wx.ListCtrl(self.panelDotacao, wx.ID_ANY, pos=(0, 30), size=(525, 200), style=wx.LC_REPORT)
        self.dotacaoListCtrl.InsertColumn(0, u'Licitação', width=120)
        self.dotacaoListCtrl.InsertColumn(1, u'Cat. Econômica', width=100)
        self.dotacaoListCtrl.InsertColumn(2, u'Natureza', width=60)
        self.dotacaoListCtrl.InsertColumn(3, u'Fonte de Rec.', width=90)
        self.dotacaoListCtrl.InsertColumn(4, u'Função', width=60)
        self.dotacaoListCtrl.InsertColumn(5, u'Programa', width=90)
        self.dotacaoListCtrl.InsertColumn(6, u'', width=0)
        self.dotacaoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.capturaIdItemSelecionado)
        self.dotacaoListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.anulaIdItemSelecionado)
        self.idSelecionado = None

        self.hbox1.Add(self.dotacaoListCtrl, 1, wx.EXPAND)
        #Fim ListCtrl

        #Binds
        self.Bind(wx.EVT_MENU, self.novoDotacao, id=ID_TOOLBAR_DOTACAO_NOVO)
        self.Bind(wx.EVT_MENU, lambda event: self.vizualizaDotacao(event, self.idSelecionado), id=ID_TOOLBAR_DOTACAO_EDITAR)
        self.Bind(wx.EVT_MENU, lambda event: self.excluiDotacao(event, self.idSelecionado), id=ID_TOOLBAR_DOTACAO_EXCLUIR)
        self.Bind(wx.EVT_MENU, self.geraArquivoWindow, id=ID_TOOLBAR_DOTACAO_CRIAR_ARQUIVO)
        self.Bind(wx.EVT_CLOSE, self.quit)
        #Fim Binds

        self.Centre()
        self.MakeModal(True)
        self.Show()

    def quit(self, event):

        self.MakeModal(False)
        self.Destroy()

    def anulaIdItemSelecionado(self, event):

        self.idSelecionado = None

    def capturaIdItemSelecionado(self, event):

        self.idSelecionado = self.dotacaoListCtrl.GetItem(event.GetIndex(), 6).GetText()

    def toolBarControler(self, novo=True, editar=True, remover=True, gerar=True):

        self.toolBar.EnableTool(ID_TOOLBAR_DOTACAO_NOVO, novo)
        self.toolBar.EnableTool(ID_TOOLBAR_DOTACAO_EDITAR, editar)
        self.toolBar.EnableTool(ID_TOOLBAR_DOTACAO_EXCLUIR, remover)
        self.toolBar.EnableTool(ID_TOOLBAR_DOTACAO_CRIAR_ARQUIVO, gerar)

    def insereInCtrList(self, event):

        self.dotacaoListCtrl.DeleteAllItems()

        if self.cbCompetenciaForView.GetSelection() != -1:
            dotacoes = Dotacao.query.filter_by(competencia=self.cbCompetenciaForView.GetValue()).all()

            for dotacao in dotacoes:

                index = self.dotacaoListCtrl.InsertStringItem(sys.maxint, unicode(dotacao.numeroProcesso))
                self.dotacaoListCtrl.SetStringItem(index, 1, dotacao.categoriaEconomica)
                self.dotacaoListCtrl.SetStringItem(index, 2, dotacao.grupoNatureza)
                self.dotacaoListCtrl.SetStringItem(index, 3, dotacao.fonteRecurso)
                self.dotacaoListCtrl.SetStringItem(index, 4, dotacao.funcao)
                self.dotacaoListCtrl.SetStringItem(index, 5, dotacao.programa)
                self.dotacaoListCtrl.SetStringItem(index, 6, unicode(dotacao.id))

    def novoDotacao(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowNovoDotacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 350), pos=(300, 170), title=u'Novo - Dotação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelNovoDotacao = wx.Panel(self.windowNovoDotacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue('0')

        self.stCompetencia = wx.StaticText(self.panelNovoDotacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelNovoDotacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)

        wx.StaticBox(self.panelNovoDotacao, -1, pos=(5, 50), size=(480, 200))

        self.stNumeroProcesso = wx.StaticText(self.panelNovoDotacao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelNovoDotacao, -1, pos=(10, 90), size=(130, -1), style=wx.CB_READONLY)

        wx.StaticText(self.panelNovoDotacao, -1, u'Cat. Econômica', pos=(10, 130))
        self.tcCategoriaEconomica = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(10, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcCategoriaEconomica.SetMaxLength(1)
        self.tcCategoriaEconomica.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Grupo Natureza', pos=(100, 130))
        self.tcGrupoNatureza = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(100, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcGrupoNatureza.SetMaxLength(1)
        self.tcGrupoNatureza.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Modalidade Apl.', pos=(200, 130))
        self.tcModalidadeAplicacao = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(200, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcModalidadeAplicacao.SetMaxLength(2)
        self.tcModalidadeAplicacao.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Elemento', pos=(300, 130))
        self.tcElemento = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(300, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcElemento.SetMaxLength(2)
        self.tcElemento.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Unid. Orçamentária', pos=(360, 130))
        self.tcUnidadeOrcamentaria = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(360, 150), size=(60, -1), style=wx.ALIGN_LEFT)
        self.tcUnidadeOrcamentaria.SetMaxLength(6)
        self.tcUnidadeOrcamentaria.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Função', pos=(10, 190))
        self.tcFuncao = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(10, 210), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcFuncao.SetMaxLength(2)
        self.tcFuncao.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'SubFunção', pos=(100, 190))
        self.tcSubFuncao = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(100, 210), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcSubFuncao.SetMaxLength(3)
        self.tcSubFuncao.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Programa', pos=(200, 190))
        self.tcPrograma = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(200, 210), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcPrograma.SetMaxLength(4)
        self.tcPrograma.Bind(wx.EVT_CHAR, self.escapaChar)

        wx.StaticText(self.panelNovoDotacao, -1, u'Ação Gov.', pos=(270, 190))
        self.tcAcaoGoverno = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(270, 210), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcAcaoGoverno.SetMaxLength(7)
        self.tcAcaoGoverno.Bind(wx.EVT_CHAR, self.escapaChar)
        
        wx.StaticText(self.panelNovoDotacao, -1, u'Fonte de Rec.', pos=(360, 190))
        self.tcFonteRecurso = wx.TextCtrl(self.panelNovoDotacao, -1, pos=(360, 210), size=(75, -1), style=wx.ALIGN_LEFT)
        self.tcFonteRecurso.SetMaxLength(10)
        self.tcFonteRecurso.Bind(wx.EVT_CHAR, self.escapaChar)
        
        self.btnSalvar = wx.Button(self.panelNovoDotacao, -1, u'Salvar', pos=(150, 280))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.salvarDotacao)
        self.btnCancelar = wx.Button(self.panelNovoDotacao, -1, u'Cancelar', pos=(250, 280))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitNovoDotacao)

        #Binds
        self.windowNovoDotacao.Bind(wx.EVT_CLOSE, self.quitNovoDotacao)

        #
        self.windowNovoDotacao.Centre()
        self.windowNovoDotacao.Show()

    def quitNovoDotacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowNovoDotacao.Destroy()

    def insereNumeroProcesso(self, event):

        self.cbNumeroProcesso.Clear()

        licitacoes = Licitacao.query.filter_by(competencia=self.cbCompetencia.GetValue()).all()

        if not licitacoes:
            self.message = wx.MessageDialog(None, u'Não existe licitações para a competência selecionada!', 'Info', wx.OK)
            self.message.ShowModal()
            self.cbNumeroProcesso.Disable()

        else:

            for licitacao in licitacoes:

                self.cbNumeroProcesso.Append(unicode(licitacao.numeroProcessoLicitatorio))

            self.cbNumeroProcesso.Enable()

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

        if self.tcCategoriaEconomica.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Cat. Econômica deve ser preenchido', 'Info', wx.OK)
            self.tcCategoriaEconomica.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcGrupoNatureza.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Grupo Natureza deve ser preenchido', 'Info', wx.OK)
            self.tcGrupoNatureza.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcModalidadeAplicacao.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Modalidade Aplicação deve ser preenchido', 'Info', wx.OK)
            self.tcModalidadeAplicacao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcElemento.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Elemento deve ser preenchido', 'Info', wx.OK)
            self.tcElemento.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcUnidadeOrcamentaria.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Unidade Orçamentária deve ser preenchido', 'Info', wx.OK)
            self.tcUnidadeOrcamentaria.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcFonteRecurso.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Fonte de Recurso deve ser preenchido', 'Info', wx.OK)
            self.tcFonteRecurso.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcAcaoGoverno.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Ação Governo deve ser preenchido', 'Info', wx.OK)
            self.tcAcaoGoverno.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcSubFuncao.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Subfunção deve ser preenchido', 'Info', wx.OK)
            self.tcSubFuncao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcFuncao.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Função deve ser preenchido', 'Info', wx.OK)
            self.tcFuncao.SetFocus()
            self.message.ShowModal()
            return 0

        if self.tcPrograma.GetValue() == '':

            self.message = wx.MessageDialog(None, u'O campo Programa deve ser preenchido', 'Info', wx.OK)
            self.tcPrograma.SetFocus()
            self.message.ShowModal()
            return 0

        return 1

    def salvarDotacao(self, event):

        if self.valida():
            
            Dotacao(numeroProcesso=unicode(self.cbNumeroProcesso.GetValue()),
                    categoriaEconomica=unicode(self.tcCategoriaEconomica.GetValue()),
                    grupoNatureza=unicode(self.tcGrupoNatureza.GetValue()),
                    modalidadeAplicacao=unicode(self.tcModalidadeAplicacao.GetValue()),
                    elemento=unicode(self.tcElemento.GetValue()),
                    unidadeOrcamentaria=unicode(self.tcUnidadeOrcamentaria.GetValue()),
                    fonteRecurso=unicode(self.tcFonteRecurso.GetValue()),
                    acaoGoverno=unicode(self.tcAcaoGoverno.GetValue()),
                    subFuncao=unicode(self.tcSubFuncao.GetValue()),
                    funcao=unicode(self.tcFuncao.GetValue()),
                    programa=unicode(self.tcPrograma.GetValue()),
                    competencia=unicode(self.cbCompetencia.GetValue()),
            )

            session.commit()
            self.message = wx.MessageDialog(None, u'Dotação salva com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitNovoDotacao(None)

    def escapaChar(self, event):

        if event.GetKeyCode() < 256:

            if chr(event.GetKeyCode()).isdigit() or event.GetKeyCode() == 8 or event.GetKeyCode() == 127:
                event.Skip()
        else:
            event.Skip()

    def vizualizaDotacao(self, event, idDotacao):

        if idDotacao is None:
            self.message = wx.MessageDialog(None, u'Nenhuma Dotação foi selecionada! Selecione uma na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        self.dotacao = Dotacao.query.filter_by(id=idDotacao).first()

        self.toolBarControler(False, False, False, False)

        self.windowVizualizaDotacao = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(500, 350), pos=(300, 170), title=u'Novo - Dotação', style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelVizualizaDotacao = wx.Panel(self.windowVizualizaDotacao, wx.ID_ANY)

        self.tcId = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(0, 0), size=(0, 0))
        self.tcId.SetValue(unicode(self.dotacao.id))

        self.stCompetencia = wx.StaticText(self.panelVizualizaDotacao, -1, u'Competência', pos=(10, 5))
        self.cbCompetencia = wx.ComboBox(self.panelVizualizaDotacao, -1, pos=(10, 25), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Bind(wx.EVT_COMBOBOX, self.insereNumeroProcesso)
        self.cbCompetencia.SetValue(self.dotacao.competencia)

        wx.StaticBox(self.panelVizualizaDotacao, -1, pos=(5, 50), size=(480, 200))

        self.stNumeroProcesso = wx.StaticText(self.panelVizualizaDotacao, -1, u'Número Proc. Licitatório', pos=(10, 70))
        self.cbNumeroProcesso = wx.ComboBox(self.panelVizualizaDotacao, -1, pos=(10, 90), size=(130, -1), style=wx.CB_READONLY)
        self.insereNumeroProcesso(None)
        self.cbNumeroProcesso.SetValue(self.dotacao.numeroProcesso)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Cat. Econômica', pos=(10, 130))
        self.tcCategoriaEconomica = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(10, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcCategoriaEconomica.SetMaxLength(1)
        self.tcCategoriaEconomica.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcCategoriaEconomica.SetValue(self.dotacao.categoriaEconomica)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Grupo Natureza', pos=(100, 130))
        self.tcGrupoNatureza = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(100, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcGrupoNatureza.SetMaxLength(1)
        self.tcGrupoNatureza.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcGrupoNatureza.SetValue(self.dotacao.grupoNatureza)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Modalidade Apl.', pos=(200, 130))
        self.tcModalidadeAplicacao = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(200, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcModalidadeAplicacao.SetMaxLength(2)
        self.tcModalidadeAplicacao.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcModalidadeAplicacao.SetValue(self.dotacao.modalidadeAplicacao)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Elemento', pos=(300, 130))
        self.tcElemento = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(300, 150), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcElemento.SetMaxLength(2)
        self.tcElemento.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcElemento.SetValue(self.dotacao.elemento)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Unid. Orçamentária', pos=(360, 130))
        self.tcUnidadeOrcamentaria = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(360, 150), size=(60, -1), style=wx.ALIGN_LEFT)
        self.tcUnidadeOrcamentaria.SetMaxLength(6)
        self.tcUnidadeOrcamentaria.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcUnidadeOrcamentaria.SetValue(self.dotacao.unidadeOrcamentaria)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Função', pos=(10, 190))
        self.tcFuncao = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(10, 210), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcFuncao.SetMaxLength(2)
        self.tcFuncao.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcFuncao.SetValue(self.dotacao.funcao)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'SubFunção', pos=(100, 190))
        self.tcSubFuncao = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(100, 210), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcSubFuncao.SetMaxLength(3)
        self.tcSubFuncao.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcSubFuncao.SetValue(self.dotacao.subFuncao)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Programa', pos=(200, 190))
        self.tcPrograma = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(200, 210), size=(40, -1), style=wx.ALIGN_LEFT)
        self.tcPrograma.SetMaxLength(4)
        self.tcPrograma.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcPrograma.SetValue(self.dotacao.programa)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Ação Gov.', pos=(270, 190))
        self.tcAcaoGoverno = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(270, 210), size=(70, -1), style=wx.ALIGN_LEFT)
        self.tcAcaoGoverno.SetMaxLength(7)
        self.tcAcaoGoverno.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcAcaoGoverno.SetValue(self.dotacao.acaoGoverno)

        wx.StaticText(self.panelVizualizaDotacao, -1, u'Fonte de Rec.', pos=(360, 190))
        self.tcFonteRecurso = wx.TextCtrl(self.panelVizualizaDotacao, -1, pos=(360, 210), size=(75, -1), style=wx.ALIGN_LEFT)
        self.tcFonteRecurso.SetMaxLength(10)
        self.tcFonteRecurso.Bind(wx.EVT_CHAR, self.escapaChar)
        self.tcFonteRecurso.SetValue(self.dotacao.fonteRecurso)
                
        self.btnSalvar = wx.Button(self.panelVizualizaDotacao, -1, u'Alterar', pos=(150, 280))
        self.btnSalvar.Bind(wx.EVT_BUTTON, self.editarDotacao)
        self.btnCancelar = wx.Button(self.panelVizualizaDotacao, -1, u'Cancelar', pos=(250, 280))
        self.btnCancelar.Bind(wx.EVT_BUTTON, self.quitVizualizaDotacao)

        #Binds
        self.windowVizualizaDotacao.Bind(wx.EVT_CLOSE, self.quitNovoDotacao)

        #
        self.windowVizualizaDotacao.Centre()
        self.windowVizualizaDotacao.Show()

    def quitVizualizaDotacao(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowVizualizaDotacao.Destroy()

    def editarDotacao(self, event):

        if self.valida():

            self.dotacao.numeroProcesso=unicode(self.cbNumeroProcesso.GetValue())
            self.dotacao.categoriaEconomica=unicode(self.tcCategoriaEconomica.GetValue())
            self.dotacao.grupoNatureza=unicode(self.tcGrupoNatureza.GetValue())
            self.dotacao.modalidadeAplicacao=unicode(self.tcModalidadeAplicacao.GetValue())
            self.dotacao.elemento=unicode(self.tcElemento.GetValue())
            self.dotacao.unidadeOrcamentaria=unicode(self.tcUnidadeOrcamentaria.GetValue())
            self.dotacao.fonteRecurso=unicode(self.tcFonteRecurso.GetValue())
            self.dotacao.acaoGoverno=unicode(self.tcAcaoGoverno.GetValue())
            self.dotacao.subFuncao=unicode(self.tcSubFuncao.GetValue())
            self.dotacao.funcao=unicode(self.tcFuncao.GetValue())
            self.dotacao.programa=unicode(self.tcPrograma.GetValue())
            self.dotacao.competencia=unicode(self.cbCompetencia.GetValue())
            

            session.commit()
            self.message = wx.MessageDialog(None, u'Dotação alterada com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
            self.insereInCtrList(None)
            self.quitVizualizaDotacao(None)

    def excluiDotacao(self, none, idDotacao):

        if idDotacao is None:
            self.message = wx.MessageDialog(None, u'Selecione um item na lista!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir esta dotação?', 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            self.dotacao = Dotacao.query.filter_by(id=idDotacao).first()
            self.dotacao.delete()
            session.commit()
            self.insereInCtrList(None)
            self.anulaIdItemSelecionado(None)
            self.message = wx.MessageDialog(None, u'Dotação excluída com sucesso!', 'Info', wx.OK)
            self.message.ShowModal()
        else:
            pass



    def geraArquivoWindow(self, event):

        self.toolBarControler(False, False, False, False)

        self.windowGeraArquivo = wx.MiniFrame(parent=self, id=wx.ID_ANY, size=(680, 470), pos=(300, 170), title=u"Gerar Arquivo de Dotação", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelGeraArquivo = wx.Panel(self.windowGeraArquivo, wx.ID_ANY)

        wx.StaticBox(self.panelGeraArquivo, -1, pos=(0, 0), size=(660, 60))

        choicesCompetencias = self.choicesCompetencias
        choicesCompetencias.append(u'Todos')
        self.stGeraArquivoCompetencia = wx.StaticText(self.panelGeraArquivo, -1, u'Competência', pos=(10, 10), style=wx.ALIGN_LEFT)
        self.cbGeraArquivoCompetencia = wx.ComboBox(self.panelGeraArquivo, -1, pos=(10, 30), size=(250, -1), choices=choicesCompetencias, style=wx.CB_READONLY)
        self.cbGeraArquivoCompetencia.Bind(wx.EVT_COMBOBOX, self.insereDotacaoPorCompetencia)

        self.competenciaAtual = None
        self.itensGeraArquivoListCtrl = []
        self.itensParaArquivosListCtrl = []

        wx.StaticText(self.panelGeraArquivo, -1, u'Inserir:', pos=(10, 70))
        self.dotacaoGeraArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(10, 90), size=(250, 300), style=wx.LC_REPORT)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(0, u'Licitação', width=120)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(1, u'Cat. Eco.', width=60)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(2, u'Natureza', width=90)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(3, u'Fonte de Rec.', width=90)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(4, u'Função', width=60)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(5, u'Programa', width=90)
        self.dotacaoGeraArquivoListCtrl.InsertColumn(6, u'', width=0)
        self.dotacaoGeraArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParticipantesGeraArquivos)

        self.btnIncluiGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u">>", pos=(290, 200))
        self.btnIncluiGeraArquivo.Bind(wx.EVT_BUTTON, self.insereGeraArquivo)
        self.btnRemoveGeraArquivo = wx.Button(self.panelGeraArquivo, -1, u"<<", pos=(290, 250))
        self.btnRemoveGeraArquivo.Bind(wx.EVT_BUTTON, self.removeGeraArquivo)

        wx.StaticText(self.panelGeraArquivo, -1, u'Gerar Arquivo Com:', pos=(400, 70))
        self.dotacaoParaArquivoListCtrl = wx.ListCtrl(self.panelGeraArquivo, wx.ID_ANY, pos=(400, 90), size=(250, 300), style=wx.LC_REPORT)
        self.dotacaoParaArquivoListCtrl.InsertColumn(0, u'Nome do Participante', width=130)
        self.dotacaoParaArquivoListCtrl.InsertColumn(1, u'Cat. Eco.', width=60)
        self.dotacaoParaArquivoListCtrl.InsertColumn(2, u'Natureza', width=90)
        self.dotacaoParaArquivoListCtrl.InsertColumn(3, u'Fonte de Rec.', width=90)
        self.dotacaoParaArquivoListCtrl.InsertColumn(4, u'Função', width=60)
        self.dotacaoParaArquivoListCtrl.InsertColumn(5, u'Programa', width=90)
        self.dotacaoParaArquivoListCtrl.InsertColumn(6, u'', width=0)
        self.dotacaoParaArquivoListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionaItensParticipantesParaArquivo)

        self.btnGerarArquivo = wx.Button(self.panelGeraArquivo, -1, "Gerar Arquivo", pos=(300, 400))
        self.btnGerarArquivo.Bind(wx.EVT_BUTTON, self.geraArquivoDialog)

        self.windowGeraArquivo.Bind(wx.EVT_CLOSE, self.quitGeraArquivo)

        self.windowGeraArquivo.Centre()
        self.windowGeraArquivo.Show()

    def quitGeraArquivo(self, event):

        self.toolBarControler(True, True, True, True)
        self.windowGeraArquivo.Destroy()

    def insereDotacaoPorCompetencia(self, event):

        dotacoes = []
        if self.competenciaAtual == unicode(self.cbGeraArquivoCompetencia.GetValue()):
            return 0

        elif self.cbGeraArquivoCompetencia.GetValue() != u'Todos':

            dotacoes = Dotacao.query.filter_by(competencia=self.cbGeraArquivoCompetencia.GetValue()).all()
        else:

            dotacoes = Dotacao.query.all()

        self.dotacaoGeraArquivoListCtrl.DeleteAllItems()

        if not dotacoes:
            self.message = wx.MessageDialog(None, u'Não existe dotação para esta competência!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            if len(dotacoes) == self.dotacaoParaArquivoListCtrl.GetItemCount():
                pass
            else:

                for dotacao in dotacoes:
                    igual = False

                    if self.dotacaoParaArquivoListCtrl.GetItemCount() == 0:
                        index = self.dotacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(dotacao.numeroProcesso))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(dotacao.categoriaEconomica))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(dotacao.grupoNatureza))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(dotacao.fonteRecurso))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(dotacao.funcao))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 5, unicode(dotacao.programa))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 6, unicode(dotacao.id))

                        igual = True
                    else:

                        for x in range(self.dotacaoParaArquivoListCtrl.GetItemCount()):

                            if dotacao.numeroProcesso == unicode(self.dotacaoParaArquivoListCtrl.GetItem(x, 0).GetText()) and dotacao.categoriaEconomica == unicode(self.dotacaoParaArquivoListCtrl.GetItem(x, 1).GetText()) and dotacao.grupoNatureza == unicode(self.dotacaoParaArquivoListCtrl.GetItem(x, 2).GetText()) and dotacao.fonteRecurso == unicode(self.dotacaoParaArquivoListCtrl.GetItem(x, 3).GetText()) and dotacao.funcao == unicode(self.dotacaoParaArquivoListCtrl.GetItem(x, 4).GetText()) and dotacao.programa == unicode(self.dotacaoParaArquivoListCtrl.GetItem(x, 5).GetText()):
                                igual = True

                    if not igual:
                        index = self.dotacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(dotacao.numeroProcesso))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(dotacao.categoriaEconomica))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(dotacao.grupoNatureza))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(dotacao.fonteRecurso))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(dotacao.funcao))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 5, unicode(dotacao.programa))
                        self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 6, unicode(dotacao.id))


        self.competenciaAtual = unicode(self.cbGeraArquivoCompetencia.GetValue())

    def selecionaItensParticipantesGeraArquivos(self, event):

        item = self.dotacaoGeraArquivoListCtrl.GetFirstSelected()
        self.itensGeraArquivoListCtrl = []
        while item != -1:
            self.itensGeraArquivoListCtrl.append(item)
            item = self.dotacaoGeraArquivoListCtrl.GetNextSelected(item)

    def selecionaItensParticipantesParaArquivo(self, event):

        item = self.dotacaoParaArquivoListCtrl.GetFirstSelected()
        self.itensParaArquivosListCtrl = []
        while item != -1:
            self.itensParaArquivosListCtrl.append(item)
            item = self.dotacaoParaArquivoListCtrl.GetNextSelected(item)

    def insereGeraArquivo(self, event):

        if not self.itensGeraArquivoListCtrl:

            self.message = wx.MessageDialog(None, u'Selecione as Dotações a serem inseridos!', 'Info', wx.OK)
            self.message.ShowModal()

        else:

            for item in self.itensGeraArquivoListCtrl:

                index = self.dotacaoParaArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 0).GetText()))
                self.dotacaoParaArquivoListCtrl.SetStringItem(index, 1, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 1).GetText()))
                self.dotacaoParaArquivoListCtrl.SetStringItem(index, 2, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 2).GetText()))
                self.dotacaoParaArquivoListCtrl.SetStringItem(index, 3, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 3).GetText()))
                self.dotacaoParaArquivoListCtrl.SetStringItem(index, 4, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 4).GetText()))
                self.dotacaoParaArquivoListCtrl.SetStringItem(index, 5, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 5).GetText()))
                self.dotacaoParaArquivoListCtrl.SetStringItem(index, 6, unicode(self.dotacaoGeraArquivoListCtrl.GetItem(item, 6).GetText()))

            for item in reversed(self.itensGeraArquivoListCtrl):
                self.dotacaoGeraArquivoListCtrl.DeleteItem(item)

        self.itensGeraArquivoListCtrl = []

    def removeGeraArquivo(self, event):

        if not self.itensParaArquivosListCtrl:
            self.message = wx.MessageDialog(None, u'Selecione as Dotações a serem removidos!', 'Info', wx.OK)
            self.message.ShowModal()
        else:

            for item in self.itensParaArquivosListCtrl:

                index = self.dotacaoGeraArquivoListCtrl.InsertStringItem(sys.maxint, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 0).GetText()))
                self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 1, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 1).GetText()))
                self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 2, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 2).GetText()))
                self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 3, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 3).GetText()))
                self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 4, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 4).GetText()))
                self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 5, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 5).GetText()))
                self.dotacaoGeraArquivoListCtrl.SetStringItem(index, 6, unicode(self.dotacaoParaArquivoListCtrl.GetItem(item, 6).GetText()))

            for item in reversed(self.itensParaArquivosListCtrl):
                self.dotacaoParaArquivoListCtrl.DeleteItem(item)

        self.itensParaArquivosListCtrl = []

    def geraArquivoDialog(self, event):

        if self.dotacaoParaArquivoListCtrl.GetItemCount() == 0:

            self.message = wx.MessageDialog(None, u'Selecione as Dotações para gerar o arquivo!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        else:

            
            dlg = wx.FileDialog(self, message=u'Salvar ', defaultDir="", defaultFile='LICITACAODOTACAO.REM', wildcard='Arquivo de Remessa (*.REM)|*.REM', style=wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:

                self.path = dlg.GetPath()
                if os.path.exists(self.path):

                    remove_dial = wx.MessageDialog(None, u'Já existe um arquivo '+dlg.GetFilename()+u".\n Deseja substituí-lo?", 'Sair', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                    ret = remove_dial.ShowModal()
                    if ret == wx.ID_YES:

                        if self.geraArquivo():
                            self.message = wx.MessageDialog(None, u'Arquivo de Dotações gerados com sucesso!', 'Info', wx.OK)
                            self.message.ShowModal()
                            
                        else:
                            self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                            self.message.ShowModal()
                            
                    else:
                        pass

                else:
                    if self.geraArquivo():
                        self.message = wx.MessageDialog(None, u'Arquivo de Dotações gerados com sucesso!', 'Info', wx.OK)
                        self.message.ShowModal()
                        
                    else:
                        self.message = wx.MessageDialog(None, u'Houve um erro na geração do arquivo!\nVerifique se você tem permissão de escrita ou se o arquivo já se encontra aberto!', 'Error', wx.OK)
                        self.message.ShowModal()
                        

    def geraArquivo(self):

        f = codecs.open(self.path, "w", "utf-8")

        for x in range(self.dotacaoParaArquivoListCtrl.GetItemCount()):

            
            try:
                
                idDotacao = int(self.dotacaoParaArquivoListCtrl.GetItem(x, 6).GetText())
                dotacao = Dotacao.query.filter_by(id=idDotacao).first()

                
                f.write(unicode(dotacao.numeroProcesso.ljust(16).replace("'", "").replace("\"", "")))
                f.write(unicode(dotacao.categoriaEconomica.zfill(1)))
                f.write(unicode(dotacao.grupoNatureza.zfill(1)))
                f.write(unicode(dotacao.modalidadeAplicacao.zfill(2)))
                f.write(unicode(dotacao.elemento.zfill(2)))
                f.write(unicode(dotacao.unidadeOrcamentaria.zfill(6)))
                f.write(unicode(dotacao.fonteRecurso.zfill(10)))
                f.write(unicode(dotacao.acaoGoverno.zfill(7)))
                f.write(unicode(dotacao.subFuncao.zfill(3)))
                f.write(unicode(dotacao.funcao.zfill(2)))
                f.write(unicode(dotacao.programa.zfill(4)))
                f.write(u'\n')


            except:
                return 0

        f.close()

        return 1



