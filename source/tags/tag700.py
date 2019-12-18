
def convertTag700(tag700, oai_id, categorize):
    if not 'a' in tag700.keys() or not '4' in tag700.keys():
        return {} #je to jen doplňková informace
    assert 'a' in tag700.keys() and '4' in tag700.keys()
    persons = tag700['a']
    roles = tag700['4']
    #assert len(persons) == len(roles)
    if len(persons) != len(roles):
        #print(oai_id, persons, roles)
        #TODO
        return {}
    ret = {}
    for i in range(len(persons)):
        if roles[i] == 'ths':
            ret['advisor'] = persons[i]
        elif roles[i] in ['csl','sad']:
            ret['consultant'] = persons[i]
        elif roles[i] == 'opn':
            ret['commitee']=persons[i]
        else:
            #TODO projet ostatni
            pass #neřeším others a dalšich pár
    return ret
