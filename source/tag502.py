import catalogue 

def convertOrigin(origin, oai_id, categorize):
    ret = {}
    origin = origin.strip()
    if "Univerzita Karlova. " == origin[:20]:
        origin = origin[20:]
    if '.' in origin:
        faculty, department = origin.split(".",1)
    else:
        faculty, department = origin, None
    if faculty in catalogue.faculty:
        ret['faculty'] = faculty
    else:
        categorize.categorize_item(oai_id,"Unknown faculty {}".format(faculty))
    if department:
        department = department.strip()
        if department in catalogue.department:
            ret['department'] = department
        else:
            categorize.categorize_item(oai_id,"Unknown department {}".format(department))
    return ret

def convertCorrectTag502(tag502, oai_id, categorize):
    ret = {}
    itemClass, origin = tag502.split("--")
    itemClass = itemClass.strip()
    if not '(' in itemClass:
        categorize.categorize_item(oai_id,"No academic title in  {}".format(itemClass))
        return ret
    level, name = itemClass.split('(')
    level = level.strip()
    if not level in catalogue.levelToTitle.keys():
        raise Exception("Unknown thesis level {}".format(level))
    else:
        ret['degree'] = level
    name = name[:-1].strip()
    if not name in catalogue.levelToTitle[level]:
        categorize.categorize_item(oai_id,"Degree '{}' has not title '{}'".format(level,name))
    else:
        ret['degreeTitle'] = name
    origin, year = origin.split(",")
    year = year.strip()
    assert 1919 < int(year) < 2019
    ret['year'] = year
    ret['university'] = 'Univerzita Karlova'
    ret = { **ret, **convertOrigin(origin, oai_id, categorize) }
    return ret 

originConvert = {
        '.': ['. .'],
        '. F': ['.F'],
        'fakulta.': ['fakulta,', 'fakzulta.,','práce.'],
        'Katedra': [ 'Kateda', 'katedra', 'Katerdra', 'Katerda', ],
        'Dizert': ['Disert'],
        'Univerzita Karlova.': [ 'Univerzita .', 'Uverzita Karlova', 'Univerzita karlova.', 
            'Univerzita Karlova,', 'Univerzita Karlova v Praze.', 'Univerzita Karlova. Univerzita Karlova.'],




        'Dizertační práce': ['Dizertace', 'Disetační práce', 'Dizertáční práce'],
        ' lékařská': ['. lékařská'], #odstraňuju tečky z lekařských fakult abych mohla parsovat #TODO vrátit
        'teologická': ['telogická', 'teologická'],
        'Filozofická': ['Filozofikcá', 'Filozofciká', 'Filozoficka', 'Filozofivká', 'Fiolozofická',],
        'psychologie': ['psyvhologie', 'psychlogie', 'pésychologie', 'psychologie', ],
        }

titleConvert = {
        '(Bc.)': ['(Bc..)'], 
        '(Mgr.)': ['(Mgr)', '( Mgr)', '(Mgr,)', '(Mgr,.)', '(Mgr..)', '(Mgt.)', '(mgr.)',],
        '(PhD.)': ['(Phd.)'],
        '(PhDr.)': ['(Phdr.)'],
        }

def convertTag502(tag502, oai_id, categorize):

    tag502 = tag502['a']
    if oai_id in ['81829', '62940', '17196', '81846' ]:
        error_msg = "Práce je zároveň diplomová a rigorozní {}".format(tag502)
        categorize.categorize_item(oai_id,error_msg)
        return
    elif len(tag502) > 1:
        if len(tag502[0]) > len(tag502[1]): #ručně ověřeno že to kratší je zbytečný bordel
            tag = tag502[0]
        else:
            tag = tag502[1]
 
    tag = tag502[0].strip()

    if not "--" in tag:
        for slash in ['-', '—', '–']:
            tag = tag.replace(slash,'--')

    if not "--" in tag:
        categorize.categorize_item(oai_id, "Not valid 502 tag {}".format(tag) )
        return {}
    
    tag = tag.replace('Univerzita Karlova. Katedra psychologie','Univerzita Karlova. Filozofikcá fakulta. Katedra psychologie',1)
    tag = tag.replace('Univerzita Karlova. Katedra věd o zemích Asie a Afriky','Univerzita Karlova. Filozofikcá fakulta. Katedra věd o zemích Asie a Afriky',1)
    tag = tag.replace('Univerzita Karlova. Katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
    tag = tag.replace('Univerzita Karlova. katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
    tag = tag.replace('Univerzita Karlova. Institut mezinárodních studií','Univerzita Karlova. Fakulta sociálních věd. Institut mezinárodních studií',1)
    tag = tag.replace('1996.', '1996')
    tag = tag.replace('[1922]', '1922')
    for correct, wrongs in originConvert.items():
        for wrong in wrongs:
            tag = tag.replace(wrong, correct)
    for correct, wrongs in titleConvert.items():
        for wrong in wrongs:
            tag = tag.replace(wrong, correct)

    if not ( tag[-4:].isdigit() and tag [-5] in [' ',','] ):
        error_msg = "Not valid year {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        return

    fixBeforeYear = {'. ':', ','a.': 'a, ','a ':'a, ','e ':'e, ',',,':', '}
    if tag[-6:-4] in fixBeforeYear.keys():
        tag = tag[:-6] + fixBeforeYear[tag[-6:-4]] + tag[-4:]

    return convertCorrectTag502(tag, oai_id, categorize)
