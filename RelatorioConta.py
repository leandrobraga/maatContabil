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

class RelatorioConta(Report):


    title = u'Relatório de Contas - Competência: '
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
            SystemField(expression=u'Relatório de Contas - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}

    
    class band_detail(ReportBand):

        height = 5.0*cm
        elements = [
            
            Label(text=u"Código da Conta:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Nome da Conta:", top=0.5*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Ano Criação:", top=1*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Nível da Conta:", top=1*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Recebe Lançamento:", top=1.5*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Tipo de Saldo:", top=1.5*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Código da Conta:", top=2.0*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Código Reduzido:", top=2.0*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Código do Item:", top=2.5*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Código do Banco:", top=2.5*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Código da Agência:", top=3*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Num. Conta Bancária:", top=3*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Tipo Conta:", top=3.5*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Código Conta TC:", top=3.5*cm, left=7*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Ano Criação Conta Superior:", top=4*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            
            
            ObjectValue(attribute_name='codigoConta', top=0.5*cm, left=3.2*cm),
            ObjectValue(attribute_name='nomeConta', width=10*cm , top=0.5*cm, left=10*cm),
            ObjectValue(attribute_name='anoConta', top=1*cm, left=2.5*cm),
            ObjectValue(attribute_name='nivelConta', top=1*cm, left=10*cm),
            ObjectValue(attribute_name='recebeLancamento', top=1.5*cm, left=3.7*cm),
            ObjectValue(attribute_name='tipoSaldo', top=1.5*cm, left=10*cm),
            ObjectValue(attribute_name='codigoContaSuperior', top=2.0*cm, left=3.3*cm),
            ObjectValue(attribute_name='codigoReduzido', top=2.0*cm, left=10.2*cm),
            ObjectValue(attribute_name='codigoItem', top=2.5*cm, left=3*cm),
            ObjectValue(attribute_name='codigoBanco', top=2.5*cm, left=10.2*cm),
            ObjectValue(attribute_name='codigoAgencia', top=3*cm, left=3.5*cm),
            ObjectValue(attribute_name='numeroConta', top=3*cm, left=10.8*cm),
            ObjectValue(attribute_name='tipoConta', top=3.5*cm, left=2.1*cm),
            ObjectValue(attribute_name='codigoTc', top=3.5*cm, left=10.2*cm),
            ObjectValue(attribute_name='anoContaSuperior', top=4*cm, left=5*cm),
            
        ]
