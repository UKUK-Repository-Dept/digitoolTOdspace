from filenameConvertor import FilenameConvertor
from metadataConvertor import Metadata

def oai(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        categorize.categorize_item(oai_id,"je v oai")

def dc(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'dc' in originalMetadataXML.keys():
            c = Metadata(categorize, oai_id)
            c.convertDC(originalMetadataXML['dc'])

def tag502(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'marc' in originalMetadataXML.keys():
            c = Metadata(categorize, oai_id)
            c.convertMarc(originalMetadataXML['marc'])

def forgot_attachements(oai_ids, digitoolXML, categorize, xml_attachements_list):
    attachements = []
    for oai_id in oai_ids:
        attachements += list(digitoolXML.get_attachements(oai_id))
    for row in open(xml_attachements_list,"r"):
        if not row[:-1] in attachements:
            oai_id = row.split("_")[0]
            categorize.categorize_item(oai_id,"opomenuty soubor bez metadat".format(oai_id))

def no_attachements(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        attachements = list(digitoolXML.get_attachements(oai_id))
        if len(attachements) == 0:
            categorize.categorize_item(oai_id,"bez přílohy")

def weird_attachements(oai_ids, digitoolXML, categorize):
    convertor = FilenameConvertor(categorize)
    for oai_id in oai_ids:
        attachements = list(digitoolXML.get_attachements(oai_id,full=True))
        if len(attachements) == 0:
            continue
        descriptions = convertor.generate_description(attachements)
        if isinstance(descriptions, list):
            continue
        print(descriptions)

