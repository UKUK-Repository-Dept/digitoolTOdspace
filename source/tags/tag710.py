import catalogue 
from tags import commonTag

def convertTag710(tag710,oai_id,categorize):
    ret = {}
    if 'a' in tag710.keys(): #univerzita nebo fakulta
        if len(tag710['a']) > 1:
            categorize.categorize_item(oai_id,"710: More than one university {}".format(tag710['a']))
            return ret
        faculty = tag710['a'][0].replace('.','')
        if faculty[:18] == 'Univerzita Karlova':
            faculty = faculty[18:]
        if faculty not in  ['','.']:
            if faculty in catalogue.faculty.keys():
                ret['faculty'] = faculty
            else:
                categorize.categorize_item(oai_id,"710: Unknown faculty {}".format(faculty))
                return ret
    if 'b' in tag710.keys():
        if faculty:
            assert len(tag710['b']) == 1
            department = tag710['b'][0]
            if department in catalogue.faculty[faculty]:
                ret['department'] = department
            else:
                err_msg = "710: Unknown departemnt {} at faculty {}".format(department, faculty)
                categorize.categorize_item(oai_id,err_msg)
        elif len(tag710['b']) == 1:
            pass
            #faculty = tag710['b'][0]
            #assert faculty in catalogue.faculty.keys(), faculty
            #ret['faculty'] = faculty
        elif len(tag710['b']) == 2:
            faculty = tag710['b'][0].replace('.','')
            department = tag710['b'][1]
            if faculty in catalogue.faculty.keys():
                ret['faculty'] = faculty
            else:
                categorize.categorize_item(oai_id,"710: Unknown faculty {}".format(faculty))
                return ret
            if department in catalogue.faculty[faculty]:
                ret['department'] = department
            else:
                err_msg = "710: Unknown department '{}' at faculty '{}'".format(department, faculty)
                categorize.categorize_item(oai_id,err_msg)
        else:
            raise Exception('710 new type')
    for key in tag710.keys():
        if not key in 'ab47':
            raise Exception("Unkown key")
    return ret
