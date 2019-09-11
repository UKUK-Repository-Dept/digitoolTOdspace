import re
from tags import * 
import catalogue

def comparePeople(name1,name2):
    def normaliseName(name):
        name = name.replace(':','')
        names = sorted(name.replace(',',' ').replace('-',' ').split())
        for name in names:
            if 'vypracoval' in name:
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
        if len(first) == 2 and first[1] == '.' and first[0] == second[0]: 
            continue #iniciály
        if not first == second:
            return False
    return True


def getTopic(categorize, oai_id, topic, metadata):
    #TODO v neshodě vrací to poslední, nikoliv autoritaivní 
    result1  = None
    tag1 = None
    for tag2 in metadata:
        if not topic in metadata[tag2].keys():
            continue
        result2 = metadata[tag2][topic]
        error_msg = 'Different {} {}:"{}" {}: "{}"'.format(topic, tag1, result1, tag2, result2)
        personTopics = ['author','advisor','commitee','consultant']
        if topic in personTopics and not comparePeople(result1,result2):
            pass # TODO ručne projít před finálním exportem
            #print(oai_id,error_msg)
            #categorize.categorize_item(oai_id,error_msg)
        elif topic not in personTopics and result1 and result1 != result2:
            categorize.categorize_item(oai_id,error_msg)
        result1 = result2
        tag1 = tag2
    return result1

def convertMarc(categorize, oai_id, metadataOrigin):
    metadata = {}
    mandatory = {
            '100': tag100.convertTag100, #autor
            '245': tag245.convertTag245, #titul, autor #TODO kontrola dle mailu od Iry, počkat na nový export 
            '260': tag260.convertTag260, #místo vydání a datum 
            '502': tag502.convertTag502, #kvalifikační práce
            #'710': tag710.convertTag710, #fakulta, katedra #TODO nový mail,povinny
            }
    obligatory = {
            '008': otherTag.convertTag008,#jazyk na pozici 35-37
            '041': tag041.convertTag041,  # jazyk 
            '246': tag246.convertTag246,  # titulek v překladu #TODO upozornit na chybějící podpole s jazykem 
            '520': tag520.convertTag520,  # abstrakt #TODO dořešit jazyky
            #'526': otherTag.convertTag526,# předmět TODO jen devět kousku
            '600': otherTag.convertTag600,# keywords osoba
            '610': otherTag.convertTag610,# keywords organizace
            '630': otherTag.convertTag630,# keywords knihy
            '648': otherTag.convertTag648,# keywords období
            '650': tag650.convertTag650,  # keywords 
            '651': otherTag.convertTag651,# keywords zeměpis
            #'655': tag655.convertTag655,  # druh práce ignorujeme 9/9 případů lhal
            '700': tag700.convertTag700,  # vedoucí, oponent,.. #TODO roky ve stejném poli hlásit!
            }

    # Jaro potvrdil následůjící postup
    if '264' in metadataOrigin.keys():
        assert '260' not in metadataOrigin.keys()
        metadataOrigin['260'] = metadataOrigin['264']

    for tag in mandatory.keys():
        if not tag in metadataOrigin.keys():
            error_msg = "No tag {} in metadata".format(tag)
            categorize.categorize_item(oai_id,error_msg)
            return
    
    allTags = {**mandatory, **obligatory}
    for tag in allTags.keys():
        if not tag in metadataOrigin.keys():
            continue
        metadata[tag] = allTags[tag](metadataOrigin[tag], oai_id, categorize)
    
    return metadata
       

def createDC(categorize, oai_id, metadataOrigin):
    metadataReturn = []
    
    title = getTopic(categorize, oai_id, 'title', metadataOrigin)
    if not title: 
        raise Exception('No title')
    metadataReturn.append({ "key": "dc.title", "language": 'TODO', "value": title },)
    faculty = getTopic(categorize, oai_id, 'faculty', metadataOrigin)
    if not faculty:
        categorize.categorize_item(oai_id,"No faculty")
    
    author = getTopic(categorize, oai_id, 'author', metadataOrigin)
    if not author: 
        raise Exception('No author')
    #TODO zkontrolovat že je to varianta 100 a strip
    metadataReturn.append({ "key": "dc.contributor.author", "value": author },)
   
    abstract = getTopic(categorize, oai_id, 'abstract', metadataOrigin)
    if abstract:
        metadataReturn.append({ "key": "dc.description.abstract", "language": 'TODO', "value": abstract },)

    advisor = getTopic(categorize, oai_id, 'advisor', metadataOrigin)
    #TODO ruční kontrola
    commitee = getTopic(categorize, oai_id, 'commitee', metadataOrigin)
    consultant = getTopic(categorize, oai_id, 'consultant', metadataOrigin)
    #TODO 'advisor' 'committe' 'consultant'

    year = getTopic(categorize, oai_id, 'year', metadataOrigin)
    #if year and len(year) == 4 and '?' not in year and int(year) > 2006:
    #    print(oai_id, year)

    degree = getTopic(categorize, oai_id, 'degree', metadataOrigin)
    if not degree: 
        categorize.categorize_item(oai_id,"No degre")

    # němčina 42606, azbuka 135200
    lang = getTopic(categorize, oai_id, 'lang', metadataOrigin)
    if not lang:
        error_msg = "No language found in 041 and 520."
        categorize.categorize_item(oai_id,error_msg)
    #TODO lang alternative_lang
    return {"metadata": metadataReturn }
