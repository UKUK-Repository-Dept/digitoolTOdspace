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

def convertTag710(tag,oai_id,categorize):
    ret = {}
    if 'a' in tag.keys():
        a = __filterUniversity(tag['a'])
        if a != []:
            assert len(a) == 1
            faculty, department = a[0].split('.')
            assert faculty in catalogue.faculty
            ret['faculty'] = faculty
            if department != '':
                department = department.strip()
                assert department in catalogue.department
                ret['department'] = department
    if 'b' in tag.keys():
        origins = tag['b']
        faculty = 'Filozofická fakulta'
        departments = ['Katedra psychologie'] #TODO
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
            if faculty in catalogue.institutToFaculty.keys():
                departments = [faculty, commonTag.superStrip(origins[1])]
                faculty = catalogue.institutToFaculty[faculty]
            else:
                departments = [commonTag.superStrip(origins[1])]
                #TODO to dole jde stričit do catalogue + convert
            if len(departments) == 1 and departments[0] in ['Katedra psychologie', 'Katedra sociologie']:
                faculty = 'Filozofická fakulta'
            if len(departments) == 1 and departments[0] in ['Institute of Economic Studies']:
                faculty = 'Fakulta sociálních věd'
                department = 'Institut ekonomických studií'
        elif len(origins) == 1:
            origin = origins[0]
            for correct, wrongs in convert.origin.items():
                for wrong in wrongs:
                    origin = origin.replace(wrong, correct)
            if origin in catalogue.faculty:
                faculty = origin
            elif origin in catalogue.department:
                pass # print(origins) #TODO
            elif origins[0] in catalogue.department:
                pass # print(origins) #TODO
            else:
                pass # print(oai_id, origin) #TODO
        
        if 'faculty' in locals():
            # TODO categorize
            #if not faculty in catalogue.faculty:
            #    print(faculty, departments)
            ret['faculty'] = faculty
        if 'department' in locals():
            #for department in departments:
            #    if not department in catalogue.department:
            #        print(department)
            ret['department'] = departments

    if '4' in tag.keys():
        if not tag['4'][0] in ['dgg','oth','ths']:
            pass #TODO 
    if '7' in tag.keys():
        pass #TODO identifikace (kn20010710045, xx0010498)
    for key in tag.keys():
        if not key in 'ab47':
            print(key)
