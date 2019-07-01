import catalogue 

def convertCorrectTag502(tag502, oai_id, categorize):
    itemClass, origin = tag502.split("--")
    itemClass = itemClass.strip()
    if not '(' in itemClass:
        error_msg = "No academic title in  {}".format(itemClass)
        categorize.categorize_item(oai_id,error_msg)
        return
    level, name = itemClass.split('(')
    level = level.strip()
    if not level in catalogue.levelToTitle.keys():
        raise Exception("Unknown thesis level {}".format(level))
    name = name[:-1].strip()
    if not name in catalogue.levelToTitle[level]:
        error_msg = "Degree '{}' has not title '{}'".format(level,name)
        categorize.categorize_item(oai_id,error_msg)
        return
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
    if not faculty in catalogue.faculty:
        error_msg = "Unknown faculty {}".format(faculty)
        categorize.categorize_item(oai_id,error_msg)
        return
    if department:
        department = department.strip()
        if not department in catalogue.department:
            error_msg = "Unknown department {}".format(department)
            categorize.categorize_item(oai_id,error_msg)
            return
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
        tag = tag.replace('-','--',1)
        tag = tag.replace('—','--',1)
        tag = tag.replace('–','--',1)
    if not "--" in tag:
        error_msg = "Not valid 502 tag {}".format(tag)
        categorize.categorize_item(oai_id,error_msg)
        return

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
        return

    fixBeforeYear = {'. ':', ','a.': 'a, ','a ':'a, ','e ':'e, ',',,':', '}
    if tag[-6:-4] in fixBeforeYear.keys():
        tag = tag[:-6] + fixBeforeYear[tag[-6:-4]] + tag[-4:]

    return convertCorrectTag502(tag, oai_id, categorize)
