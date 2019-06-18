from filenameConvertor import FilenameConvertor
from metadataConvertor import MetadataConvertor

def oai(digitool, digitoolXML, categorize, skip=False): #categorieze whole oai
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        categorize.categorize_item(oai_id,"je v oai")

def forgot_attachements(digitool, digitoolXML, categorize, xml_attachements_list):
    attachements = []
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        attachements += list(digitoolXML.get_attachements(oai_id))
    for row in open(xml_attachements_list,"r"):
        if not row[:-1] in attachements:
            oai_id = row.split("_")[0]
            categorize.categorize_item(oai_id,"opomenuty soubor {} - bez metadat".format(oai_id))

def no_attachements(digitool, digitoolXML, categorize):
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        attachements = list(digitoolXML.get_attachements(oai_id))
        if len(attachements) == 0:
            categorize.categorize_item(oai_id,"bez přílohy")

def weird_attachements(digitool, digitoolXML, categorize):
    convertor = FilenameConvertor(categorize)
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        attachements = list(digitoolXML.get_attachements(oai_id,full=True))
        if len(attachements) == 0:
            continue
        descriptions = convertor.generate_description(attachements)
        if isinstance(descriptions, list):
            continue
        print(descriptions)

def preview(digitool, digitoolXMLnoskip, digitoolXMLall):
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        try:
            attachements = list(digitoolXMLnoskip.get_attachements(oai_id))
        except Exception as e:
            oai_id = str(e).split('/')[-1].split('.')[0]
            try:
                attachements = list(digitoolXMLall.get_attachements(oai_id))
                if len(attachements) == 1 and 'thumbnail' in attachements[0]:
                    print(oai_id, end = ", ")
                #digitoolXMLall.is_preview(oai_id)
            except:
                pass #TODO

def unknown_type(digitool, digitoolXML, categorize):
    convertor = MetadataConvertor(categorize)
    for record in digitool.list:
        originalMetadata = digitool.get_metadata(record)
        attachements = list(digitoolXML.get_attachements(oai_id,full=True))
        #TODO třizeni typu do metada i filename convertoru

