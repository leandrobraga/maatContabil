#! -*- coding: utf-8 -*-

from models import *
from geraldo.generators import PDFGenerator
from geraldo.base import EmptyQueryset
import os
import wx

setup_all()


class Relatorio:

    def __init__(self, competencia):

        self.competencia = competencia
    
    def gerarRelatorioContrato(self):
        
        from RelatorioContrato import RelatorioContrato

        contratos = Contrato.query.filter_by(competencia=self.competencia)
        relatorio = RelatorioContrato(queryset=contratos)
        relatorio.generate_by(PDFGenerator, filename='contratos.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Contratos gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("contratos.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None,'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()
            

    def gerarRelatorioEmepenhoContrato(self):

        from RelatorioEmpenhoContrato import RelatorioEmpenhoContrato

        empenhos = ContratoEmpenho.query.filter_by(competencia=self.competencia)
        relatorio = RelatorioEmpenhoContrato(queryset=empenhos)
        relatorio.generate_by(PDFGenerator, filename='empenhoContrato.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Empenhos de Contratos gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("empenhoContrato.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None,'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioLicitacao(self):

        from RelatorioLicitacao import RelatorioLicitacao

        licitacaoes = Licitacao.query.filter_by(competencia=self.competencia)
        relatorio = RelatorioLicitacao(queryset=licitacaoes)
        relatorio.generate_by(PDFGenerator, filename='licitacao.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Licitações gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("licitacao.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None,'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()  

    def gerarRelatorioItemLicitacao(self):

        from RelatorioItemLicitacao import RelatorioItemLicitacao

        itens = ItemLicitacao.query.filter_by(competencia=self.competencia).order_by(ItemLicitacao.numeroProcessoLicitatorio).order_by(ItemLicitacao.sequenciaItem)
        relatorio = RelatorioItemLicitacao(queryset=itens)
        relatorio.generate_by(PDFGenerator, filename='itemLicitacao.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Itens de Licitação gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("itemLicitacao.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()


    def gerarRelatorioParticipanteLicitacao(self):  

        
        from RelatorioParticipanteLicitacao import RelatorioParticipanteLicitacao

        participantes = ParticipanteLicitacao.query.filter_by(competencia=self.competencia).order_by(ParticipanteLicitacao.numeroProcessoLicitatorio)
        relatorio = RelatorioParticipanteLicitacao(queryset=participantes)
        relatorio.generate_by(PDFGenerator, filename='participantesLicitacao.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Participantes de Licitação gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("participantesLicitacao.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioRelatorioCotacao(self):

        from RelatorioCotacao import RelatorioCotacao

        cotacoes = Cotacao.query.filter_by(competencia=self.competencia).order_by(Cotacao.numeroProcessoLicitatorio).order_by(Cotacao.sequenciaItem)
        relatorio = RelatorioCotacao(queryset=cotacoes)
        relatorio.generate_by(PDFGenerator, filename='cotacoes.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Cotações gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("cotacoes.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioCertidao(self):

        from RelatorioCertidao import RelatorioCertidao

        certidoes = Certidao.query.filter_by(competencia=self.competencia).order_by(Certidao.numeroProcesso)
        relatorio = RelatorioCertidao(queryset=certidoes)
        relatorio.generate_by(PDFGenerator, filename='certidoes.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Certidões gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("certidoes.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()


    def gerarRelatorioPublicacao(self):

        from RelatorioPublicacao import RelatorioPublicacao

        publicacoes = Publicacao.query.filter_by(competencia=self.competencia).order_by(Publicacao.numeroProcesso).order_by(Publicacao.dataPublicacao)
        relatorio = RelatorioPublicacao(queryset=publicacoes)
        relatorio.generate_by(PDFGenerator, filename='publicacoes.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Publicações gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("publicacoes.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioDotacao(self):

        from RelatorioDotacao import RelatorioDotacao

        dotacoes = Dotacao.query.filter_by(competencia=self.competencia).order_by(Dotacao.numeroProcesso)
        relatorio = RelatorioDotacao(queryset=dotacoes)
        relatorio.generate_by(PDFGenerator, filename='dotacoes.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Dotações gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("dotacoes.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioConvenio(self):

        from RelatorioConvenio import RelatorioConvenio

        convenios = Convenio.query.filter_by(competencia=self.competencia).order_by(Convenio.numeroConvenio)
        relatorio = RelatorioConvenio(queryset=convenios)
        relatorio.generate_by(PDFGenerator, filename='convenios.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Convênios gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("convenios.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioParticipanteConvenio(self):

        from RelatorioParticipanteConvenio import RelatorioParticipanteConvenio

        participantes = ParticipanteConvenio.query.filter_by(competencia=self.competencia).order_by(ParticipanteConvenio.numeroConvenio)
        relatorio = RelatorioParticipanteConvenio(queryset=participantes)
        relatorio.generate_by(PDFGenerator, filename='participantesConvenios.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Participantes de Convênios gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("participantesConvenios.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()


    def gerarRelatorioEmepnhoConvenio(self):

        from RelatorioEmpenhoConvenio import RelatorioEmpenhoConvenio

        empenhos = ConvenioEmpenho.query.filter_by(competencia=self.competencia).order_by(ConvenioEmpenho.numeroConvenio)
        relatorio = RelatorioEmpenhoConvenio(queryset=empenhos)
        relatorio.generate_by(PDFGenerator, filename='empenhoConvenio.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Empenhos de Convênios gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("empenhoConvenio.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()



    def gerarRelatorioItemAta(self):

        from RelatorioItemAta import RelatorioItemAta

        itens = ItemAta.query.filter_by(competencia=self.competencia).order_by(ItemAta.processoCompra)
        relatorio = RelatorioItemAta(queryset=itens)
        relatorio.generate_by(PDFGenerator, filename='itensAta.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Itens Adesão Ata gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("itensAta.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioLicitacaoAta(self):

        from RelatorioLicitacaoAta import RelatorioLicitacaoAta

        licitacoes = LicitacaoAta.query.filter_by(competencia=self.competencia).order_by(LicitacaoAta.processoCompra)
        relatorio = RelatorioLicitacaoAta(queryset=licitacoes)
        relatorio.generate_by(PDFGenerator, filename='licitacoesAta.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Adesão Ata de Licitação gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("licitacoesAta.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()


    def gerarRelatorioPlanoConta(self):

        from RelatorioPlanosConta import RelatorioPlanosConta

        planoContas = PlanoConta.query.all()
        
        relatorio = RelatorioPlanosConta(queryset=planoContas)
        relatorio.generate_by(PDFGenerator, filename='planoConta.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Plano de Contas gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("planoConta.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()


    def gerarRelatorioConta(self):

        from RelatorioConta import RelatorioConta

        contas = Conta.query.filter_by(competencia=self.competencia).order_by(Conta.codigoConta)
        
        relatorio = RelatorioConta(queryset=contas)
        relatorio.generate_by(PDFGenerator, filename='contas.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Contas gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("contas.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioMovConIni(self):

        from RelatorioMovConIni import RelatorioMovConIni

        movConInis = MovConIni.query.filter_by(competencia=self.competencia).order_by(MovConIni.codigoConta)
        
        relatorio = RelatorioMovConIni(queryset=movConInis)
        relatorio.generate_by(PDFGenerator, filename='movconini.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Movimento Contábil Inicial gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("movconini.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()


    def gerarRelatorioMovConMensal(self):

        from RelatorioMovConMensal import RelatorioMovConMensal

        movConMensal = MovConMensal.query.filter_by(competencia=self.competencia).order_by(MovConMensal.codigoConta)
        
        relatorio = RelatorioMovConMensal(queryset=movConMensal)
        relatorio.generate_by(PDFGenerator, filename='movconmensal.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Movimento Contábil Mensal gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("movconmensal.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()

    def gerarRelatorioMovConFinal(self):

        from RelatorioMovConFinal import RelatorioMovConFinal

        movConMensal = MovConFinal.query.filter_by(competencia=self.competencia).order_by(MovConFinal.codigoConta)
        
        relatorio = RelatorioMovConFinal(queryset=movConMensal)
        relatorio.generate_by(PDFGenerator, filename='movconfinal.pdf', variables={'competencia': self.competencia})
        self.message = wx.MessageDialog(None, u'Relatório de Movimento Contábil Final gerado com sucesso!', 'OK', wx.OK)
        self.message.ShowModal()
        
        try:
        
            os.startfile("movconfinal.pdf")
        
        except :
            
            self.message = wx.MessageDialog(None, u'\n Favor instale um programa capaz de abrir arquivos pdf!', 'Error', wx.OK)
            self.message.ShowModal()
