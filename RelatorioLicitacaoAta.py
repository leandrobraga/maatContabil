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

class RelatorioLicitacaoAta(Report):


    title = u'Relatório de Adesão Ata de Licitação - Competência: '
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
            SystemField(expression=u'Relatório de Adesão Ata de Licitação - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}

    
    class band_detail(ReportBand):

        height = 3.5*cm
        elements = [
            
            Label(text=u"Número do Proc. de Compra:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Número da Ata:", top=0.5*cm, left=11*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Num. do Proc. Licit.:", top=1.2*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Num. D. Oficial:", top=1.2*cm, left=7.4*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data Pub. D. Oficial:", top=1.2*cm, left=12.3*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Validade da Ata:", top=1.9*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data de Adesão:", top=1.9*cm, left=6.5*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"T. de Adesão:", top=1.9*cm, left=11.7*cm, style={'fontName':'Helvetica-Bold'}),
            

            ObjectValue(attribute_name='processoCompra', top=0.5*cm, left=5*cm),
            ObjectValue(attribute_name='numeroAta', width=10*cm , top=0.5*cm, left=13.8*cm),
            ObjectValue(attribute_name='numeroLicitacao', width=5*cm , top=1.2*cm, left=3.6*cm),
            ObjectValue(attribute_name='numeroDOE', width=10*cm, top=1.2*cm, left=10.2*cm),
            ObjectValue(attribute_name='publicacaoDOE', width=10*cm, top=1.2*cm, left=15.9*cm),
            ObjectValue(attribute_name='dataValidade', width=10*cm, top=1.9*cm, left=4.3*cm),
            ObjectValue(attribute_name='dataAdesao', width=10*cm , top=1.9*cm, left=9.3*cm),
            ObjectValue(attribute_name='tipoAdesao', width=10*cm , top=1.9*cm, left=14.2*cm),
            
        ]
