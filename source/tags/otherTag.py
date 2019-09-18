import catalogue

def convertTag001(tag001,oai_id,categorize):
    return {'aleph_id': tag001} 

def convertTag008(tag008,oai_id,categorize):
    lang = tag008[35:38]
    return {'lang': catalogue.convertLang[lang]}

def convertTag526(tag526,oai_id,categorize):
    ret = {'discipline': tag526['a'][0] }
    if len(tag526['a']) > 1:
        ret['program'] = tag526['a'][1]
    return ret

def convertTag600(tag600,oai_id,categorize):
    return {'keywords': tag600['a']} 

def convertTag610(tag610,oai_id,categorize):
    return {'keywords': tag610['a']} 

def convertTag630(tag630,oai_id,categorize):
    return {'keywords': tag630['a']} 

def convertTag648(tag648,oai_id,categorize):
    return {'keywords': tag648['a']} 

def convertTag651(tag651,oai_id,categorize):
    return {'keywords': tag651['a']} 

