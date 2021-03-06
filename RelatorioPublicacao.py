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


class RelatorioPublicacao(Report):


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
            SystemField(expression=u'Relatório de Publicações - Competência: %(var:competencia)s', top=0.1*cm, left=0, width=BAND_WIDTH, 
                style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER, 'textColor': black}),
            SystemField(expression=u'%(page_number)d de %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
        ]

        borders = {'bottom': Line(stroke_color=black)}

    
    class band_detail(ReportBand):

        height = 2.5*cm
        elements = [
            
            Label(text=u"Num. Processo Licitatório:", top=0.5*cm, left=0, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Data Publicação:", top=1.2*cm, left=0*cm, style={'fontName':'Helvetica-Bold'}),
            Label(text=u"Veiculo:", top=1.2*cm, left=11*cm, style={'fontName':'Helvetica-Bold'}),
            

            ObjectValue(attribute_name='numeroProcesso', top=0.5*cm, left=4.6*cm),
            ObjectValue(attribute_name='dataPublicacao', width=5*cm , top=1.2*cm, left=3*cm),
            ObjectValue(attribute_name='veiculoComunicacao', width=10*cm, top=1.2*cm, left=12.5*cm),
            
        ]
