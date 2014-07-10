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



class RelatorioConvenio(Report):


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
            SystemField(expression=u'Relatório de Convênios - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}
    
    class band_detail(ReportBand):

        

        height = 5.5*cm
        elements = [

            Label(text="Número:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text="Tipo:", top=0.5*cm, left=11*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Objetivo:", top=1.2*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Recebe valor:", top=1.9*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Tipo Moeda:", top=1.9*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Valor:", top=1.9*cm, left=12.8*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Assinatura:", top=2.6*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Vencimento:", top=2.6*cm, left=9*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Num. da Lei Autoriztiva:", top=3.3*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data da Lei Autorizativa:", top=3.3*cm, left=9*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Num. Diário oficial Est/Mun:", top=4*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data da Publicação:", top=4*cm, left=9*cm, style={'fontName':'Helvetica-Bold'}),
           
            
            ObjectValue(attribute_name='numeroConvenio', top=0.5*cm, left=1.7*cm),
            ObjectValue(attribute_name='tipoConvenio', width=10*cm , top=0.5*cm, left=12*cm),
            ObjectValue(attribute_name='objetivoConvenio', width=5*cm , top=1.2*cm, left=1.7*cm),
            ObjectValue(attribute_name='recebeValor', width=10*cm , top=1.9*cm, left=2.4*cm),
            ObjectValue(attribute_name='moedaConvenio', width=10*cm , top=1.9*cm, left=8.2*cm),
            ObjectValue(attribute_name='valorConvenio', width=10*cm , top=1.9*cm, left=14*cm, get_value=lambda instance: converte(instance.valorConvenio)),
            ObjectValue(attribute_name='dataAssinaturaConvenio', width=10*cm , top=2.6*cm, left=3.5*cm),
            ObjectValue(attribute_name='dataVencimentoConvenio', width=10*cm , top=2.6*cm, left=12.6*cm),
            ObjectValue(attribute_name='leiAutorizativa', width=10*cm , top=3.3*cm, left=4.1*cm),
            ObjectValue(attribute_name='dataLeiAutorizativa', width=10*cm , top=3.3*cm, left=13.2*cm),
            ObjectValue(attribute_name='numeroDiarioOficial', width=10*cm , top=4*cm, left=4.8*cm),
            ObjectValue(attribute_name='dataPublicacaoConvenio', width=10*cm , top=4*cm, left=12.4*cm),
         
            ]
