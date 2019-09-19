import re

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
    if ';' not in source and (':' in source or ',' in source):
        source = source.replace(':',';').replace(',',';')
    if not ';' in source:
        #return {'author': source}
        return {'tip': [source]}
    else:
        author, others = source.split(';',1)
        #ret =  {'author': author}
        ret =  {'tip': [author]}
        if 'Univer' in source:
            return ret #kašlem na to
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
                done = False
                for name in rules[role]:
                    if not done and re.match(name,person.lower()):
                        span = re.match(name,person.lower()).span()
                        assert span[0] == 0
                        personName = person[span[1]:].strip()
                        #ret[role].append(personName)
                        ret['tip'].append(personName)
                        done = True
        return ret

delete = [
        '; vedoucí práce Jiří Odehnal',
        ' : disertační práce z oboru Starého zákona /',
        ' : disertační práce /',
        ' diplomová práce /',
        ' : bakalářská práce /',
        ' bakalářská práce /',
        ' /',
        ]

def convertTag245(tag245, oai_id, categorize):
    ret = {}

    #title
    assert 'a' in tag245
    assert len(tag245['a']) == 1
    if not 'b' in tag245:
        title = tag245['a'][0].strip()
    else:
        assert len(tag245['b']) == 1
        title = tag245['a'][0].strip() + ' ' + tag245['b'][0].strip()
    for d in delete:
        if d in title:
            title = title.replace(d,'')
    title = title.replace('\\','').replace('/','')
    ret['title'] = title

    #author
    if 'c' in tag245:
        assert len(tag245['c']) == 1
        ret.update(__splitPeople(oai_id,tag245['c'][0]))
    else:
        pass #autor tady je jen bonusový
    
    for key in tag245.keys():
        if not key in 'abchnp6':
            raise Exception('Unknown key {}',format(key))
    return ret
