import catalogue 
import convert
from commonTag import convertOrigin

def convertCorrectTag502(tag502, oai_id, categorize):
    ret = {}
    itemClass, origin = tag502.split("--")
    itemClass = itemClass.strip()
    if not '(' in itemClass:
        categorize.categorize_item(oai_id,"No academic title in  {}".format(itemClass))
        return ret
    level, name = itemClass.split('(')
    level = level.strip()
    if not level in catalogue.levelToTitle.keys():
        raise Exception("Unknown thesis level {}".format(level))
    else:
        ret['degree'] = [level]
    name = name[:-1].strip()
    if not name in catalogue.levelToTitle[level]:
        categorize.categorize_item(oai_id,"Degree '{}' has not title '{}'".format(level,name))
    else:
        ret['degreeTitle'] = name
    origin, year = origin.split(",")
    year = year.strip()
    assert 1919 < int(year) < 2019
    ret['year'] = year
    ret['university'] = 'Univerzita Karlova'
    ret = { **ret, **convertOrigin(origin, oai_id, categorize) }
    return ret 

def convertTag502(tag502, oai_id, categorize):

    tag502 = tag502['a']
    if oai_id in ['81829', '62940', '17196', '81846' ]:
        error_msg = "Práce je zároveň diplomová a rigorozní {}".format(tag502)
        categorize.categorize_item(oai_id,error_msg)
        return
    elif len(tag502) > 1:
        if len(tag502[0]) > len(tag502[1]): #ručně ověřeno že to kratší je zbytečný bordel
            tag = tag502[0]
        else:
            tag = tag502[1]
 
    tag = tag502[0].strip()

    if not "--" in tag:
        for slash in ['-', '—', '–']:
            tag = tag.replace(slash,'--')

    if not "--" in tag:
        categorize.categorize_item(oai_id, "Not valid 502 tag {}".format(tag) )
        return {}
   
    tag = tag.replace('. .','.',1)
    tag = tag.replace('1996.', '1996')
    tag = tag.replace('[1922]', '1922')
    tag = tag.replace('fakulta,','fakulta.',1)
    tag = tag.replace('Karlova,','Karlova.',1)

    tag = tag.replace('Disert', 'Dizert')
    tag = tag.replace('Dizertace', 'Dizertační práce')
    tag = tag.replace('Disetační', 'Dizertační')
    tag = tag.replace('Dizertá', 'Dizerta')

    tag = tag.replace('Univerzita Karlova. Katedra psychologie','Univerzita Karlova. Filozofikcá fakulta. Katedra psychologie',1)
    tag = tag.replace('Univerzita Karlova. Katedra věd o zemích Asie a Afriky','Univerzita Karlova. Filozofikcá fakulta. Katedra věd o zemích Asie a Afriky',1)
    tag = tag.replace('Univerzita Karlova. Katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
    tag = tag.replace('Univerzita Karlova. katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
    tag = tag.replace('Univerzita Karlova. Institut mezinárodních studií','Univerzita Karlova. Fakulta sociálních věd. Institut mezinárodních studií',1)
    
    
    for correct, wrongs in convert.title.items():
        for wrong in wrongs:
            tag = tag.replace(wrong, correct)

    if not ( tag[-4:].isdigit() and tag [-5] in [' ',','] ):
        error_msg = "Not valid year {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        return

    fixBeforeYear = {'. ':', ','a.': 'a, ','a ':'a, ','e ':'e, ',',,':', '}
    if tag[-6:-4] in fixBeforeYear.keys():
        tag = tag[:-6] + fixBeforeYear[tag[-6:-4]] + tag[-4:]

    return convertCorrectTag502(tag, oai_id, categorize)
