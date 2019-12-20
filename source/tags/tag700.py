
def convertTag700(tag700, oai_id):
    if not 'a' in tag700.keys() or not '4' in tag700.keys():
        return {} #je to jen doplňková informace
    assert 'a' in tag700.keys() and '4' in tag700.keys()
    persons = tag700['a']
    roles = tag700['4']
    while len(persons) > len(roles):
        roles.append('aut')
    assert len(persons) == len(roles)
    ret = {}
    for i in range(len(persons)):
        if roles[i] == 'aut':
            ret['author'] = [persons[i]]
        elif roles[i] == 'edt':
            ret['editor'] = [persons[i]]
        elif roles[i] == 'oth':
            ret['other'] = persons[i]
        else:
            raise Exception('Unknown role')
    return ret
