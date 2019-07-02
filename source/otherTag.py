import catalogue 

university = [ 
    'Univerzita Karlova (Praha).',
    'Univerzita Karlova. (Praha)',
    'Univerzita Karlova.',
    'Univerzita Karlova .',
    'Univerzita Karlova,',
    'Univerzita Karlova',
    ]

def __filterUniversity(values):
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
        #TODO ověřit že to v ret už není
        pass
        #if len(tag['b']) > 1:
        #    print(tag['b'])
    if '4' in tag.keys():
        if not tag['4'][0] in ['dgg','oth','ths']:
            pass #TODO 
    if '7' in tag.keys():
        pass #TODO identifikace (kn20010710045, xx0010498)
    for key in tag.keys():
        if not key in 'ab47':
            print(key)
