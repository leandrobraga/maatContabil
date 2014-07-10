# -*- coding: utf-8 -*-


import wx
from datetime import date
import shutil

ID_CONTRATO = 1001
ID_EMPENHO_CONTRATO = 1002
ID_CONVENIO = 1003
ID_PARTICIPANTES_CONVENIOS = 1004
ID_EMPENHO_CONVENIO = 1005
ID_LICITACAO = 1006
ID_ITEM_LICITACAO = 1007
ID_COTACAO = 1008
ID_CERTIDAO = 1009
ID_PARTICIPANTE_LICITACAO = 1010
ID_PUBLICACAO = 1011
ID_DOTACAO = 1012
ID_USUARIO = 1013
ID_BACKUP = 1014
ID_RESTORE = 1015
ID_RELATORIOS = 1016
ID_GERAR_RELATORIOS = 1017
ID_ITEMADESAOATA = 1018
ID_ADESAOATALICITACAO = 1019
ID_PLANO_DE_CONTAS = 1020
ID_CONTAS = 1021
ID_MOVCOMINICIAL = 1022
ID_MOVCOMMENSAL = 1023
ID_MOVCOMFINAL = 1024


class WindowNormal(wx.Frame):

    def __init__(self, user):
        wx.Frame.__init__(self, None, -1, u'Maat - Sistema de Geração de Arquivos de Atos Jurídicos', size=(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU)

        self.panelManagerWindow = wx.Panel(self, 1)
        self.panelManagerWindow.SetBackgroundColour('#BEBEBE')

        self.ico = wx.Icon("./imagens/pena.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        #Menu

        menuBar = wx.MenuBar()

        atoJuridicoMenu = wx.Menu()
        
        contratosMenu = wx.Menu()
        contratosSubMenu = contratosMenu.Append(ID_CONTRATO, u'Contratos', u'Informe de Contratos')
        empenhosContratosSubMenu = contratosMenu.Append(ID_EMPENHO_CONTRATO, u'Informações de Empenho', u'Informe os empenhos dos contratos')
        atoJuridicoMenu.AppendMenu(-1, u'Contratos', contratosMenu)

        conveniosMenu = wx.Menu()
        convenioSubMenu = conveniosMenu.Append(ID_CONVENIO, u'Convênios', u'Informe de Convênios')
        participantesConvenioSubMenu = conveniosMenu.Append(ID_PARTICIPANTES_CONVENIOS, u'Participante de Convênios', u'Informe de Participantes de Convênios')
        empenhosConvenioSubmenu = conveniosMenu.Append(ID_EMPENHO_CONVENIO, u'Informações de Empenho', u'Informe os empenhos dos convênios')

        atoJuridicoMenu.AppendMenu(-1, u'Convênios', conveniosMenu)

        licitacoesMenu = wx.Menu()
        licitacoesMenuItem1 = licitacoesMenu.Append(ID_LICITACAO, u'Licitação', u'Informe de Licitações')
        licitacoesMenuItem2 = licitacoesMenu.Append(ID_ITEM_LICITACAO, u'Item de Licitação', u'Informe de Item de Licitação')
        licitacoesMenuItem3 = licitacoesMenu.Append(ID_PARTICIPANTE_LICITACAO, u'Participante de Licitação', u'Informe de Participante de Licitação')
        licitacoesMenuItem4 = licitacoesMenu.Append(ID_COTACAO, u'Cotação', u'Informe de Cotação')
        licitacoesMenuItem5 = licitacoesMenu.Append(ID_CERTIDAO, u'Certidão', u'Informe de Certidão')
        licitacoesMenuItem6 = licitacoesMenu.Append(ID_PUBLICACAO, u'Publicação', u'Informe de Publicação de licitação')
        
        atasMenu = wx.Menu()
        atasMenuItem1 = atasMenu.Append(ID_ITEMADESAOATA, u'Item Adesão Ata', 'Informe os itens de adesão a ata')
        atasMenuItem2 = atasMenu.Append(ID_ADESAOATALICITACAO, u'Adesão Ata de Licitação', u'Ifnorme adesão a ata de licitação')
        
        contabilMenu = wx.Menu()
        planoDeContasSubMenu = contabilMenu.Append(ID_PLANO_DE_CONTAS, u'Plano de Contas', u'Informe os planos de contas')
        contasSubMenu = contabilMenu.Append(ID_CONTAS, u'Contas', u'Informe as contas')
        movConMenu = wx.Menu()
        movConInicialSubMenu = movConMenu.Append(ID_MOVCOMINICIAL, u'Inicial', u'Informe Movimentação Contábil Incial')
        movConMensalSubMenu = movConMenu.Append(ID_MOVCOMMENSAL, u'Mensal', u'Informe Movimentação Contábil Mensal')
        movConFinalSubMenu = movConMenu.Append(ID_MOVCOMFINAL, u'Final', u'Informe Movimentação Contábil Final')
        
        
        contabilMenu.AppendMenu(-1, u'Movimentação Contábil', movConMenu)

        relatoriosMenu = wx.Menu()
        relatoriosMenuItem1 = relatoriosMenu.Append(ID_GERAR_RELATORIOS, u'Gerar Relatórios')

        #usuariosMenu = wx.Menu()
        #usuarioMenuItem1 = usuariosMenu.Append(ID_USUARIO, u'Cadastro de Usuário', u'Gerencia os usuários do sistema')

        #backupMenu = wx.Menu()
        #backupMenuItem1 = backupMenu.Append(ID_BACKUP, u'Backup', 'Realiza procedimetno de backup do banco de dados!')
        #backupMenuItem2 = backupMenu.Append(ID_RESTORE, u'Restaurar Backup', 'Realiza procedimetno de restauração de backup do banco de dados!')

        menuBar.Append(atoJuridicoMenu, u'Atos Jurídicos')
        menuBar.Append(licitacoesMenu, u'Licitações')
        menuBar.Append(atasMenu,u'Adesão de Ata')
        menuBar.Append(contabilMenu, u'Contábil')
        #menuBar.Append(usuariosMenu, u'Usuários')
        #menuBar.Append(backupMenu, u'Backup')
        menuBar.Append(relatoriosMenu, u'Relatórios')
        self.SetMenuBar(menuBar)

        #Fim Menu

        #StatusBar

        self.status = self.CreateStatusBar(number=4)
        self.status.SetStatusText(u'Usuário: '+user.name, 1)
        self.status.SetStatusText(u'Login: '+user.login, 2)
        self.status.SetStatusText(date.today().strftime('%d/%m/%Y'), 3)

        #Fim StatusBar

        #Binds

        self.Bind(wx.EVT_MENU, self.windowContrato, contratosSubMenu)
        self.Bind(wx.EVT_MENU, self.windowEmpenhoContrato, empenhosContratosSubMenu)
        self.Bind(wx.EVT_MENU, self.windowConvenio, convenioSubMenu)
        self.Bind(wx.EVT_MENU, self.windowParticipanteConvenio, participantesConvenioSubMenu)
        self.Bind(wx.EVT_MENU, self.windowEmpenhoConvenio, empenhosConvenioSubmenu)
        self.Bind(wx.EVT_MENU, self.windowLicitacao, licitacoesMenuItem1)
        self.Bind(wx.EVT_MENU, self.windowItemLicitacao, licitacoesMenuItem2)
        self.Bind(wx.EVT_MENU, self.windowParticipanteLicitacao, licitacoesMenuItem3)
        self.Bind(wx.EVT_MENU, self.windowCotacao, licitacoesMenuItem4)
        self.Bind(wx.EVT_MENU, self.windowCertidao, licitacoesMenuItem5)
        self.Bind(wx.EVT_MENU, self.windowPublicacao, licitacoesMenuItem6)
        #self.Bind(wx.EVT_MENU, self.windowDotacao, licitacoesMenuItem7)
        self.Bind(wx.EVT_MENU, self.windowItemAta,atasMenuItem1)
        self.Bind(wx.EVT_MENU, self.windowLicitacaoAta,atasMenuItem2)
        self.Bind(wx.EVT_MENU, self.windowPlanoConta, planoDeContasSubMenu)
        self.Bind(wx.EVT_MENU, self.windowConta, contasSubMenu)
        self.Bind(wx.EVT_MENU, self.windowMovConInicial, movConInicialSubMenu)
        self.Bind(wx.EVT_MENU, self.windowMovConMensal, movConMensalSubMenu)
        self.Bind(wx.EVT_MENU, self.windowMovConFinal, movConFinalSubMenu)
        #self.Bind(Wx.EVT_MENU, self., movConSubMenu)
        #self.Bind(wx.EVT_MENU, self.windowUser, usuarioMenuItem1)
        #self.Bind(wx.EVT_MENU, self.backup, backupMenuItem1)
        #self.Bind(wx.EVT_MENU, self.restoreBackup, backupMenuItem2)
        self.Bind(wx.EVT_MENU, self.gerarRelatorioContrato, relatoriosMenuItem1)

        

        #Fim Binds

        self.Maximize()
        self.Show()

    def backup(self, event):
        import os
        self.message = wx.MessageDialog(None, u'Para realizar o backup da base de dados é altamente recomendado,por motivos de segurança,que você escolha uma unidade diferente de onde está instalada a aplicação!', 'Info', wx.OK)
        self.message.ShowModal()

        dlgDir = wx.DirDialog(None, message=u"Escolha um diretório")
        if dlgDir.ShowModal() == wx.ID_OK:
            try:
                shutil.copy(os.getcwd()+'\\db\\database.sqlite', dlgDir.GetPath().encode("utf-8"))
            except TypeError:

                self.message = wx.MessageDialog(None, u'Houve um erro na realização do seu backup!Por favor tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0
            self.message = wx.MessageDialog(None, u'Backup realizado com sucesso!Um arquivo database.sqlite foi gerado no diretório escolhido!', 'Info', wx.OK)
            self.message.ShowModal()

    def restoreBackup(self, event):
        import os
        dlgDirFile = wx.FileDialog(None, message=u"Selecione o arquivo...", wildcard="*.sqlite")
        if dlgDirFile.ShowModal() == wx.ID_OK:
            if dlgDirFile.GetFilename() == 'database.sqlite':
                try:
                    #import commands
                    #cmd = 'cp -R %s %s' % (dlgDirFile.GetPath().encode("utf-8"), os.getcwd()+'\\db\\')
                    #commands.getstatusoutput(cmd)
                    shutil.copy(dlgDirFile.GetPath().encode("utf-8"), os.getcwd()+'\\db\\')
                except:
                    self.message = wx.MessageDialog(None, u'Houve um erro na inesperado na restauração do seu backup!Por favor tente novamente!', 'Info', wx.OK)
                    self.message.ShowModal()
                    return 0
                self.message = wx.MessageDialog(None, u'A restauração do Backup foi realizado com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
            else:
                self.message = wx.MessageDialog(None, u'O arquivo de backup deve ter EXATAMENTE o nome:\n\ndatabase.sqlite\n\n Caso este esteja alterado renome-o e repita o processo de Resauração de Backup !', 'Info', wx.OK)
                self.message.ShowModal()

    def windowContrato(self, event):
        import WindowContrato
        WindowContrato.WindowContrato(self)

    def windowConvenio(self, event):
        import WindowConvenio
        WindowConvenio.WindowConvenio(self)

    def windowParticipanteConvenio(self, event):
        import WindowParticipanteConvenio
        WindowParticipanteConvenio.WindowParticipanteConvenio(self)

    def windowLicitacao(self, event):
        import WindowLicitacao
        WindowLicitacao.WindowLicitacao(self)

    def windowItemLicitacao(self, event):
        import WindowItemLicitacao
        WindowItemLicitacao.WindowItemLicitacao(self)

    def windowParticipanteLicitacao(self, event):
        import WindowParticipanteLicitacao
        WindowParticipanteLicitacao.WindowParticipanteLicitacao(self)

    def windowCotacao(self, event):
        import WindowCotacao
        WindowCotacao.WindowCotacao(self)

    def windowCertidao(self, event):
        import WindowCertidao
        WindowCertidao.WindowCertidao(self)

    def windowEmpenhoContrato(self, event):
        import WindowEmpenhoContrato
        WindowEmpenhoContrato.WindowEmpenhoContrato(self)

    def windowEmpenhoConvenio(self, event):
        import WindowEmpenhoConvenio
        WindowEmpenhoConvenio.WindowEmpenhoConvenio(self)

    def windowPublicacao(self, event):
        import WindowPublicacao
        WindowPublicacao.WindowPublicacao(self)

    def windowDotacao(self, event):
        import WindowDotacao
        WindowDotacao.WindowDotacao(self)

    def windowItemAta(self, event):
        import WindowItemAta
        WindowItemAta.WindowItemAta(self)

    def windowLicitacaoAta(self, event):
        import WindowLicitacaoAta
        WindowLicitacaoAta.WindowLicitacaoAta(self)

    def windowPlanoConta(self, event):
        import WindowPlanoConta
        WindowPlanoConta.WindowPlanoConta(self)

    def windowConta(self, event):
        import WindowConta
        WindowConta.WindowConta(self)

    def windowMovConInicial(self,event):
        import WindowMovConInicial
        WindowMovConInicial.WindowMovConInicial(self)

    def windowMovConMensal(self, event):
        import WindowMovConMensal
        WindowMovConMensal.WindowMovConMensal(self)
    
    def windowMovConFinal(self, event):
        import WindowMovConFinal
        WindowMovConFinal.WindowMovConFinal(self)
    
    def windowUser(self, event):
        import WindowUser
        WindowUser.WindowUser(self)

    def gerarRelatorioContrato(self, event):
        import WindowRelatorio
        WindowRelatorio.WindowRelatorio(self)

    def quit(self, event):
        self.MakeModal(False)
        self.Destroy()

if __name__ == '__main__':
    
    app = wx.App(redirect=False)
    access = WindowMain(None)
    app.MainLoop()
 
