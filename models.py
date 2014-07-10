#!/usr/bin/python
# -*- coding: utf-8 -*-

from elixir import *
metadata.bind = 'sqlite:///db/database.sqlite'
metadata.bind.echo = False


class Contrato(Entity):

    numeroContrato = Field(Unicode(18))
    valorContrato = Field(Unicode(18))
    dataAssinaturaContrato = Field(Unicode(10))
    objetivoContrato = Field(Unicode(50))
    numeroProcessoLicitatorio = Field(Unicode(18))
    codigoMoeda = Field(Unicode(3))
    tipoJuridicoContratado = Field(Unicode(1))
    cicContratado = Field(Unicode(14))
    nomeContratado = Field(Unicode(50))
    dataVencimentoContrato = Field(Unicode(10))
    numeroDiarioOficial = Field(Unicode(6))
    dataPublicacaoContrato = Field(Unicode(10))
    recebeValor = Field(Unicode(1))
    numeroCertidaoINSS = Field(Unicode(60))
    dataCertidaoINSS = Field(Unicode(10))
    dataValidadeINSS = Field(Unicode(10))
    numeroCertidaoFGTS = Field(Unicode(60))
    dataCertidaoFGTS = Field(Unicode(10))
    dataValidadeFGTS = Field(Unicode(10))
    numeroCertidaoFazendaEstadual = Field(Unicode(60))
    dataCertidaoFazendaEstadual = Field(Unicode(10))
    dataValidadeFazendaEstadual = Field(Unicode(10))
    numeroCertidaoFazendaMunicipal = Field(Unicode(60))
    dataCertidaoFazendaMunicipal = Field(Unicode(10))
    dataValidadeFazendaMunicipal = Field(Unicode(10))
    numeroCertidaoFazendaFederal = Field(Unicode(60))
    dataCertidaoFazendaFederal = Field(Unicode(10))
    dataValidadeFazendaFederal = Field(Unicode(10))
    numeroCertidaoCNDT = Field(Unicode(60))
    dataCertidaoCNDT = Field(Unicode(10))
    dataValidadeCNDT = Field(Unicode(10))
    numeroCertidaoOutras = Field(Unicode(60))
    dataCertidaoOutras = Field(Unicode(10))
    dataValidadeOutras = Field(Unicode(10))
    tipoContrato = Field(Unicode(50))
    competencia = Field(Unicode(50))

    def __repr__(self):
        return self.numeroContrato


class Convenio(Entity):

    recebeValor = Field(Unicode(1))
    numeroConvenio = Field(Unicode(16))
    valorConvenio = Field(Unicode(16))
    moedaConvenio = Field(Unicode(3))
    dataAssinaturaConvenio = Field(Unicode(8))
    objetivoConvenio = Field(Unicode(50))
    dataVencimentoConvenio = Field(Unicode(8))
    leiAutorizativa = Field(Unicode(6))
    dataLeiAutorizativa = Field(Unicode(8))
    numeroDiarioOficial = Field(Unicode(6))
    dataPublicacaoConvenio = Field(Unicode(8))
    tipoConvenio = Field(Unicode(2))
    competencia = Field(Unicode(50))

    def __repr__(self):
        return self.numeroConvenio


class ParticipanteConvenio(Entity):

    cicParticipante = Field(Unicode(14))
    pessoaParticipante = Field(Unicode(1))
    nomeParticipante = Field(Unicode(50))
    valorParticipacao = Field(Unicode(16))
    percentualParticipacao = Field(Unicode(7))
    
    certidaoINSS = Field(Unicode(60))
    dataINSS = Field(Unicode(8))
    dataValidadeINSS = Field(Unicode(8))
    certidaoFGTS = Field(Unicode(60))
    dataFGTS = Field(Unicode(8))
    dataValidadeFGTS = Field(Unicode(8))
    certidaoFazendaEstadual = Field(Unicode(60))
    dataFazendaEstadual = Field(Unicode(8))
    dataValidadeFazendaEstadual = Field(Unicode(8))
    certidaoFazendaMunicipal = Field(Unicode(60))
    dataFazendaMunicipal = Field(Unicode(8))
    dataValidadeFazendaMunicipal = Field(Unicode(8))
    certidaoFazendaFederal = Field(Unicode(60))
    dataFazendaFederal = Field(Unicode(8))
    dataValidadeFazendaFederal = Field(Unicode(8))
    certidaoCNDT = Field(Unicode(60))
    dataCNDT = Field(Unicode(8))
    dataValidadeCNDT = Field(Unicode(8))
    certidaoOutras = Field(Unicode(60))
    dataOutras = Field(Unicode(8))
    dataValidadeOutras = Field(Unicode(8))
    numeroConvenio = Field(Unicode(16))
    esferaConvenio = Field(Unicode(1))
    
    competencia = Field(Unicode(50))

    def __repr__(self):
        return self.nomeParticipante


class Licitacao(Entity):

    numeroProcessoLicitatorio = Field(Unicode(16))
    numeroDiarioOficial = Field(Unicode(6))
    dataLicitacao = Field(Unicode(8))
    modalidadeLicitacao = Field(Unicode(1))
    descricaoLicitacao = Field(Unicode(50))
    valorDespesa = Field(Unicode(16))
    numeroEditalLicitacao = Field(Unicode(16))
    tipoLicitacao = Field(Unicode(1))
    competencia = Field(Unicode(50))

    def __repr__(self):
        return self.numeroProcessoLicitatorio


class ItemLicitacao(Entity):

    numeroProcessoLicitatorio = Field(Unicode(18))
    sequenciaItem = Field(Unicode(5))
    descricaoItem = Field(Unicode(300))
    quantidadeItem = Field(Unicode(16))
    dataAssinatura = Field(Unicode(10))
    dataPublicacao = Field(Unicode(10))
    unidadeMedida = Field(Unicode(30))
    statusItem = Field(Unicode(2))
    competencia = Field(Unicode(40))
    controleItem = Field(Unicode(10))

    def __repr__(self):
        return self.descricaoItem


class ParticipanteLicitacao(Entity):

    numeroProcessoLicitatorio = Field(Unicode(18))
    cicParticipante = Field(Unicode(14))
    tipoJuridicoParticipante = Field(Unicode(1))
    nomeParticipante = Field(Unicode(50))
    tipoParticipacao = Field(Unicode(1))
    cicConsorcio = Field(Unicode(14))
    participanteConvidado = Field(Unicode(1))
    
    competencia = Field(Unicode(40))

    def __repr__(self):
        return self.nomeParticipante


class Cotacao(Entity):

    tipoValor = Field(Unicode(1))
    numeroProcessoLicitatorio = Field(Unicode(18))
    tipoJuridico = Field(Unicode(1))
    cicParticipante = Field(Unicode(14))
    sequenciaItem = Field(Unicode(5))
    valorCotado = Field(Unicode(16))
    situacaoParticipante = Field(Unicode(1))
    quantidadeItem = Field(Unicode(16))
    competencia = Field(Unicode(40))
    controleItem = Field(Unicode(10))


class Certidao(Entity):

    numeroProcesso = Field(Unicode(16))
    cicParticipante = Field(Unicode(14))
    tipoCertidao = Field(Unicode(2))
    tipoJuridico = Field(Unicode(1))
    numeroCertidao = Field(Unicode(16))
    dataEmissao = Field(Unicode(10))
    dataValidade = Field(Unicode(10))
    competencia = Field(Unicode(30))

    def __repr__(self):

        return self.numeroCertidao


class ContratoEmpenho(Entity):

    numeroContrato = Field(Unicode(16))
    notaEmpenho = Field(Unicode(10))
    anoEmpenho = Field(Unicode(4))
    unidadeOrcamentaria = Field(Unicode(6))
    competencia = Field(Unicode(30))

    def __repr__(self):
        return self.notaEmpenho


class ConvenioEmpenho(Entity):

    numeroConvenio = Field(Unicode(16))
    notaEmpenho = Field(Unicode(10))
    anoEmpenho = Field(Unicode(4))
    unidadeOrcamentaria = Field(Unicode(6))
    competencia = Field(Unicode(30))

    def __repr__(self):
        return self.notaEmpeho


class Publicacao(Entity):

    numeroProcesso = Field(Unicode(16))
    dataPublicacao = Field(Unicode(10))
    veiculoComunicacao = Field(Unicode(50))
    competencia = Field(Unicode(30))

    def __repr__(self):
        return self.numeroProcesso


class Dotacao(Entity):

    numeroProcesso = Field(Unicode(16))
    categoriaEconomica = Field(Unicode(1))
    grupoNatureza = Field(Unicode(1))
    modalidadeAplicacao = Field(Unicode(2))
    elemento = Field(Unicode(2))
    unidadeOrcamentaria = Field(Unicode(6))
    fonteRecurso = Field(Unicode(10))
    acaoGoverno = Field(Unicode(7))
    subFuncao = Field(Unicode(3))
    funcao = Field(Unicode(2))
    programa = Field(Unicode(4))
    competencia = Field(Unicode(30))


class User(Entity):

    name = Field(Unicode(50), required=True)
    login = Field(Unicode(50), required=True)
    password = Field(Unicode(50), required=True)
    level = Field(Integer, required=False)

    def __repr__(self):
        return self.name

class ItemAta(Entity):

    processoCompra = Field(Unicode(18), required=True)
    numeroAta = Field(Unicode(18), required=True)
    quantidade = Field(Unicode(2), required=True)
    sequenciaItem = Field(Unicode(5), required=True)
    valorItem = Field(Unicode(16), required=True)
    unidadeMedida = Field(Unicode(30), required=True)
    descricaoItem = Field(Unicode(300), required=True)
    competencia = Field(Unicode(30))

class LicitacaoAta(Entity):

    processoCompra = Field(Unicode(18), required=True)
    numeroAta = Field(Unicode(18), required=True)
    numeroLicitacao = Field(Unicode(18), required=True)
    publicacaoDOE = Field(Unicode(8), required=True)
    dataValidade = Field(Unicode(8), required=True)
    numeroDOE = Field(Unicode(6), required=True)
    dataAdesao = Field(Unicode(8), required=True)
    tipoAdesao = Field(Unicode(2), required=True)
    competencia = Field(Unicode(30), required=True)


class PlanoConta(Entity):
    
    conta = Field(Unicode(34), required=True)
    descricao = Field(Unicode(50), required=True)


class Conta(Entity):

    anoConta = Field(Unicode(4), required=True)
    codigoConta = Field(Unicode(34), required=True)
    nomeConta = Field(Unicode(50), required=True)
    nivelConta = Field(Unicode(2), required=True)
    recebeLancamento = Field(Unicode(1), required=True)
    tipoSaldo = Field(Unicode(50), required=True)
    codigoContaSuperior = Field(Unicode(34), required=True)
    codigoReduzido = Field(Unicode(10), required=True)
    codigoItem = Field(Unicode(10), required=True)
    codigoBanco = Field(Unicode(10), required=True)
    codigoAgencia = Field(Unicode(11), required=True)
    numeroConta = Field(Unicode(11), required=True)
    tipoConta = Field(Unicode(11), required=True)
    codigoTc = Field(Unicode(11), required=True)
    anoContaSuperior = Field(Unicode(11), required=True)
    competencia = Field(Unicode(40), required= True)


class MovConIni(Entity):

    anoConta = Field(Unicode(4), required=True)
    codigoConta = Field(Unicode(34), required=True)
    tipoMovimento = Field(Unicode(2), required=True)
    debito = Field(Unicode(16), required=True)
    credito = Field(Unicode(16), required=True)
    competencia = Field(Unicode(40), required= True)

class MovConMensal(Entity):

    anoConta = Field(Unicode(4), required=True)
    codigoConta = Field(Unicode(34), required=True)
    tipoMovimento = Field(Unicode(2), required=True)
    debito = Field(Unicode(16), required=True)
    credito = Field(Unicode(16), required=True)
    competencia = Field(Unicode(40), required= True)

class MovConFinal(Entity):

    anoConta = Field(Unicode(4), required=True)
    codigoConta = Field(Unicode(34), required=True)
    tipoMovimento = Field(Unicode(2), required=True)
    debito = Field(Unicode(16), required=True)
    credito = Field(Unicode(16), required=True)
    competencia = Field(Unicode(40), required= True)

