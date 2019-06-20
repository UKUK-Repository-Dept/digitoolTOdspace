from digitoolOAI import Digitool
from digitoolXML import DigitoolXML
from dspace import Dspace
from filenameConvertor import FilenameConvertor
from metadataConvertor import MetadataConvertor
from categorize import Categorize
import problematicGroup as bugs
from digitoolTOdspace import *

def test_convertItem():
    a = convertItem(104691, False)

def test_convert():
    dt = Digitool(digitool_category) 
    dt.download_list()
    dtx = DigitoolXML(xml_dirname)
    categorize = Categorize(dtx)
    c = MetadataConvertor(categorize)
    for record in dt.list:
        oai_id = dt.get_oai_id(record)
       # checked, convertedMetadata, attachements = convertItem(oai_id, False)
        #print(oai_id)
        attachements = list(dtx.get_attachements(oai_id))

#def test_categorize(group):
#    #TODO všechny dalši skupiny viz ostatni TODO
#
#    dtx = DigitoolXML(xml_dirname)
#    c = Categorize(dtx)
#    dt = Digitool(digitool_category) 
#    dt.download_list()
#    if group == 'oai':
#        bugs.oai(dt,dtx,c)
#    elif group == 'forgot':
#        bugs.forgot_attachements(dt,dtx,c,xml_dirname+"/ls_streams.txt")
#    elif group == 'noattachement':
#        bugs.no_attachements(dt,dtx,c)
#    elif group == 'weird':
#        bugs.weird_attachements(dt,dtx,c)
#    elif group == 'type':
#        bugs.unknown_type(dt,dtx,c)
#    elif group == 'preview':
#        dtx_no_skip = DigitoolXML(xml_dirname)
#        dtx_all = DigitoolXML('s-nahledy')
#        bugs.preview(dt,dtx_no_skip,dtx_all)
#        return
#    elif group == 'all':
#        bugs.forgot_attachements(dt,dtx,c,xml_dirname+"/ls_streams.txt")
#        bugs.no_attachements(dt,dtx,c)
#        bugs.weird_attachements(dt,dtx,c)
#    c.print()


