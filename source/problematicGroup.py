from filenameConvertor import FilenameConvertor
import metadataConvertor
from categorize import Categorize
from tags.tag502 import convertTag502
import aleph

def all_attachements(oai_ids, dtx, c):
    forgot_attachements(oai_ids,dtx,c)
    no_attachements(oai_ids,dtx,c)
    only_dc(oai_ids,dtx,c)

def oai(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        categorize.categorize_item(oai_id,"je v oai")

def forgot_attachements(oai_ids, digitoolXML, categorize):
    attachements = []
    for oai_id in oai_ids:
        attachements += list(zip(*digitoolXML.get_attachements(oai_id)))[0]
    for row in open( digitoolXML.dirname+"/ls_streams.txt" ,"r"):
        if '_index.html' in row:
            continue
        if '_thumbnail.jpg' in row:
            continue
        if not row[:-1] in attachements:
            oai_id = row.split("_")[0]
            categorize.categorize_item(oai_id,"{} nemá metadata".format(row[:-1]))


def no_attachements(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        attachements = list(digitoolXML.get_attachements(oai_id))
        if len(attachements) == 0:
            categorize.categorize_item(oai_id,"bez přílohy")

def only_dc(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        mark = False
        dc = False
        for relation in digitoolXML.get_relations(oai_id):
            originalMetadataXML = digitoolXML.get_metadata(relation)
            if 'marc' in originalMetadataXML.keys():
                mark = True
            if 'dc' in originalMetadataXML.keys():
                dc = True
        if not mark and dc:
            categorize.categorize_item(oai_id,"má dc, nemá marc")
            

def weird_attachements(oai_ids, digitoolXML, categorize):
    convertor = FilenameConvertor(categorize)
    categorizeTrash = Categorize(digitoolXML, 'no')
    records = aleph.openAleph("dtl_2006.xml")
    for oai_id in oai_ids:
        metadataDigitool = digitoolXML.get_metadata(oai_id)['marc']
        aleph_id = aleph.normalise(metadataDigitool['001'])
        originalMetadata = records[aleph_id]
        metadataTopic = metadataConvertor.convertMarc(categorizeTrash, oai_id, originalMetadata)
        degree = None
        if metadataTopic != None:
            for topicName in metadataTopic.keys():
                if 'degree' in metadataTopic[topicName].keys():
                    degree = metadataTopic[topicName]['degree']
        attachements = list(digitoolXML.get_attachements(oai_id))
        descriptions = convertor.generate_description(oai_id,attachements) #,degree)
        if descriptions == None:
            categorize.categorize_item(oai_id,"bez vystupu")

def aleph_metadata(oai_ids, digitoolXML, categorize):
    records = aleph.openAleph("dtl_2006.xml")
    for aleph_id in records.keys():
        metadata = records[aleph_id]
        digittol_id = metadata['856']['u'][0].split('=')[-1]
        oai_id = "{},{}".format(aleph_id,digittol_id)
        #oai_id = aleph_id
        #oai_id = digittol_id
        metadataTopic = metadataConvertor.convertMarc(categorize, oai_id, metadata)
        metadataReturn = metadataConvertor.createDC('gull',categorize, oai_id, metadataTopic, metadata)

def not_in_aleph(oai_ids, digitoolXML, categorize):
    records = aleph.openAleph("dtl_2006.xml")
    for oai_id in oai_ids:
        metadata = digitoolXML.get_metadata(oai_id)['marc']
        aleph_id = aleph.normalise(metadata['001'])
        if aleph_id not in records.keys():
            categorize.categorize_item(oai_id,"id {} neni v aleph exportu".format(aleph_id))
