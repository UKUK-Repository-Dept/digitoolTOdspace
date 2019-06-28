
def __sortTags(tag245, oai_id):
    title, alternative, creator = '','',''
    if oai_id == '74132':
        title = tag245[0]
        creator = tag245[3]
    elif len(tag245) == 2:
        title = tag245[0]
        creator = tag245[1]
    elif len(tag245) == 3:
        if tag245[1] in ['[rukopis] /','[rukopis] :']:
            title = tag245[0]
            creator = tag245[2]
        elif tag245[0] == '[rukopis] /':
            title = tag245[1]
            creator = tag245[2]
        elif tag245[2] == '[rukopis] /':
            title = tag245[0]
            creator = tag245[1]
        else:
            title = tag245[0]
            alternative = tag245[1]
            creator = tag245[2]
    elif len(tag245) == 4:
        if tag245[1] in ['[rukopis] :','1,','[rukopis] ;','[rukopis] /']:
            title = tag245[0]
            alternative = tag245[2]
            creator = tag245[3]
        elif tag245[2] in ['[rukopis] :','[rukopis] /']:
            title = tag245[0]
            alternative = tag245[1]
            creator = tag245[3]
    else:
        raise Exception()
    return title, alternative, creator

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

def convertRealTag245(tag245, oai_id, categorize):

    title, alternative, creator = __sortTags(tag245, oai_id)

    res = {}
    res['title'] = __deleteBackslash(title)
    if alternative != '':
        res['alternative'] = __deleteBackslash(alternative)

    c = creator.split(';')
    creators = {
            'author': ['vypracovala','vypracoval',''],
            'advisor': ['vedoucí práce','vedoucí diplomové práce','ved. dipl. práce','ved. práce','vedoucí bakalářské práce',' škol. rig. práce','vedoucí dipl. práce','ved. bakal. práce','školitel práce','vedoucí diplomove práce','školitel disertační práce','kolitel rigorózní práce','Vedoucí diplomové práce','škol. disert. práce','vedoucí rigorózní práce','vedocí diplomové práce','ved. diplomové práce','vedouí diplomové práce' 'vedoucí diplomové vedoucí', 'vedoucí [práce]', 'vedúci práce', 'Ved. práce', 'školitel rig. práce', 'vedoucí diplomové', 'vedpoucí diplomové práce', 'ved. rigorózní práce', 'vedoucí siplomové práce', 'ved. dipl. práce Radvan Bahbouh', 'školitel ', ],
            'committe': ['oponent'],
            'consultant': ['konzultant','konzultanti','konzult.']
    }

    for creator, tags in creators.items():
        if len(c) == 0:
            break
        for tag in tags:
            if tag in c[0]:
                res[creator] = c[0].replace(tag, '').strip()
                c = c[1:]
                break

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
