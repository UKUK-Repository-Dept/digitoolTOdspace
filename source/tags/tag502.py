import catalogue 
from tags.commonTag import convertOrigin

def convertCorrectTag502(tag502, oai_id, categorize):
    ret = {}
    itemClass, origin = tag502.split("--")
    itemClass = itemClass.strip()
    if not '(' in itemClass:
        categorize.categorize_item(oai_id,"502: No academic title in  {}".format(itemClass))
        return ret
    level, name = itemClass.split('(')
    level = level.strip()
    if not level in catalogue.levelToTitle.keys():
        categorize.categorize_item(oai_id,"502: Unknown thesis level {}".format(level))
        return ret
    else:
        ret['degree'] = level
    name = name[:-1].strip()
    if not name in catalogue.levelToTitle[level]:
        categorize.categorize_item(oai_id,"502: Degree '{}' has no title '{}'".format(level,name))
    else:
        ret['degreeTitle'] = name
    if origin.count(',') != 1:
        categorize.categorize_item(oai_id,"502: {}x ',' in '{}'".format(origin.count(','),tag502))
        return ret
    origin, year = origin.split(",")
    year = year.strip()
    assert 190 < int(year[:3]) < 202, year
    ret['year'] = year
    ret['university'] = 'Univerzita Karlova'
    ret = { **ret, **convertOrigin(origin, oai_id, categorize) }
    return ret 

def convertTag502(tag502, oai_id, categorize):
    ret = {}
    tag502 = tag502['a']
    if len(tag502) > 1:
        categorize.categorize_item(oai_id,"502: More than one tag 502")
        return ret
 
    tag = tag502[0].strip()

    if not "--" in tag:
        categorize.categorize_item(oai_id,"502: No -- split.")
        return ret
    
    return convertCorrectTag502(tag, oai_id, categorize)
