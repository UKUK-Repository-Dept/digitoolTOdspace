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
        checked, convertedMetadata, attachements = convertItem(oai_id, False)
