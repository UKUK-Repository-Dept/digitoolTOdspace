
#def convertCorrectTag245(tag245, oai_id, categorize):
#    pass

def convertRealTag245(tag245, oai_id, categorize):
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

    if title[-1] == '/':
        if '/' in title[:-1]:
            if not ' /' in title[:-1]:
                title = title[:-1]
        else:
            title = title[:-1]
    
    if title[-1] == '/':
        if '/' in title[:-1]:
            if not ' /' in title[:-1]:
                title = title[:-1]
        else:
            title = title[:-1]

    if alternative[:-1] == '/':
        alternative = alternative[:-1]

    c = creator.split(';')
    author = c[0].strip()
    if ',' in author or ':' in author or '/' in author:
        categorize.categorize_item(oai_id,"tag 245c syntax")
        return
    if 'vypracovala' in author:
        author = author[12:]
    if 'vypracoval' in author:
        author = author[11:]

    c = c[1:]
    if len(c) == 0:
        return (title, alternative,author)
    if 'Univ' in c[0]:
        c = c[1:]

    
    comitte = ['vedoucí práce','vedoucí diplomové práce','ved. dipl. práce','ved. práce','vedoucí bakalářské práce',' škol. rig. práce','vedoucí dipl. práce','ved. bakal. práce','školitel práce','vedoucí diplomove práce','školitel disertační práce','kolitel rigorózní práce','Vedoucí diplomové práce','škol. disert. práce','vedoucí rigorózní práce','vedocí diplomové práce','ved. diplomové práce','vedouí diplomové práce']
    if len(c) == 0:
        return (title, alternative,author)
    for tag in comitte:
        if tag in c[0]:
            comitte = c[0]
            comitte = comitte.replace(tag, '')
            comitte = comitte.strip()
            c = c[1:]
            break
    
    comitte = ['oponent']
    if len(c) == 0:
        return (title, alternative,author)
    for tag in comitte:
        if tag in c[0]:
            comitte = c[0]
            comitte = comitte.replace(tag, '')
            comitte = comitte.strip()
            c = c[1:]
            break

    if len(c) == 0:
        return (title, alternative,author)
    
    comitte = ['konzultant','konzultanti']
    if len(c) == 0:
        return (title, alternative,author)
    for tag in comitte:
        if tag in c[0]:
            comitte = c[0]
            comitte = comitte.replace(tag, '')
            comitte = comitte.strip()
            c = c[1:]
            break

    if len(c) == 0:
        return (title, alternative,author)


    print(c)
