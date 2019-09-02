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
        return
    else:
        ret['degree'] = level
    name = name[:-1].strip()
    if not name in catalogue.levelToTitle[level]:
        categorize.categorize_item(oai_id,"502: Degree '{}' has no title '{}'".format(level,name))
    else:
        ret['degreeTitle'] = name
    if origin.count(',') != 1:
        categorize.categorize_item(oai_id,"502: {}x ',' in '{}'".format(origin.count(','),tag502))
        return
    origin, year = origin.split(",")
    year = year.strip()
    assert 1919 < int(year) < 2019
    ret['year'] = year
    ret['university'] = 'Univerzita Karlova'
    ret = { **ret, **convertOrigin(origin, oai_id, categorize) }
    return ret 

def convertTag502(tag502, oai_id, categorize):
    #print(tag502)
    tag502 = tag502['a']
    if len(tag502) > 1:
        categorize.categorize_item(oai_id,"More than one tag 502")
        return
 
    tag = tag502[0].strip()

    if not "--" in tag:
        categorize.categorize_item(oai_id,"502: No -- split.")
        return
    
    if not ( tag[-4:].isdigit() and tag [-5] in [' ',','] ):
        error_msg = "502: Not valid year in {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        return

    return convertCorrectTag502(tag, oai_id, categorize)