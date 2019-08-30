import catalogue

def getFaculty(department):
    for faculty in catalogue.faculty.keys():
        if department in catalogue.faculty[faculty]:
            return faculty

def surnameFirst(name):
    s = name.split()
    if len(s) == 2:
        return s[1]+', '+s[0]
    else: 
        return name

def convertOrigin(origin, oai_id, categorize):
    ret = {}
    origin = origin.strip()
    if "Univerzita Karlova. " == origin[:20]:
        origin = origin[20:]
    if '.' in origin:
        faculty, department = origin.split(".",1)
    else:
        faculty, department = origin, None
    if faculty in catalogue.faculty:
        ret['faculty'] = faculty
    else:
        pass #TODO
        #categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
        return ret #jinak by se katedra psychologie v plzni mohla smotat s tou pražskou, raději ať to zařve
    if department:
        if department in catalogue.faculty[faculty]:
            ret['department'] = department
        else:
            pass # TODO
            #categorize.categorize_item(oai_id,"Unknown department {}".format(department))
    return ret

