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
#        categorize.categorize_item(oai_id,"Unknown thesis level {}".format(level))
        return
    else:
        ret['degree'] = [level]
    name = name[:-1].strip()
    if not name in catalogue.levelToTitle[level]:
        categorize.categorize_item(oai_id,"Degree '{}' has no title '{}'".format(level,name))
    else:
        ret['degreeTitle'] = name
    if origin.count(',') != 1:
        categorize.categorize_item(oai_id,"{}x ',' in {}".format(origin.count(','),tag502))
        return
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
    if len(tag502) > 1:
        categorize.categorize_item(oai_id,"More than one tag 502")
        return
 
    tag = tag502[0].strip()

    if not "--" in tag:
        categorize.categorize_item(oai_id,"No -- split.")
        return
    
    for correct, wrongs in convert.title.items():
        for wrong in wrongs:
            tag = tag.replace(wrong, correct)

    if not ( tag[-4:].isdigit() and tag [-5] in [' ',','] ):
        error_msg = "Not valid year in {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        return

    return convertCorrectTag502(tag, oai_id, categorize)
