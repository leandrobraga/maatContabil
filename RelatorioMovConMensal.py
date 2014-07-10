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

    valor = float(valor)
    valor = unicode(valor)
    partes = valor.split('.')
    
    if len(partes[1]) >1:
        centavos =partes[1]
    else:
        centavos = partes[1]+'0'
        
    return split1000(partes[0])+','+centavos

class RelatorioMovConMensal(Report):


    title = u'Relatório de Movimento Contábil Mensal - Competência: '
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
            SystemField(expression=u'Relatório de Movimento Contábil Mensal - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}

    
    class band_detail(ReportBand):

        height = 2.0*cm
        elements = [
            
            Label(text=u"Código da Conta:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Ano de Criação:", top=0.5*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Débito:", top=1*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Crédito:", top=1*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            

            ObjectValue(attribute_name='codigoConta', top=0.5*cm, left=3.1*cm),
            ObjectValue(attribute_name='anoConta', top=0.5*cm, left=10*cm),
            ObjectValue(attribute_name='debito', top=1*cm, left=1.5*cm, get_value=lambda instance: converte(instance.debito)),
            ObjectValue(attribute_name='credito', top=1*cm, left=8.5*cm, get_value=lambda instance: converte(instance.credito)),
                        
        ]
