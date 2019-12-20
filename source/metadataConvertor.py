import re
from tags import * 
import catalogue

def comparePeople(name1,name2): #TODO potrebuju to?
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


def getTopic(topic, metadata):
    #v neshodě vrací to poslední, nikoliv autoritaivní 
    #TODO kontrovat vše
    result1  = None
    tag1 = None
    for tag2 in metadata:
        if not topic in metadata[tag2].keys():
            continue
        result2 = metadata[tag2][topic]
        error_msg = 'Different {} {}:"{}" {}: "{}"'.format(topic, tag1, result1, tag2, result2)
        personTopics = ['author','editor','other']
        result1 = result2
        tag1 = tag2
    return result1

def sumTopic(topic, metadata):
    result = []
    for tag2 in metadata:
        if not topic in metadata[tag2].keys():
            continue
        result = result + metadata[tag2][topic]
    if result != []:
        return result


def parseMarc(metadataDigitool, oai_id):
    parsedMetadata = {}
    tags = { #TODO zkontroval vyplnenou tabulku vs statistiku vs toto
            '001': otherTag.convertTag001,#aleph_id
            '245': tag245.convertTag245, #titul, autor 
            '100': tag100.convertTag100, #autor
            '260': tag260.convertTag260, #místo vydání a datum 
            '008': otherTag.convertTag008,#jazyk na pozici 35-37
            '041': tag041.convertTag041,  # jazyk 
            '246': tag246.convertTag246,  # titulek v překladu 
            'C15': tagC15.convertTagC15,  # abstract
            '653': tag653.convertTag653,  # keywords
            '700': tag700.convertTag700,  # vedoucí, oponent,.. 
            '300': otherTag.convertTag300, # počet stran
            '020': tag020.convertTag020, # ISBN
            '500': otherTag.convertTag500, # obecná poznámka - TODO smazat
            '964': otherTag.convertTag964, 
            }

    for tag in tags.keys():
        if not tag in metadataDigitool.keys():
            continue
        parsedMetadata[tag] = tags[tag](metadataDigitool[tag], oai_id)
    
    return parsedMetadata
       

def createDC(oai_id, metadataOrigin, metadataDigitool):
    metadataReturn = []
    #TODO
    #print('hui',metadataOrigin)
    #if metadataOrigin is None:
    #    return None, None

    lang = getTopic('lang', metadataOrigin)
    if not lang:
        raise Exception("No language found in 041 and 008.")
    metadataReturn.append({ "key": "dc.language", "value": catalogue.langText[lang], "language": 'cs_CZ' },) 
    metadataReturn.append({ "key": "dc.language.iso", "value": lang },) 
    
    aleph_id = getTopic('aleph_id', metadataOrigin)
    metadataReturn.append({ "key": "dc.identifier.aleph", "value": aleph_id },)
    
    title = getTopic('title', metadataOrigin)
    if not title: 
        raise Exception('No title')
    metadataReturn.append({ "key": "dc.title", "language": lang, "value": title },)
    
    title2 = getTopic('alternative', metadataOrigin)
    if title2:
        lang2 = getTopic('alternative_lang', metadataOrigin)
        if not lang2 and lang in ['cs_CZ','sk_SK']:
            lang2 = 'en_US'
        if not lang2 and lang in ['en_US']:
            lang2 = 'cs_CZ'
        if not lang2:
            raise Exception('Unknown langue of alternative title')
        metadataReturn.append({ "key": "dc.title.translated", "language": lang2, "value": title2 },)

    degree = getTopic('degree', metadataOrigin)
    metadataReturn.append({ "key": "dc.type", "language": 'cs_CZ', "value": degree },)
    degreeTitle = getTopic('degreeTitle', metadataOrigin)
    metadataReturn.append({ "key": "thesis.degree.name", "language": 'cs_CZ', "value": degreeTitle },)

    abstract = getTopic('abstract', metadataOrigin)
    if abstract:
        metadataReturn.append({ "key": "dc.description.abstract", "language": lang, "value": abstract },)
    abstract2 = getTopic('abstract2', metadataOrigin)
    abstract3 = getTopic('abstract3', metadataOrigin)
    if abstract2 and abstract3:
        assert "Thomas Schelling's  Beitrag" in abstract or 'volatilitu menových' in abstract 
        metadataReturn.append({ "key": "dc.description.abstract", "language": 'en_US', "value": abstract2 },)
        metadataReturn.append({ "key": "dc.description.abstract", "language": 'cs_CZ', "value": abstract3 },)
    elif abstract2 or abstract3:
        if abstract3:
            abstract2 = abstract3
        lang2 = getTopic('alternative_lang', metadataOrigin)
        if not lang2 and lang in ['cs_CZ','sk_SK']:
            lang2 = 'en_US'
        if not lang2 and lang in ['en_US']:
            lang2 = 'cs_CZ'
        if not lang2:
            raise Exception('Unknown langue of alternative title')
        if lang2=='sk_SK':
            lang2='cs_CZ'
        metadataReturn.append({ "key": "dc.description.abstract", "language": lang2, "value": abstract2 },)
   
    discipline = getTopic('discipline', metadataOrigin)
    if discipline:
        metadataReturn.append({ "key": "thesis.degree.discipline", "language": 'cs_CZ', "value": discipline },)
    program = getTopic('program', metadataOrigin)
    if program:
        metadataReturn.append({ "key": "thesis.degree.program", "language": 'cs_CZ', "value": program },)
    
    faculty = getTopic('faculty', metadataOrigin)
    metadataReturn.append({ "key": "dc.description.faculty", "language": 'cs_CZ', "value": faculty },)
   
    department = getTopic('department', metadataOrigin)
    if department:
        metadataReturn.append({ "key": "dc.description.department", "language": 'cs_CZ', "value": department },)
    
    author = getTopic('author', metadataOrigin)
    metadataReturn.append({ "key": "dc.contributor.author", "value": author },)

    advisor = getTopic('advisor', metadataOrigin)
    if advisor:
        metadataReturn.append({ "key": "dc.contributor.advisor","value": advisor },)
    commitee = getTopic('commitee', metadataOrigin)
    if commitee:
        metadataReturn.append({ "key": "dc.contributor.referee","value": commitee },)
    consultant = getTopic('consultant', metadataOrigin)
    if consultant:
        metadataReturn.append({ "key": "dc.contributor","value": consultant },)

    #TODO place, institut, isbn

    #další lide TODO poupravit
    tip = getTopic('tip', metadataOrigin)
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

    pages = getTopic('pages', metadataOrigin)
    #TODO ulozit

    year = getTopic('year', metadataOrigin)
    if year:
        metadataReturn.append({ "key": "dc.date.issued","value": year },)

    keywords = sumTopic('keywords', metadataOrigin)
    if keywords:
        for keyword in keywords:
            metadataReturn.append({ "key": "dc.subject","value": keyword, "language": "en_US" },)

    return {"metadata": metadataReturn }
