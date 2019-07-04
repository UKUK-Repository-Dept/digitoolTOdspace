import catalogue, convert

def superStrip(word):
    #TODO / : , []
    while True:
        change = False
        if word != word.strip():
            word = word.strip()
            change = True
        if word == '':
            break
        if word[-1] == '.':
            word = word[:-1]
        if not change:
            break
    return word

def getFaculty(department):
    for faculty in catalogue.faculty.keys():
        if department in catalogue.faculty[faculty]:
            return faculty

def convertOrigin(origin, oai_id, categorize, tag502):
    for correct, wrongs in convert.origin.items():
        for wrong in wrongs:
            origin = origin.replace(wrong, correct)
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
        categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
        return ret #jinak by se katedra psychologie v plzni mohla smotat s tou pražskou, raději ať to zařve
    if department:
        department = department.strip()
        if department in catalogue.faculty[faculty]:
            ret['department'] = department
        else:
            categorize.categorize_item(oai_id,"Unknown department {}".format(department))
    return ret

