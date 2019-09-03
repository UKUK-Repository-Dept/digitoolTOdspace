import  tags.commonTag

rules = {
        'advisor': [
            'vedoucí práce',
            'vedoucí diplomové práce',
            'školitel práce',
            'vedoucí bakalářské práce',
            'vedoucí rigorózní práce',
            'ved. dipl. práce',
            'ved. práce',
            'škol. rig. práce',
            'ved. bakal. práce',
            'školitel disertační práce',
            'ved. bak. práce',



            #'vedoucí',
            #'školitel',
            ],
        'committe': [
            #'oponent',
            ],
        'consultant': [
            'konzultant rigorózní práce',
            'konzultant práce',
            #'konzultant',
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
                #print(oai_id, source)
                continue #TODO
            hui = False
            if person[0] == ' ':
                person = person[1:]
            for role in rules.keys():
                for name in rules[role]:
                    if name in person.lower():
                        #ret.setdefault(role, []).append('osoba TODO')
                        hui = True #TODO smazat
                        continue
            #TODO ten seznam je fakt dlouhý
            #if not hui:
            #    print(oai_id,person)
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
