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

def test_oai():
    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx)
    dt = Digitool(digitool_category) 
    dt.download_list()
    bugs.oai(dt,dtx,c)
    assert str(c) == '''
ksp 57
mff 3
psy 2176
uisk 0
12345 0
other ingest 52
['HTF'] 5
['FFUk', 'FF', 'FF UK', 'FFUK'] 503
['etf', 'ETF'] 59
['MFF'] 56
['PF'] 24
['FTVS'] 0
['2LF', 'LF2', '2LF -'] 1
['FSV', 'FSV IMS', 'FSV_IKSZ', 'FSV ISS', 'FSV IPS'] 18
['FHS'] 44
['3LF'] 5
other note 330
None note 137
no xml file 53
celkem 3523'''

def test_forgot():
    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx)
    dt = Digitool(digitool_category) 
    dt.download_list()
    bugs.forgot_attachements(dt,dtx,c,xml_dirname+"/ls_streams.txt")
    assert str(c) == '''
ksp 377
mff 297
psy 166
uisk 7
12345 37
other ingest 3
['HTF'] 74
['FFUk', 'FF', 'FF UK', 'FFUK'] 70
['etf', 'ETF'] 38
['MFF'] 31
['PF'] 19
['FTVS'] 13
['2LF', 'LF2', '2LF -'] 10
['FSV', 'FSV IMS', 'FSV_IKSZ', 'FSV ISS', 'FSV IPS'] 10
['FHS'] 3
['3LF'] 2
other note 0
None note 62
no xml file 0
celkem 1219'''

def test_noattachement():
    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx)
    dt = Digitool(digitool_category) 
    dt.download_list()
    bugs.no_attachements(dt,dtx,c)
    assert str(c) == '''
ksp 0
mff 0
psy 0
uisk 0
12345 0
other ingest 0
['HTF'] 0
['FFUk', 'FF', 'FF UK', 'FFUK'] 0
['etf', 'ETF'] 2
['MFF'] 0
['PF'] 0
['FTVS'] 0
['2LF', 'LF2', '2LF -'] 0
['FSV', 'FSV IMS', 'FSV_IKSZ', 'FSV ISS', 'FSV IPS'] 0
['FHS'] 0
['3LF'] 0
other note 0
None note 5
no xml file 53
celkem 60'''


def test_weird():
    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx)
    dt = Digitool(digitool_category) 
    dt.download_list()
    bugs.weird_attachements(dt,dtx,c)
    assert str(c) == '''
ksp 0
mff 0
psy 4
uisk 0
12345 0
other ingest 31
['HTF'] 0
['FFUk', 'FF', 'FF UK', 'FFUK'] 2
['etf', 'ETF'] 0
['MFF'] 1
['PF'] 0
['FTVS'] 0
['2LF', 'LF2', '2LF -'] 0
['FSV', 'FSV IMS', 'FSV_IKSZ', 'FSV ISS', 'FSV IPS'] 0
['FHS'] 0
['3LF'] 0
other note 4
None note 14
no xml file 0
celkem 56'''
