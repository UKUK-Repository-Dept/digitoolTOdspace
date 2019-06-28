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
            'author': ['vypracovala','vypracoval',''],
            'advisor': ['vedoucí práce','vedoucí diplomové práce','ved. dipl. práce','ved. práce','vedoucí bakalářské práce',' škol. rig. práce','vedoucí dipl. práce','ved. bakal. práce','školitel práce','vedoucí diplomove práce','školitel disertační práce','kolitel rigorózní práce','Vedoucí diplomové práce','škol. disert. práce','vedoucí rigorózní práce','vedocí diplomové práce','ved. diplomové práce','vedouí diplomové práce' 'vedoucí diplomové vedoucí', 'vedoucí [práce]', 'vedúci práce', 'Ved. práce', 'školitel rig. práce', 'vedoucí diplomové', 'vedpoucí diplomové práce', 'ved. rigorózní práce', 'vedoucí siplomové práce', 'ved. dipl. práce Radvan Bahbouh', 'školitel ', ],
            'committe': ['oponent'],
            'consultant': ['konzultant','konzultanti','konzult.']
    }

def __splitCreator(source, rules):
    res = {}
    c = source.split(';')
    for creator, tags in rules.items():
        if len(c) == 0:
            break
        for tag in tags:
            if tag in c[0]:
                res[creator] = c[0].replace(tag, '').strip()
                c = c[1:]
                break
    return res, c

def convertTag245(tag245, oai_id, categorize):

    res = {}
    c = []

    if len(tag245['a']) == 1:
        title = tag245['a'][0]
        res['title'] = __deleteBackslash(title)
    if 'b' in tag245.keys():
        alternative = tag245['b'][0]
        res['alternative'] = __deleteBackslash(alternative)
    if 'c' in tag245.keys():
        creator = tag245['c'][0]
        res1, c = __splitCreator(creator, rules)
        res.update(res1)
    if 'p' in tag245.keys():
        alternative = tag245['p'][0]
    for key in tag245.keys():
        if not key in 'abchpn':
            raise Exception('Unknown key')
    

    d = [
        ('title','[diplomová práce]'),
        ('title','[rigorózní práce]'),
        ('alternative','[diplomová práce]'),
            ]
    for creator, delete in d:
        if creator in res:
            if delete in res[creator]:
                res[creator] = res[creator].replace(delete, '').strip()
   
    res = { k:v for k,v in res.items() if v != '' }
    for key, value in res.items():
        if value[0] == '[' and value[-1] == ']':
            res[key] = value[1:-1]

    return res, c
