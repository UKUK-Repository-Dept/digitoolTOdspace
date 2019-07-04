import catalogue, convert
import commonTag

university = [ 
    'Univerzita Karlova (Praha).',
    'Univerzita Karlova. (Praha)',
    'Univerzita Karlova.',
    'Univerzita Karlova .',
    'Univerzita Karlova,',
    'Univerzita Karlova',
    ]

def __filterUniversity(values):
    university = convert.origin['Univerzita Karlova.']
    ret = []
    for value in values:
        if not value in university:
            for tag in university:
                if tag in value:
                    ret.append(value.replace(tag,'').strip())
                    break
    return ret

def convertTag710(tag710,oai_id,categorize):
    ret = {}
    if 'a' in tag710.keys():
        a = __filterUniversity(tag710['a'])
        if a != []:
            assert len(a) == 1
            faculty, department = a[0].split('.')
            assert faculty in catalogue.faculty
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
                categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
        if 'departments' in locals():
            facultyTip = commonTag.getFaculty(departments[0])
            if facultyTip == None:
                pass #TODO cca deset nezařazených kateder 
            else:
                assert facultyTip == faculty
                for department in departments:
                    if not department in catalogue.faculty[facultyTip]:
                        raise Exception('Unknown department {}'.formant(department))
                ret['department'] = departments

    if '4' in tag710.keys():
        if not tag710['4'][0] in ['dgg','oth','ths']:
            pass #TODO 
    if '7' in tag710.keys():
        pass #TODO identifikace (kn20010710045, xx0010498)
    for key in tag710.keys():
        if not key in 'ab47':
            raise Exception("Unkown key")
