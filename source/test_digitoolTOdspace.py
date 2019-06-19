from digitoolOAI import Digitool
from digitoolXML import DigitoolXML
from dspace import Dspace
from filenameConvertor import FilenameConvertor
from metadataConvertor import MetadataConvertor
from categorize import Categorize
import problematicGroup as bugs
from digitoolTOdspace import *

def test_convertItem():
    a = convertItem(104691, False, False)
    print(a)
