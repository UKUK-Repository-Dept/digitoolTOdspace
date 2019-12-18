import catalogue
def convertTag041(tag041,oai_id,categorize):
    ret = {}
    if 'a' in tag041.keys():
        lang = tag041['a'][0]
        ret['lang'] = catalogue.convertLang[lang]
    if 'b' in tag041.keys():
        langs = []
        for l in tag041['b']:
            if l not in catalogue.convertLang.keys():
                #TODO kouknout kolik jich je a pak ignorovat?
                #print(oai_id)
                continue
            else:
                langs.append(catalogue.convertLang[l])
        ret['alternative_lang'] = langs
    return ret
