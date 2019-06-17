
def oai(digitool, digitoolXML, categorize, skip=False): #categorieze whole oai
    digitool.download_list()
    attachements = []
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        categorize.categorize_item(oai_id,"je v oai",skip=skip)

def forgot_attachements(digitool, digitoolXML, categorize, xml_attachements_list):
    digitool.download_list()
    attachements = []
    for record in digitool.list:
        oai_id = digitool.get_oai_id(record)
        attachements += list(digitoolXML.get_attachements(str(oai_id)+".xml"))
    for row in open(xml_attachements_list,"r"):
        if not row[:-1] in attachements:
            oai_id = row.split("_")[0]
            categorize.categorize_item(oai_id,"opomenuty soubor")
