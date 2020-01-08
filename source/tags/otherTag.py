import catalogue

def convertTag242(tag242,oai_id):
    assert len(tag242.keys()) == 1
    title = tag242['a'][0]
    if '$' in title:
        shorter = {
                'Rozhodování, nejistota a mozek. Věda neuroekonomie, Paul W. Glimcher; The MIT Press, Cambridge, MA, USA, 2003, 375 stran, ISBN 0-262-07244-0 (hbk), $37.95': 'Rozhodování, nejistota a mozek',
                'Behaviorální teorie her, Colin F. Camerer, 2003, Russell Sage Foundation, New York, New York/Princeton University Press, Princeton, New Jersey, hardcover, 544 stran, ISBN: 0691090394, $65.00. Recenze knihy': 'Behaviorální teorie her',
                }
        title = shorter[title] 
        if '$' in title:
            raise Exception()

    return {'title_by_agency': title} 

def convertTagTYP(tagTYP,oai_id):
    assert len(tagTYP['a']) == 1
    return {'book_type': tagTYP['a'][0]} 

def convertTag001(tag001,oai_id):
    return {'aleph_id': tag001} 

def convertTag017(tag017,oai_id):
    assert len(tag017['a']) == 1
    return {'doi': tag017['a'][0]}

def convertTag022(tag022,oai_id):
    assert len(tag022['a']) == 1
    return {'issn': tag022['a'][0]}

def convertTag964(tag964,oai_id):
    return {'keywords': tag964['a']} 

def convertTag300(tag300,oai_id):
    if 'a' in tag300.keys():
        return {'pages': tag300['a'][0]} 
    return {}

def convertTag008(tag008,oai_id):
    lang = tag008[35:38]
    if lang not in catalogue.convertLang.keys():
        if lang == '---':
            return {} #ty tri maji vyplnenou 041
        else:
            raise Exception('Unknown language')
    return {'lang': catalogue.convertLang[lang]}

def convertTag526(tag526,oai_id):
    ret = {'discipline': tag526['a'][0] }
    if len(tag526['a']) > 1:
        ret['program'] = tag526['a'][1]
    return ret

def convertTag600(tag600,oai_id):
    if '2' in tag600:
        return {'czenas': tag600['a']} 
    else:
        return {'keywords': tag600['a']} 

def convertTag610(tag610,oai_id):
    if '2' in tag610:
        return {'czenas': tag610['a']} 
    else:
        return {'keywords': tag610['a']} 

def convertTag630(tag630,oai_id):
    return {'keywords': tag630['a']} 

def convertTag648(tag648,oai_id):
    if '2' in tag648:
        return {'czenas': tag648['a']} 
    return {'keywords': tag648['a']} 

def convertTag651(tag651,oai_id):
    if '2' in tag651:
        return {'czenas': tag651['a']} 
    return {'keywords': tag651['a']} 

