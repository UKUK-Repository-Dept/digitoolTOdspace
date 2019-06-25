#TODO zkontrolovat výčty
thesisLevel = {
    "Diplomová práce":"TODO",
    "Bakalářská práce":"TODO",
    "Rigorózní práce":"TODO",
    "Habilitační práce":"TODO",
    "Dizertační práce":"Doktorský",
    }
levelToTitle = {
    "Diplomová práce": [ "Mgr.", ],
    "Bakalářská práce": [ "Bc.", ],
    "Rigorózní práce": [ "PhDr.", 'JUDr.', 'RNDr.', 'PharmDr.', 'MUDr.', "ThDr.", ],
    "Habilitační práce": [ "Doc.", ],
    "Dizertační práce": [ 'ThD.', "PhD.", ],
    }
thesisGrantorFaculty = {
    'Filozofická fakulta',
    'Filozoficko-historická fakulta',
    'Fakulta sociálních věd a publicistiky',
    'Fakulta sociálních věd',
    'Pedagogická fakulta',
    'Fakulta humanitních studií',
    'Husova evangelická bohoslovecká fakulta', #TODO vážně všechny tyhle Husovy?
    'Husova československá evangelická fakulta',
    'Husova československá evangelická fakulta bohoslovecká',
    'Husova československá evangelická bohoslovecká fakulta',
    'Komenského evangelická bohoslovecká fakulta',
    'Komenského bohoslovecká fakulta v Praze',
    'Evangelická teologická fakulta',
    'Matematicko-fyzikální fakulta',
    '1 lékařská fakulta',
    '2 lékařská fakulta',
    '3 lékařská fakulta',
    }
thesisGrantorDepartment = {
    'Katedra sociologie',
    'Katedra psychologie',
    'Katedra speciální pedagogiky',
    'Katedra marxisticko-leninskej filozofie',
    'Institut ekonomických studií',
    'Institut sociologických studií. Katedra sociologie',
    'Katedra výchovy a vzdělávání dospělých',
    'Katedra andragogiky a personálního řízení',
    'Katedra obecné antropologie',
    'Institut sociologických studií',
    'Katedra řízení a supervize v sociálních a zdravotnických organizacích',
    'Ústav informačních studií a knihovnictví',
    'Katedra filosofie',
    'Katedra psychofyziologie a klinické psychologie',
    'Katedra softwarového inženýrství',
    'Ústav filozofie a religionistiky',
    'Katedra nadragogiky a personálního řízení',
    'Katedra tělesné výchovy a sportu',
    'Katedra osvěty a výchovy dospělých',
    'Katedra pedagogiky',
    'Katedra Starého zákona',
    'Institut komunikačních studií a žurnalistiky',
    'Institut komunikačních studií a žurnalistiky. Katedra mediálních studií',
    'Katedra systematické teologie',
    'Katedra socioloogie',
    'Katedra věd o zemích Asie a Afriky',
    'Katedra elektronické kultury a sémiotiky',
    'Katedra teorie kultury',
    'Katedra biblických věd',
    'Katedra české literatury a literární vědy',
    'Katedra sociologie a filozofie',
    'Katedra sociální teologie',
    'Katedra církevních dějin',
    'Katedra marxisticko-leninské sociologie',
    'Katedra teorie kultury',
    'Institut mezinárodních studií. Katedra západoevropských studií',
    'Psychologický seminář',
    'Katedra výtvarné výchovy',
    'Katedra sociologie a filosofie',
    'Institut politologických studií',
    'Katedra marxisticko-leninské filosofie',
    'Katedra andragogika personálního řízení',
    'Katedra teoretické informatiky a matematické logiky',
    }

preconvert = {
    "81846": 'Diplomová & Rigorózní práce--Univerzita Karlova. Filozofická fakulta. Katedra psychologie, 2000',
    '74098': 'Diplomová práce (Mgr.)--Univerzita Karlova. Filozofická fakulta. Katedra sociologie, 1997',
    '98661': 'Bakalářská práce (Bc.)--Univerzita Karlova. 2. lékařská fakulta, 2004',
    '17196': 'Diplomová & Rigorózní práce--Univerzita Karlova. Matematicko-fyzikální fakulta, 2004',
    '62940': 'Diplomová & Rigorózní práce—Univerzita Karlova. Filozofická fakulta. Katedra psychologie,1998',
    '89739': 'Rigorózní práce (PhDr.)--Univerzita Karlova. Filozofická fakulta. Ústav informačních studií a knihovnictví, 2005',
    '81829': 'Diplomová & Rigorózní práce--Univerzita Karlova. Filozofická fakulta. Katedra psychologie, 1999'
    }

def convertCorrectTag502(tag502, oai_id, categorize):
    itemClass, origin = tag502.split("--")
    itemClass = itemClass.strip()
    if not '(' in itemClass:
        error_msg = "No academic title in  {}".format(itemClass)
        categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)
    level, name = itemClass.split('(')
    level = level.strip()
    if not level in thesisLevel.keys():
        raise Exception("Unknown thesis level {}".format(level))
    name = name[:-1].strip()
    if not name in levelToTitle[level]:
        error_msg = "Degree '{}' has not title '{}'".format(level,name)
        categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)
    origin, year = origin.split(",")
    year = year.strip()
    assert 1919 < int(year) < 2019
    origin = origin.strip()
    if "Univerzita Karlova. " == origin[:20]:
        origin = origin[20:]
    if '.' in origin:
        faculty, department = origin.split(".",1)
    else:
        faculty, department = origin, None
    if not faculty in thesisGrantorFaculty:
        error_msg = "Unknown faculty {}".format(faculty)
        categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)
    if department:
        department = department.strip()
        if not department in thesisGrantorDepartment:
            error_msg = "Unknown department {}".format(department)
            categorize.categorize_item(oai_id,error_msg)
            raise Exception(error_msg)
    return (level, name, 'Univerzita Karlova', faculty, department, year)


titleConvert = {
        '(Bc..)': '(Bc.)',
        '(Mgr)': '(Mgr.)',
        '( Mgr)': '(Mgr.)',
        '(Mgr,)': '(Mgr.)',
        '(Mgr,.)': '(Mgr.)',
        '(Mgr..)': '(Mgr.)',
        '(Mgt.)': '(Mgr.)',
        '(mgr.)': '(Mgr.)',
        '(Phd.)': '(PhD.)',
        '(Phdr.)': '(PhDr.)',
        }

def convertRealTag502(tag502, oai_id, categorize):

    if oai_id in ['81829', '62940', '17196', '81846' ]:
        error_msg = "Práce je zároveň diplomová a rigorozní {}".format(tag502)
        categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)
    if tag502 == []:
        error_msg = "No tag 502"
        #categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)
    elif len(tag502) > 1:
        if len(tag502[0]) > len(tag502[1]): #ručně ověřeno že to kratší je zbytečný bordel
            tag = tag502[0]
        else:
            tag = tag502[1]
    else:
        tag = tag502[0].strip()

    if not "--" in tag:
        tag = tag.replace('-','--',1)
        tag = tag.replace('—','--',1)
        tag = tag.replace('–','--',1)
    if not "--" in tag:
        error_msg = "Not valid 502 tag {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)

    tag = tag.replace('. .','.',1)
    tag = tag.replace('Univerzita .','Univerzita Karlova.',1)
    tag = tag.replace('Uverzita','Univerzita',1)
    tag = tag.replace('Univerzita karlova.','Univerzita Karlova.',1)
    tag = tag.replace('Univerzita Karlova,','Univerzita Karlova.',1)
    tag = tag.replace('Univerzita Karlova.F','Univerzita Karlova. F',1)
    tag = tag.replace('Univerzita Karlova v Praze.','Univerzita Karlova.',1)
    tag = tag.replace('Univerzita Karlova. Univerzita Karlova.','Univerzita Karlova.',1)
    tag = tag.replace('Univerzita Karlova. Katedra psychologie','Univerzita Karlova. Filozofikcá fakulta. Katedra psychologie',1)
    tag = tag.replace('Univerzita Karlova. Katedra věd o zemích Asie a Afriky','Univerzita Karlova. Filozofikcá fakulta. Katedra věd o zemích Asie a Afriky',1)
    tag = tag.replace('Univerzita Karlova. Katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
    tag = tag.replace('Univerzita Karlova. katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
    tag = tag.replace('Univerzita Karlova. Institut mezinárodních studií','Univerzita Karlova. Fakulta sociálních věd. Institut mezinárodních studií',1)
    tag = tag.replace('Filozofikcá','Filozofická',1)
    tag = tag.replace('Filozofciká','Filozofická',1)
    tag = tag.replace('Filozoficka','Filozofická',1)
    tag = tag.replace('Filozofivká','Filozofická',1)
    tag = tag.replace('Fiolozofická','Filozofická',1)
    tag = tag.replace('Filozofická práce','Filozofická fakulta',1)
    tag = tag.replace('telogická','teologická',1)
    tag = tag.replace('1. lékařská', '1 lékařská')
    tag = tag.replace('2. lékařská', '2 lékařská')
    tag = tag.replace('3. lékařská', '3 lékařská')
    tag = tag.replace('fakulta,','fakulta.',1)
    tag = tag.replace('fakzulta.','fakulta.',1)
    tag = tag.replace('Kateda','Katedra',1)
    tag = tag.replace('katedra','Katedra',1)
    tag = tag.replace('Katerdra','Katedra',1)
    tag = tag.replace('Katerda','Katedra',1)
    tag = tag.replace('psyvhologie','psychologie',1)
    tag = tag.replace('psychlogie','psychologie',1)
    tag = tag.replace('pésychologie','psychologie',1)
    tag = tag.replace('psychologie','psychologie',1)
    tag = tag.replace('Disert', 'Dizert')
    tag = tag.replace('Dizertace', 'Dizertační práce')
    tag = tag.replace('Disetační', 'Dizertační')
    tag = tag.replace('Dizertá', 'Dizerta')
    tag = tag.replace('fakulta. 1', 'fakulta. 1')
    tag = tag.replace('1996.', '1996')
    tag = tag.replace('[1922]', '1922')
    for wrong, correct in titleConvert.items():
        tag = tag.replace(wrong, correct)

    if not ( tag[-4:].isdigit() and tag [-5] in [' ',','] ):
        error_msg = "Not valid year {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        raise Exception(error_msg)

    fixBeforeYear = {'. ':', ','a.': 'a, ','a ':'a, ','e ':'e, ',',,':', '}
    if tag[-6:-4] in fixBeforeYear.keys():
        tag = tag[:-6] + fixBeforeYear[tag[-6:-4]] + tag[-4:]

    return convertCorrectTag502(tag, oai_id, categorize)
