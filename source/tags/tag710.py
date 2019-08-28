import catalogue 
import convert
from tags import commonTag

def convertTag710(tag710,oai_id,categorize):
    ret = {}
    if 'a' in tag710.keys():
        #a = __filterUniversity(tag710['a'])
        
        a=0
        if tag710['a'][:31] == 'Univerzita Karlova. ':
            a = tag710['a'][31:i]
        else:
            a = tag710['a']
            pass # TODO print(tag710)
        if tag710['a'][:31] == 'Univerzita Karlova. ':
            pass
    return {}
'''        if a != []:
            assert len(a) == 1
            #faculty, department = a[0].split('.')
            #assert faculty in catalogue.faculty
            ret['faculty'] = faculty
            if department != '':
                department = department.strip()
                assert department in catalogue.faculty[faculty]
                ret['department'] = department
    if 'b' in tag710.keys():
        origins = tag710['b']
        for i in range(len(origins)):
            for correct, wrongs in convert.origin.items():
                for wrong in wrongs:
                    origins[i] = origins[i].replace(wrong, correct)
        if len(origins) > 4:
            raise Exception("Au")
        elif len(origins) == 4:
            faculty = commonTag.superStrip(origins[2])
            departments = [commonTag.superStrip(origins[3])]
        elif len(origins) == 3:
            faculty = commonTag.superStrip(origins[0])
            departments = [commonTag.superStrip(origins[1]),commonTag.superStrip(origins[2])]
        elif len(origins) == 2:
            faculty = commonTag.superStrip(origins[0])
            if faculty in catalogue.faculty.keys():
                pass
            elif faculty in catalogue.institutToFaculty.keys():
                departments = [faculty, commonTag.superStrip(origins[1])]
                faculty = catalogue.institutToFaculty[faculty]
            elif faculty in ['','F']:
                origins = origins[1:]
            else:
                categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
        if len(origins) == 1:
            origin = commonTag.superStrip(origins[0])
            facultyTip = commonTag.getFaculty(origin)
            if origin in catalogue.faculty:
                faculty = origin
            elif facultyTip in catalogue.faculty:
                faculty = facultyTip
                departments = [origin]
            else:
                departments = [origin]
        
        if 'faculty' in locals():
            if faculty in catalogue.faculty:
                ret['faculty'] = faculty
            else:
                pass #TODO
                #categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
        if 'departments' in locals():
            facultyTip = commonTag.getFaculty(departments[0])
            if facultyTip == None:
                pass #TODO cca deset nezařazených kateder 
            else:
                assert facultyTip == faculty, "{}, {}".format(facultyTip, faculty)
                for department in departments:
                    if not department in catalogue.faculty[facultyTip]:
                        raise Exception('Unknown department {}'.format(department))
                ret['department'] = departments

    for key in tag710.keys():
        if not key in 'ab47':
            raise Exception("Unkown key")
    return ret
'''
