import catalogue
def convertTag041(tag041,oai_id,categorize):
    ret = {}
    if 'a' in tag041.keys():
        lang = tag041['a'][0]
        ret['lang'] = catalogue.convertLang[lang]
    if 'b' in tag041.keys():
        #TODO konvertovat
        ret['alternative_lang'] = tag041['b']
    return ret
