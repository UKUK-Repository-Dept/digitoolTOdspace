import catalogue 

def convertTag710(tag710,oai_id,categorize):
    ret = {}
    if 'a' in tag710.keys(): #univerzita nebo fakulta
        if len(tag710['a']) > 1:
            assert 'Jabok' in tag710['a'][1]
            tag710['a'] = tag710['a'][:1]
            #kašlu na Jabok
            #categorize.categorize_item(oai_id,"710: More than one university {}".format(tag710['a']))
        faculty = tag710['a'][0].replace('.','')
        if faculty[:18] == 'Univerzita Karlova':
            faculty = faculty[18:]
        if faculty not in  ['','.']:
            if faculty in catalogue.faculty.keys():
                ret['faculty'] = faculty
            else:
                #print(oai_id,tag710) TODO samazat tu práci
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
            faculty = tag710['b'][0]
            if faculty in catalogue.faculty.keys():
                ret['faculty'] = faculty
            else:
                department = faculty
                faculty = catalogue.getFaculty(department)
                if faculty:
                    ret['faculty'] = faculty
                    ret['department'] = department
                else:
                    pass #TODO ta plzeň
                    #print(oai_id,tag710)
        elif len(tag710['b']) == 2:
            faculty = tag710['b'][0].replace('.','')
            department = tag710['b'][1]
            if faculty in catalogue.faculty.keys():
                ret['faculty'] = faculty
            elif faculty in catalogue.institutToFaculty.keys():
                insitut = faculty
                faculty = catalogue.institutToFaculty[faculty]
                ret['faculty'] = faculty
                ret['department'] = insitut
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
    if ret == {}:
        err_msg = "710: No faculty found in "+str(tag710)
        categorize.categorize_item(oai_id,err_msg)
    return ret
