import re
from tags import * 
import catalogue

def comparePeople(name1,name2):
    def normaliseName(name):
        name = name.replace(':','').replace('.','. ')
        names = sorted(name.replace(',',' ').replace('-',' ').split())
        for name in names:
            if name in ['vypracoval', 'vypracovala', 'p.', 'autorka', 'autor:', 'roz.', 'a', 'prcáe', 'sociolog', 'prác', 'práve', 'by']:
                continue
            name = name.strip()
            yield name
    if name1 == None:
        return True
    name1 = list(normaliseName(name1))
    name2 = list(normaliseName(name2))
    if not len(name1) == len(name2):
       return False
    for i in range(len(name1)):
        if len(name1[i]) > len(name2[i]):
            first, second = name2[i], name1[i]
        else:
            first, second = name1[i], name2[i]
        if len(first) == 2 and first[1] in ['.',','] and first[0] == second[0]: 
            continue #iniciály
        if not first == second:
            return False
    return True


def getTopic(categorize, oai_id, topic, metadata):
    #v neshodě vrací to poslední, nikoliv autoritaivní 
    result1  = None
    tag1 = None
    for tag2 in metadata:
        if not topic in metadata[tag2].keys():
            continue
        result2 = metadata[tag2][topic]
        error_msg = 'Different {} {}:"{}" {}: "{}"'.format(topic, tag1, result1, tag2, result2)
        personTopics = ['author','advisor','commitee','consultant','editor']
        if topic in personTopics and not comparePeople(result1,result2):
            categorize.categorize_item(oai_id,error_msg)
        elif topic not in personTopics and result1 and result1 != result2:
            categorize.categorize_item(oai_id,error_msg)
        result1 = result2
        tag1 = tag2
    return result1

def sumTopic(categorize, oai_id, topic, metadata):
    result = []
    for tag2 in metadata:
        if not topic in metadata[tag2].keys():
            continue
        result = result + metadata[tag2][topic]
    if result != []:
        return result


def convertMarc(categorize, oai_id, metadataOrigin):
    metadata = {}
    mandatory = {
            '001': otherTag.convertTag001,#aleph_id
            '245': tag245.convertTag245, #titul, autor 
            #'502': tag502.convertTag502, #kvalifikační práce
            }
    obligatory = {
            '100': tag100.convertTag100, #autor
            '260': tag260.convertTag260, #místo vydání a datum 
            #'710': tag710.convertTag710, #fakulta, katedra
            '008': otherTag.convertTag008,#jazyk na pozici 35-37
            '041': tag041.convertTag041,  # jazyk 
            '246': tag246.convertTag246,  # titulek v překladu 
            #'520': tag520.convertTag520,  # abstrakt 
            #'526': otherTag.convertTag526,# obor a program
            #'600': otherTag.convertTag600,# keywords osoba
            #'610': otherTag.convertTag610,# keywords organizace
            #'630': otherTag.convertTag630,# keywords knihy
            #'648': otherTag.convertTag648,# keywords období
            #'650': tag650.convertTag650,  # keywords 
            #'651': otherTag.convertTag651,# keywords zeměpis
            #'655': tag655.convertTag655,  # druh práce ignorujeme 9/9 případů lhal
            'C15': tagC15.convertTagC15,  # abstract
            '653': tag653.convertTag653,  # keywords
            '700': tag700.convertTag700,  # vedoucí, oponent,.. 
            '300': otherTag.convertTag300, # počet stran
            '020': tag020.convertTag020, # ISBN
            '500': otherTag.convertTag500, # obecná poznámka - TODO smazat
            '964': otherTag.convertTag964, 
            }

    #TODO jsou dva zdroje autoru zkotrovat jestli sedi

    # Jaro potvrdil následůjící postup
    if '264' in metadataOrigin.keys():
        assert '260' not in metadataOrigin.keys()
        metadataOrigin['260'] = metadataOrigin['264']

    for tag in mandatory.keys():
        if not tag in metadataOrigin.keys():
            error_msg = "No tag {} in metadata".format(tag)
            categorize.categorize_item(oai_id,error_msg)
            #print(metadata)
            return
   
    allTags = {**mandatory, **obligatory}
    for tag in allTags.keys():
        if not tag in metadataOrigin.keys():
            continue
        metadata[tag] = allTags[tag](metadataOrigin[tag], oai_id, categorize)
    
    #print(metadata)
    return metadata
       

def createDC(server, categorize, oai_id, metadataOrigin, metadataDigitool):
    metadataReturn = []
    #TODO
    #print('hui',metadataOrigin)
    #if metadataOrigin is None:
    #    return None, None

    lang = getTopic(categorize, oai_id, 'lang', metadataOrigin)
    if not lang:
        error_msg = "No language found in 041 and 008."
        categorize.categorize_item(oai_id,error_msg)
    metadataReturn.append({ "key": "dc.language", "value": catalogue.langText[lang], "language": 'cs_CZ' },) 
    metadataReturn.append({ "key": "dc.language.iso", "value": lang },) 
    
    aleph_id = getTopic(categorize, oai_id, 'aleph_id', metadataOrigin)
    metadataReturn.append({ "key": "dc.identifier.aleph", "value": aleph_id },)
    
    title = getTopic(categorize, oai_id, 'title', metadataOrigin)
    if not title: 
        raise Exception('No title')
    metadataReturn.append({ "key": "dc.title", "language": lang, "value": title },)
    
    title2 = getTopic(categorize, oai_id, 'alternative', metadataOrigin)
    if title2:
        lang2 = getTopic(categorize, oai_id, 'alternative_lang', metadataOrigin)
        if not lang2 and lang in ['cs_CZ','sk_SK']:
            lang2 = 'en_US'
        if not lang2 and lang in ['en_US']:
            lang2 = 'cs_CZ'
        if not lang2:
            raise Exception('Unknown langue of alternative title')
        metadataReturn.append({ "key": "dc.title.translated", "language": lang2, "value": title2 },)

    degree = getTopic(categorize, oai_id, 'degree', metadataOrigin)
    metadataReturn.append({ "key": "dc.type", "language": 'cs_CZ', "value": degree },)
    degreeTitle = getTopic(categorize, oai_id, 'degreeTitle', metadataOrigin)
    metadataReturn.append({ "key": "thesis.degree.name", "language": 'cs_CZ', "value": degreeTitle },)

    abstract = getTopic(categorize, oai_id, 'abstract', metadataOrigin)
    if abstract:
        metadataReturn.append({ "key": "dc.description.abstract", "language": lang, "value": abstract },)
    abstract2 = getTopic(categorize, oai_id, 'abstract2', metadataOrigin)
    abstract3 = getTopic(categorize, oai_id, 'abstract3', metadataOrigin)
    if abstract2 and abstract3:
        assert "Thomas Schelling's  Beitrag" in abstract or 'volatilitu menových' in abstract 
        metadataReturn.append({ "key": "dc.description.abstract", "language": 'en_US', "value": abstract2 },)
        metadataReturn.append({ "key": "dc.description.abstract", "language": 'cs_CZ', "value": abstract3 },)
    elif abstract2 or abstract3:
        if abstract3:
            abstract2 = abstract3
        lang2 = getTopic(categorize, oai_id, 'alternative_lang', metadataOrigin)
        if not lang2 and lang in ['cs_CZ','sk_SK']:
            lang2 = 'en_US'
        if not lang2 and lang in ['en_US']:
            lang2 = 'cs_CZ'
        if not lang2:
            raise Exception('Unknown langue of alternative title')
        if lang2=='sk_SK':
            lang2='cs_CZ'
        metadataReturn.append({ "key": "dc.description.abstract", "language": lang2, "value": abstract2 },)
   
    discipline = getTopic(categorize, oai_id, 'discipline', metadataOrigin)
    if discipline:
        metadataReturn.append({ "key": "thesis.degree.discipline", "language": 'cs_CZ', "value": discipline },)
    program = getTopic(categorize, oai_id, 'program', metadataOrigin)
    if program:
        metadataReturn.append({ "key": "thesis.degree.program", "language": 'cs_CZ', "value": program },)
    
    faculty = getTopic(categorize, oai_id, 'faculty', metadataOrigin)
    metadataReturn.append({ "key": "dc.description.faculty", "language": 'cs_CZ', "value": faculty },)
   
    department = getTopic(categorize, oai_id, 'department', metadataOrigin)
    if department:
        metadataReturn.append({ "key": "dc.description.department", "language": 'cs_CZ', "value": department },)
    
    author = getTopic(categorize, oai_id, 'author', metadataOrigin)
    metadataReturn.append({ "key": "dc.contributor.author", "value": author },)

    advisor = getTopic(categorize, oai_id, 'advisor', metadataOrigin)
    if advisor:
        metadataReturn.append({ "key": "dc.contributor.advisor","value": advisor },)
    commitee = getTopic(categorize, oai_id, 'commitee', metadataOrigin)
    if commitee:
        metadataReturn.append({ "key": "dc.contributor.referee","value": commitee },)
    consultant = getTopic(categorize, oai_id, 'consultant', metadataOrigin)
    if consultant:
        metadataReturn.append({ "key": "dc.contributor","value": consultant },)

    #TODO place, institut, isbn

    #další lide TODO poupravit
    tip = getTopic(categorize, oai_id, 'tip', metadataOrigin)
    if tip:
        for person in tip:
            if comparePeople(person,author):
                continue
            if advisor and comparePeople(person,advisor):
                continue
            if commitee and comparePeople(person,commitee):
                continue
            if consultant and comparePeople(person,consultant):
                continue
            metadataReturn.append({ "key": "dc.contributor","value": person },)

    pages = getTopic(categorize, oai_id, 'pages', metadataOrigin)
    #TODO ulozit

    year = getTopic(categorize, oai_id, 'year', metadataOrigin)
    if year:
        metadataReturn.append({ "key": "dc.date.issued","value": year },)
    if year and (len(year) == 4 and '?' not in year and int(year) >= 2006):
        categorize.categorize_item(oai_id,"Work in year {}".format(year))

    keywords = sumTopic(categorize, oai_id, 'keywords', metadataOrigin)
    if keywords:
        for keyword in keywords:
            metadataReturn.append({ "key": "dc.subject","value": keyword, "language": "en_US" },)

    return {"metadata": metadataReturn }
