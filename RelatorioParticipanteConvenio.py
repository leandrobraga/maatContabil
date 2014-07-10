#! -*- coding: utf-8 -*-

from models import *
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.colors import navy, yellow, red, black

from geraldo import Report, ReportBand, Label, Line, SubReport,ObjectValue, SystemField,\
    FIELD_ACTION_COUNT, FIELD_ACTION_AVG, FIELD_ACTION_MIN,\
    FIELD_ACTION_MAX, FIELD_ACTION_SUM, FIELD_ACTION_DISTINCT_COUNT, BAND_WIDTH,\
    RoundRect, Line
from geraldo.base import EmptyQueryset


setup_all()

def split1000(s, sep='.'):
    
    if len(s) <= 3:
        return s
    else:
        return split1000(s[:-3], sep) + sep + s[-3:]

def converte(valor):

    partes = valor.split('.')
    
    if len(partes[1]) >1:
        centavos =partes[1]
    else:
        centavos = partes[1]+'0'
        
    return split1000(partes[0])+','+centavos



class RelatorioParticipanteConvenio(Report):


    title = u'Relatório de Contratos - Competência: '
    print_if_empty = True        
        

    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
        Label(text='Sistema Maat', top=0.1*cm, right=0), SystemField(expression='Gerado em %(now: %d/%m/%Y)s às %(now:%H:%M)s', 
            top=0.1*cm, width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]

        borders = {'top': Line(stroke_color=black, stroke_width=2)}


    class band_page_header(ReportBand):
        height = 1.3*cm
        elements = [
            SystemField(expression=u'Relatório de Participantes de Convênio - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}
    
    class band_detail(ReportBand):

        

        height = 14*cm
        elements = [
            Label(text="Convênio:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text="Tipo Pessoa:", top=1.2*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="CPF/CNPJ:", top=1.2*cm, left=11*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Nome:", top=1.9*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Valor Participação:", top=2.6*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Percentual Participação:", top=2.6*cm, left=11*cm, style={'fontName':'Helvetica-Bold'}),
            
            Label(text=u"INSS:", top=3.3*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=4*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=4*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            
            Label(text=u"FGTS:", top=4.7*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=5.4*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=5.4*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            
            Label(text=u"Faz. Federal:", top=6.1*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=6.8*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=6.8*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            
            Label(text=u"Faz. Estadual:", top=7.5*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=8.2*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=8.2*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            
            Label(text=u"Faz. Municipal:", top=8.9*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=9.6*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=9.6*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            
            Label(text=u"Outras:", top=10.3*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=11*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=11*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),

            Label(text=u"CNDT:", top=11.7*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Emissão:", top=12.4*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=12.4*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            
            
            ObjectValue(attribute_name='numeroConvenio', top=0.5*cm, left=1.8*cm),
            ObjectValue(attribute_name='pessoaParticipante', width=10*cm , top=1.2*cm, left=2.2*cm),
            ObjectValue(attribute_name='cicParticipante', width=10*cm , top=1.2*cm, left=13*cm),
            ObjectValue(attribute_name='nomeParticipante', width=5*cm , top=1.9*cm, left=1.3*cm),
            ObjectValue(attribute_name='valorParticipacao', width=5*cm , top=2.6*cm, left=3.3*cm, get_value=lambda instance: converte(instance.valorParticipacao)),
            ObjectValue(attribute_name='percentualParticipacao', width=10*cm , top=2.6*cm, left=15.2*cm, get_value=lambda instance: converte(instance.percentualParticipacao)),
            
            ObjectValue(attribute_name='certidaoINSS', width=10*cm , top=3.3*cm, left=1.1*cm),
            ObjectValue(attribute_name='dataINSS', width=10*cm , top=4*cm, left=3.1*cm),
            ObjectValue(attribute_name='dataValidadeINSS', width=10*cm , top=4*cm, left=9.6*cm),
            
            ObjectValue(attribute_name='certidaoFGTS', width=10*cm , top=4.7*cm, left=1.1*cm),
            ObjectValue(attribute_name='dataFGTS', width=10*cm , top=5.4*cm, left=3.1*cm),
            ObjectValue(attribute_name='dataValidadeFGTS', width=10*cm , top=5.4*cm, left=9.6*cm),
            
            ObjectValue(attribute_name='certidaoFazendaFederal', width=10*cm , top=6.1*cm, left=2.3*cm),
            ObjectValue(attribute_name='dataFazendaFederal', width=10*cm , top=6.8*cm, left=3.3*cm),
            ObjectValue(attribute_name='dataValidadeFazendaFederal', width=10*cm , top=6.8*cm, left=9.9*cm),

            ObjectValue(attribute_name='certidaoFazendaEstadual', width=10*cm , top=7.5*cm, left=2.5*cm),
            ObjectValue(attribute_name='dataFazendaEstadual', width=10*cm , top=8.2*cm, left=3.3*cm),
            ObjectValue(attribute_name='dataValidadeFazendaEstadual', width=10*cm , top=8.2*cm, left=9.9*cm),

            ObjectValue(attribute_name='certidaoFazendaMunicipal', width=10*cm , top=8.9*cm, left=2.6*cm),
            ObjectValue(attribute_name='dataFazendaMunicipal', width=10*cm , top=9.6*cm, left=3.3*cm),
            ObjectValue(attribute_name='dataValidadeFazendaMunicipal', width=10*cm , top=9.6*cm, left=9.9*cm),

            ObjectValue(attribute_name='certidaoOutras', width=10*cm , top=10.3*cm, left=1.5*cm),
            ObjectValue(attribute_name='dataOutras', width=10*cm , top=11*cm, left=3.3*cm),
            ObjectValue(attribute_name='dataValidadeOutras', width=10*cm , top=11*cm, left=9.9*cm),

            ObjectValue(attribute_name='certidaoCNDT', width=10*cm , top=11.7*cm, left=1.5*cm),
            ObjectValue(attribute_name='dataCNDT', width=10*cm , top=12.4*cm, left=3.3*cm),
            ObjectValue(attribute_name='dataValidadeCNDT', width=10*cm , top=12.4*cm, left=9.9*cm),
            


            
            
            ]

