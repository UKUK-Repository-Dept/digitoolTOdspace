import catalogue
def convertTag041(tag041,oai_id,categorize):
    ret = {}
    lang = None
    if 'a' in tag041.keys():
        lang = tag041['a'][0]
        ret['lang'] = catalogue.convertLang[lang]
    if 'b' in tag041.keys():
        langs = []
        if lang and tag041['b'][0] == lang:
            tag041['b'] = tag041['b'][1:]
        for l in tag041['b']:
            if l in ['akh','hun']:
                continue #nejde smazat v digitoolu
            if l not in catalogue.convertLang.keys():
                #TODO kouknout kolik jich je a pak ignorovat?
                #print(oai_id, l)
                continue
                raise Exception('unknown language {}'.format(l))
            else:
                langs.append(catalogue.convertLang[l])
        assert len(langs) <= 1
        if len(langs) == 1:
            ret['alternative_lang'] = langs[0]
    return ret
