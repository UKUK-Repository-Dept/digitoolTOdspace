import catalogue, convert

def superStrip(word):
    delete = ['.','/',':',',','[',']']
    while True:
        change = False
        if word != word.strip():
            word = word.strip()
            change = True
        word = word.strip()
        if word == '':
            break
        if word[-1] in delete:
            word = word[:-1]
            continue
        if word[0] in delete:
            word = word[1:]
            continue
        if not change:
            break
    return word


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
        department = superStrip(department)
        if department in catalogue.faculty[faculty]:
            ret['department'] = department
        else:
            categorize.categorize_item(oai_id,"Unknown department {}".format(department))
    return ret

