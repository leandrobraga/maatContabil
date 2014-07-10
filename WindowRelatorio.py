#! -*- coding: utf-8 -*-


import wx
from wx.lib import masked
import datetime
from models import *
import sys
import os
import codecs

setup_all()

ID_TOOLBAR_RELATORIO_NOVO = 34001
ID_TOOLBAR_RELATORIO_EDITAR = 34002
ID_TOOLBAR_RELATORIO_EXCLUIR = 34003
ID_TOOLBAR_RELATORIO_CRIAR_ARQUIVO = 34004

class PaginaContrato(wx.Panel):
        
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']
        
        wx.StaticText(self, -1, u'Selecione o Relatório', pos=(20, 30))
        self.cbTipoRelatorio = wx.ComboBox(self, -1, pos=(20, 55), size=(200, -1), choices=['Contratos','Empenhos de Contratos'], style=wx.CB_READONLY)
        self.cbTipoRelatorio.Bind(wx.EVT_COMBOBOX, self.habilitaCopetencia)

        wx.StaticText(self, -1, u'Selecione a Competência desejada', pos=(20, 90))
        self.cbCompetencia = wx.ComboBox(self, -1, pos=(20, 115), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Disable()
        
        self.btnGerar = wx.Button(self, -1, u"Gerar Relatório", pos=(65, 155))
        self.btnGerar.Bind(wx.EVT_BUTTON, self.relatorioContrato)

    def habilitaCopetencia(self,event):
        self.cbCompetencia.Enable()   
        
    def relatorioContrato(self,event):
        
        from Relatorio import Relatorio
        
        if self.cbTipoRelatorio.GetValue() != '' and self.cbCompetencia.GetValue() != '':
            
            relatorio = Relatorio(self.cbCompetencia.GetValue())
                
            if self.cbTipoRelatorio.GetValue() == u'Contratos':
                
                relatorio.gerarRelatorioContrato()
            
            else:
                
                relatorio.gerarRelatorioEmepenhoContrato()
        
        else:

            self.message = wx.MessageDialog(None,u'Uma opção deve ser selecionada nas duas opções!', 'INFO', wx.OK)
            self.message.ShowModal()
        
class PaginaConvenio(wx.Panel):
        
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']
        
        wx.StaticText(self, -1, u'Selecione o Relatório', pos=(20, 30))
        self.cbTipoRelatorio = wx.ComboBox(self, -1, pos=(20, 55), size=(200, -1), choices=[u'Convênio', u'Participante de Convênio', u'Empenho'], style=wx.CB_READONLY)
        self.cbTipoRelatorio.Bind(wx.EVT_COMBOBOX, self.habilitaCopetencia)

        wx.StaticText(self, -1, u'Selecione a Competência desejada', pos=(20, 90))
        self.cbCompetencia = wx.ComboBox(self, -1, pos=(20, 115), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Disable()
        
        self.btnGerar = wx.Button(self, -1, u"Gerar Relatório", pos=(65, 155))
        self.btnGerar.Bind(wx.EVT_BUTTON, self.relatorioConvenio)

    def habilitaCopetencia(self,event):
        self.cbCompetencia.Enable()

    def relatorioConvenio(self,event):
        
        from Relatorio import Relatorio
        
        if self.cbTipoRelatorio.GetValue() != '' and self.cbCompetencia.GetValue() != '':
            
            relatorio = Relatorio(self.cbCompetencia.GetValue())

            if self.cbTipoRelatorio.GetValue() == u'Convênio':
                
                relatorio.gerarRelatorioConvenio()
            
            elif self.cbTipoRelatorio.GetValue() == u'Participante de Convênio':
                
                relatorio.gerarRelatorioParticipanteConvenio()

            else:
                relatorio.gerarRelatorioEmepnhoConvenio()

class PaginaLicitacao(wx.Panel):
        
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']
        
        wx.StaticText(self, -1, u'Selecione o Relatório', pos=(20, 30))
        self.cbTipoRelatorio = wx.ComboBox(self, -1, pos=(20, 55), size=(200, -1), choices=[u'Licitação', u'Item de Licitação', u'Participante de Licitação', u'Cotação', u'Certidão', u'Publicação'], style=wx.CB_READONLY)
        self.cbTipoRelatorio.Bind(wx.EVT_COMBOBOX, self.habilitaCopetencia)

        wx.StaticText(self, -1, u'Selecione a Competência desejada', pos=(20, 90))
        self.cbCompetencia = wx.ComboBox(self, -1, pos=(20, 115), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Disable()
        
        self.btnGerar = wx.Button(self, -1, u"Gerar Relatório", pos=(65, 155))
        self.btnGerar.Bind(wx.EVT_BUTTON, self.relatorioLicitacao)

    def habilitaCopetencia(self,event):
        self.cbCompetencia.Enable()

    def relatorioLicitacao(self,event):
        
        from Relatorio import Relatorio
        
        if self.cbTipoRelatorio.GetValue() != '' and self.cbCompetencia.GetValue() != '':
            
            relatorio = Relatorio(self.cbCompetencia.GetValue())
                
            if self.cbTipoRelatorio.GetValue() == u'Licitação':
                
                relatorio.gerarRelatorioLicitacao()
            
            elif self.cbTipoRelatorio.GetValue() == u'Item de Licitação':
                
                relatorio.gerarRelatorioItemLicitacao()
            
            elif self.cbTipoRelatorio.GetValue() == u'Participante de Licitação':
                
                relatorio.gerarRelatorioParticipanteLicitacao()

            elif self.cbTipoRelatorio.GetValue() == u'Cotação':
                
                relatorio.gerarRelatorioRelatorioCotacao()

            elif self.cbTipoRelatorio.GetValue() == u'Certidão':
                
                relatorio.gerarRelatorioCertidao()

            elif self.cbTipoRelatorio.GetValue() == u'Publicação':
                
                relatorio.gerarRelatorioPublicacao()

            else:

                relatorio.gerarRelatorioDotacao()
        
        else:

            self.message = wx.MessageDialog(None,u'Uma opção deve ser selecionada nas duas opções!', 'INFO', wx.OK)
            self.message.ShowModal()

class PaginaItemAta(wx.Panel):
        
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']
        
        wx.StaticText(self, -1, u'Selecione o Relatório', pos=(20, 30))
        self.cbTipoRelatorio = wx.ComboBox(self, -1, pos=(20, 55), size=(200, -1), choices=[u'Item Adesão Ata', u'Adesão Ata de Licitação'], style=wx.CB_READONLY)
        self.cbTipoRelatorio.Bind(wx.EVT_COMBOBOX, self.habilitaCopetencia)

        wx.StaticText(self, -1, u'Selecione a Competência desejada', pos=(20, 90))
        self.cbCompetencia = wx.ComboBox(self, -1, pos=(20, 115), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Disable()
        
        self.btnGerar = wx.Button(self, -1, u"Gerar Relatório", pos=(65, 155))
        self.btnGerar.Bind(wx.EVT_BUTTON, self.relatorioAta)

    def habilitaCopetencia(self,event):
        self.cbCompetencia.Enable()

    def relatorioAta(self,event):
        
        from Relatorio import Relatorio
        
        if self.cbTipoRelatorio.GetValue() != '' and self.cbCompetencia.GetValue() != '':
            
            relatorio = Relatorio(self.cbCompetencia.GetValue())
                
            if self.cbTipoRelatorio.GetValue() == u'Item Adesão Ata':
                
                relatorio.gerarRelatorioItemAta()
            else:
                relatorio.gerarRelatorioLicitacaoAta()

            
        
        else:

            self.message = wx.MessageDialog(None,u'Uma opção deve ser selecionada nas duas opções!', 'INFO', wx.OK)
            self.message.ShowModal()


class PaginaContabil(wx.Panel):
        
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.choicesCompetencias = [u'Orçamento', u'Janeiro', u'Fevereiro', u'Março', u'Abril', u'Maio', u'Junho', u'Julho', u'Agosto', u'Setembro',
                                    u'Outubro', u'Novembro', u'Dezembro']
        
        wx.StaticText(self, -1, u'Selecione o Relatório', pos=(20, 30))
        self.cbTipoRelatorio = wx.ComboBox(self, -1, pos=(20, 55), size=(200, -1), choices=[u'Plano de Contas', u'Contas', u'Movimento Contábil Inicial', u'Movimento Contábil Mensal', u'Movimento Contábil Final'], style=wx.CB_READONLY)
        self.cbTipoRelatorio.Bind(wx.EVT_COMBOBOX, self.habilitaCopetencia)

        wx.StaticText(self, -1, u'Selecione a Competência desejada', pos=(20, 90))
        self.cbCompetencia = wx.ComboBox(self, -1, pos=(20, 115), size=(200, -1), choices=self.choicesCompetencias, style=wx.CB_READONLY)
        self.cbCompetencia.Disable()
        
        self.btnGerar = wx.Button(self, -1, u"Gerar Relatório", pos=(65, 155))
        self.btnGerar.Bind(wx.EVT_BUTTON, self.relatorioLicitacao)

    def habilitaCopetencia(self,event):
        self.cbCompetencia.Enable()

    def relatorioLicitacao(self,event):
        
        from Relatorio import Relatorio
        
        if self.cbTipoRelatorio.GetValue() != '' and self.cbCompetencia.GetValue() != '':
            
            relatorio = Relatorio(self.cbCompetencia.GetValue())
                
            if self.cbTipoRelatorio.GetValue() == u'Plano de Contas':
                
                relatorio.gerarRelatorioPlanoConta()
            
            elif self.cbTipoRelatorio.GetValue() == u'Contas':
                
                relatorio.gerarRelatorioConta()
            
            elif self.cbTipoRelatorio.GetValue() == u'Movimento Contábil Inicial':
                
                relatorio.gerarRelatorioMovConIni()

            elif self.cbTipoRelatorio.GetValue() == u'Movimento Contábil Mensal':
                
                relatorio.gerarRelatorioMovConMensal()

            elif self.cbTipoRelatorio.GetValue() == u'Movimento Contábil Final':
                
                relatorio.gerarRelatorioMovConFinal()

        else:

            self.message = wx.MessageDialog(None,u'Uma opção deve ser selecionada nas duas opções!', 'INFO', wx.OK)
            self.message.ShowModal()




class WindowRelatorio(wx.MiniFrame):

    def __init__(self, parent):

        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, size=(330, 240), pos=(300, 170), title=u"Relatórios", style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.panelRelatorio = wx.Panel(self, wx.ID_ANY)
        self.noteRelatorio = wx.Notebook(self.panelRelatorio)

        paginaContrato = PaginaContrato(self.noteRelatorio)
        paginaConvenio = PaginaConvenio(self.noteRelatorio)
        paginaLicitacao = PaginaLicitacao(self.noteRelatorio)
        paginaItemAta = PaginaItemAta(self.noteRelatorio)
        paginaContabil = PaginaContabil(self.noteRelatorio)

        self.noteRelatorio.AddPage(paginaContrato, u"Contratos")
        self.noteRelatorio.AddPage(paginaConvenio, u"Convênios")
        self.noteRelatorio.AddPage(paginaItemAta, u"Ata de Adesão")
        self.noteRelatorio.AddPage(paginaLicitacao, u"Licitação")
        self.noteRelatorio.AddPage(paginaContabil, u"Contábil")

        sizer = wx.BoxSizer()
        sizer.Add(self.noteRelatorio, 1, wx.EXPAND)
        self.panelRelatorio.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.quit)

               
        self.MakeModal(True)
        self.Centre()
        self.Show()

    def quit(self,event):

        self.MakeModal(False)
        self.Destroy()


if __name__ == '__main__':
    
    app = wx.App(redirect=False)
    access = WindowRelatorio(None)
    app.MainLoop()
