import  tags.commonTag
import re

#TODO špatně žere práce
rules = {
        'advisor': [
            'ved.*áce',
            'ved.*ace',
            'ško.*áce',
            'ved.*vedoucí',
            'vedoucí:',
            'vedoucí diplomové',
            'ved. dipl.',
            'ved. dipl. p.',
            'školitel',
            ],
        'commitee': [
            'op.*áce',
            'commitee',
            'oponent',
            ],
        'consultant': [
            'odborný konzultant',
            'kon.*áce',
            'konzultantka',
            'konzultanti',
            'konzult\.',
            'konzultant',
            ]
}

def __splitPeople(oai_id, source):
    if not ';' in source:
        if ':' in source or ',' in source:
            pass #TODO odstranit
        return {'author': source}
    else:
        author, others = source.split(';',1)
        ret =  {'author': author}
        if 'Univer' in source:
            return ret #TODO odstranit
        others.replace('[',' ')
        others.replace(']',' ')
        if ';' in others:
            others = others.split(';')
        else:
            others = [others]
        for person in others:
            if 'neuveden' in person:
                continue #Iry souhlasí
            if len(person) == 0:
                continue #zakončeni středníkem a nic dál
            person = person.replace('[','').replace(']','')
            if person[0] == ' ':
                person = person[1:]
            for role in rules.keys():
                for name in rules[role]:
                    if re.match(name,person.lower()):
                        span = re.match(name,person.lower()).span()
                        assert span[0] == 0
                        personName = person[span[1]:].strip()
                        ret[role] = personName
                        continue
        return ret

def convertTag245(tag245, oai_id, categorize):
    ret = {}

    #title
    assert 'a' in tag245
    assert len(tag245['a']) == 1
    if not 'b' in tag245:
        title = tag245['a'][0]
    else:
        assert len(tag245['b']) == 1
        title = tag245['a'][0] + ' ' + tag245['b'][0]
    #TODO '/' 'bakalářská práce'
    #print(oai_id, title)
    ret['title'] = title

    #author
    if 'c' in tag245:
        assert len(tag245['c']) == 1
        ret.update(__splitPeople(oai_id,tag245['c'][0]))
    else:
        pass #TODO
        #print(oai_id,'245: no author')
    
    for key in tag245.keys():
        if not key in 'abchnp6':
            raise Exception('Unknown key {}',format(key))
    return ret
