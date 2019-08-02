from filenameConvertor import FilenameConvertor
from metadataConvertor import Metadata
from tag502 import convertTag502

def all_attachements(oai_ids, dtx, c):
    forgot_attachements(oai_ids,dtx,c)
    no_attachements(oai_ids,dtx,c)
    weird_attachements(oai_ids,dtx,c)

def oai(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        categorize.categorize_item(oai_id,"je v oai")

def dc(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'dc' in originalMetadataXML.keys():
            c = Metadata(categorize, oai_id)
            c.convertDC(originalMetadataXML['dc'])

def marc(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'marc' in originalMetadataXML.keys():
            m = Metadata(categorize, oai_id)
            m.convertMarc(originalMetadataXML['marc'])

def no502(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'marc' in originalMetadataXML.keys():
            metadata = originalMetadataXML['marc']
            if not '502- - ' in metadata.keys():
                error_msg = "No tag 502"
                categorize.categorize_item(oai_id,error_msg)
                continue

def tag502(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'marc' in originalMetadataXML.keys():
            metadata = originalMetadataXML['marc']
            if not '502- - ' in metadata.keys():
                continue
            convertTag502(metadata['502- - '],oai_id,categorize)

def forgot_attachements(oai_ids, digitoolXML, categorize):
    attachements = []
    for oai_id in oai_ids:
        attachements += list(digitoolXML.get_attachements(oai_id))
    for row in open( digitoolXML.xml_dirname.split('/')[0]+"/ls_streams.txt" ,"r"):
        if '_index.html' in row:
            continue
        if '_thumbnail.jpg' in row:
            continue
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
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if 'marc' in originalMetadataXML.keys():
            m = Metadata(categorize, oai_id)
            m.convertMarc(originalMetadataXML['marc'])
            #print(m.degree) TODO poslat dovnitr
            attachements = list(digitoolXML.get_attachements(oai_id,full=True))
            descriptions = convertor.generate_description(attachements)
        else:
            assert 'dc' in originalMetadataXML.keys()
            #TODO

        if isinstance(descriptions, list):
            continue
        print(descriptions)

