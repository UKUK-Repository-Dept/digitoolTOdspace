import catalogue 

def convertCorrectTag502(tag502, oai_id):
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
    
    origin = origin.strip()
    if "Univerzita Karlova. " == origin[:20]:
        origin = origin[20:]
    faculty, department = None, None
    if origin[1] == '.': #lékařské fakulty 1/2
        origin = origin[0] + '$' + origin[2:]
    if '.' in origin:
        faculty, department = origin.split(".",1)
    else:
        faculty, department = origin, None
    if '$' in faculty: #lékařské fakluty 2/2
        faculty = faculty.replace('$','.')
    if faculty in catalogue.faculty:
        ret['faculty'] = faculty
    else:
        #print(faculty, tag502)
        #categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
        return ret
    if department:
        department = department.strip()
        if department in catalogue.faculty[faculty]:
            ret['department'] = department
        else:
            pass 
            #print("{} '{}' '{}'".format(oai_id,faculty, department))
            #categorize.categorize_item(oai_id,"Unknown department {}".format(department))
    return ret 

def convertTag502(tag502, oai_id):
    ret = {}
    tag502 = tag502['a']
    if len(tag502) > 1:
        categorize.categorize_item(oai_id,"502: More than one tag 502")
        return ret
 
    tag = tag502[0].strip()

    if not "--" in tag:
        categorize.categorize_item(oai_id,"502: No -- split.")
        return ret
    
    return convertCorrectTag502(tag, oai_id)
