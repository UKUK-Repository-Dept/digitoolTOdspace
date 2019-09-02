from filenameConvertor import FilenameConvertor
from metadataConvertor import Metadata
from categorize import Categorize
from tags.tag502 import convertTag502
from aleph import openAleph

def all_attachements(oai_ids, dtx, c):
    forgot_attachements(oai_ids,dtx,c)
    no_attachements(oai_ids,dtx,c)
    only_dc(oai_ids,dtx,c)

def oai(oai_ids, digitoolXML, categorize):
    for oai_id in oai_ids:
        categorize.categorize_item(oai_id,"je v oai")

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
        attachements += list(zip(*digitoolXML.get_attachements(oai_id)))[0]
    for row in open( digitoolXML.xml_dirname.split('/')[0]+"/ls_streams.txt" ,"r"):
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
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        m = Metadata(Categorize(digitoolXML,export='no'), oai_id)
        if 'marc' in originalMetadataXML.keys():
            m.convertMarc(originalMetadataXML['marc'])
            attachements = list(digitoolXML.get_attachements(oai_id))
            #TODO smazat
            if not m.degree:
                continue

            descriptions = convertor.generate_description(oai_id,attachements,m.degree)
        else:
            pass #TODO raise Exception('no marc')

def aleph(oai_ids, digitoolXML, categorize):
    records = openAleph("dtl_2006.xml")
    for metadata in records:
        digittol_id, aleph_id = None, None
        for tag in metadata.keys():
            if '856' in tag:
                digittol_id = metadata[tag]['u'][0].split('=')[-1]
            if '001' in tag:
                aleph_id = metadata[tag]
        oai_id = "{},{}".format(aleph_id,digittol_id)
        #oai_id = aleph_id
        m = Metadata(categorize, oai_id)
        m.convertMarc(metadata)

def not_in_aleph(oai_ids, digitoolXML, categorize):
    records = openAleph("dtl_2006.xml")
    for oai_id in oai_ids:
        originalMetadataXML = digitoolXML.get_metadata(oai_id)
        if not 'marc' in originalMetadataXML.keys():
            #categorize.categorize_item(oai_id,"no marc")
            continue
        #if not '001' in originalMetadataXML['marc']:
        #    print(originalMetadataXML['marc'])
