def __deleteBackslash(title):
    title = title.strip()
    if title[:2] == '/ ':
        title = title[2:]
    if title[-1] == '/':
        if '/' in title[:-1]:
            if not ' /' in title[:-1]:
                title = title[:-1]
        else:
            title = title[:-1]
    return title.strip()

rules = {
            'author': ['vypracovala','vypracoval'],
            'advisor': [ 
                'supervisor', 'ved. dipl. prác', 'školitel', 'vedúci', 'ved. dipl. prcáe',
                'ved. dipl. p.', 'ved. dipl.', 'vedoucí diplomové práve', 'vedoucí diplomové',
                'vedoucí diplomové vedoucí', 'vedoucí' ],
            'committe': ['oponent práce', 'oponent','commitee'],
            'consultant': ['konzultantka práce', 'konzultanti ', 'konzult.','consultant',
                'konzultant práce','konzultant rigorózní práce', 'konzultant ',
                ]
    }

def __splitCreator(source, rules):
    res = {}
    for part in source.split(';'):
        creatorType = None
        if part == '':
            continue
        if 'Univ' in part:
            creatorType = 'origin'
            continue # fakultu tady ignoruju #TODO porovnat až budu mit nevylněné
        for creator, tags in rules.items():
            for tag in tags: # na pořadí if záleži
                if ('ved' in part or 'škol' in part or 'Ved' in part)  and 'áce' in part:
                    creatorType = 'advisor'
                    remove = part.split('áce')[0]+'áce'
                    break
                if tag in part:
                    creatorType = creator
                    remove = tag
                    break
                if part == source.split(';')[0]:
                    creatorType = 'author'
                    remove = ''
        if creatorType:
            res[creatorType] = part.replace(remove,'').strip()
        else:
            raise Exception('no Creator category')
    return res

def convertTag245(tag245, oai_id, categorize):

    res = {}
    
    if len(tag245['a']) == 1:
        title = tag245['a'][0]
        res['title'] = __deleteBackslash(title)
    if 'b' in tag245.keys():
        alternative = tag245['b'][0]
        res['alternative'] = __deleteBackslash(alternative)
    if 'c' in tag245.keys():
        creator = tag245['c'][0]
        res.update(__splitCreator(creator, rules))
    if 'p' in tag245.keys():
        alternative = tag245['p'][0]
    for key in tag245.keys():
        if not key in 'abchpn':
            raise Exception('Unknown key')
    

    d = [
        ('title','[diplomová práce]'),
        ('title','[rigorózní práce]'),
        ('title','[disertační práce]'),
        ('title','[1996]'),
        ('title',' -FF-'),
        ('alternative','[diplomová práce]'),
        ('alternative','[rigorózní práce]'),
        ('alternative',' -FF-'),
            ]
    for creator, delete in d:
        if creator in res:
            if delete in res[creator]:
                res[creator] = res[creator].replace(delete, '').strip()
   
    res = { k:v for k,v in res.items() if not v in ['','není uveden','neuveden'] }
    for key, value in res.items():
        if value[0] == ':':
            value = value[1:]
        if value[0] == '[':
            value = value[1:]
        if value[-1] == ']':
            value = value[:-1]
        res[key] = value

    if 'advisor' in res.keys() and ', konz' in res['advisor']:
        res['advisor'] = res['advisor'].split(',')[0]
    if 'author' in res.keys() and ',' in res['author']:
        if ', vedoucí ' in res['author']:
            res['author'] = res['author'].split(',')[0]
        else:
            #print(res['author']) #TODO co s rozenyma 
            pass
    for tag in ['title','alternative']:
        if tag in res.keys() and ';' in res[tag]:
            res[tag] = res[tag].split(';')[0]
    return res
