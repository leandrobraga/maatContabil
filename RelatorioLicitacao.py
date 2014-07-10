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

class RelatorioLicitacao(Report):


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
            SystemField(expression=u'Relatório de Licitações - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}
    

    class band_detail(ReportBand):

        

        height = 4.3*cm
        elements = [

            Label(text="Num. Processo Licitatório:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text="Tipo Licitação:", top=1.2*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Modalidade:", top=1.2*cm, left=6*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Descrição:", top=1.9*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Num. Edital Licitação:", top=2.6*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text="Data Publicação Edital:", top=2.6*cm, left=8*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Diário Oficial:", top=3.3*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text="Valor:", top=3.3*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            
            
            ObjectValue(attribute_name='numeroProcessoLicitatorio', top=0.5*cm, left=4.6*cm),
            ObjectValue(attribute_name='tipoLicitacao', width=10*cm , top=1.2*cm, left=2.6*cm),
            ObjectValue(attribute_name='modalidadeLicitacao', width=10*cm , top=1.2*cm, left=8.2*cm),
            ObjectValue(attribute_name='descricaoLicitacao', width=20*cm , top=1.9*cm, left=1.9*cm),
            ObjectValue(attribute_name='numeroEditalLicitacao', top=2.6*cm, left=3.8*cm),
            ObjectValue(attribute_name='dataLicitacao', width=10*cm , top=2.6*cm, left=12*cm),
            ObjectValue(attribute_name='numeroDiarioOficial', width=10*cm , top=3.3*cm, left=2.4*cm),
            ObjectValue(attribute_name='valorDespesa', width=5*cm , top=3.3*cm, left=8.1*cm, get_value=lambda instance: converte(instance.valorDespesa)),
            
            
            ]


    