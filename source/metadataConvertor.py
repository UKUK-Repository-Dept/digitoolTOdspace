import re
import xml.etree.cElementTree as ET
from tags import * 
import catalogue

class Metadata:
    def __init__(self):
        self.dc = ET.Element("dublin_core")
        self.thesis = ET.Element("dublin_core", schema="thesis")
        self.dcterms = ET.Element("dublin_core", schema="dcterms")

    def __str__(self):
        s = ET.tostring(self.dc).decode() + "\n"
        s += ET.tostring(self.thesis).decode()
        return s

    def save(self, directory):
        tree = ET.ElementTree(self.dc)
        tree.write(directory+'/dublin_core.xml')
        tree = ET.ElementTree(self.thesis)
        tree.write(directory+'/metadata_thesis.xml')

def getTopic(topic, metadata):
    result1  = None
    tag1 = None
    for tag2 in metadata:
        if not topic in metadata[tag2].keys():
            continue
        result2 = metadata[tag2][topic]
        if result1 and result1 != result2:
            error_msg = 'Different {} {}:"{}" {}: "{}"'.format(topic, tag1, result1, tag2, result2)
            raise Exception(error_msg)
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
    tags = { 
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
            '022': otherTag.convertTag022, # ISSN
            '017': otherTag.convertTag017, # DIO
            '964': otherTag.convertTag964, 
            'TYP': otherTag.convertTagTYP, 
            }

    ignoredTags = ['LDR','FMT','500','C26','BAS','999','005','003','C13','024','250']
    todoTags = ['003', '005', '024', '242', '250', '490', '500', '773', '787', '856', '999', 'BAS', 'C12', 'C13', 'C20', 'C26', 'C30', 'C34', 'C99', 'FMT', 'LDR']


    for tag in metadataDigitool.keys():
        if not tag in tags.keys():
            if  not tag in (ignoredTags + todoTags):
                raise Exception('Unknown tag')
            continue
        parsedMetadata[tag] = tags[tag](metadataDigitool[tag], oai_id)
    
    return parsedMetadata
       

def createDC(oai_id, metadataOrigin, metadataDigitool):
    m = Metadata()

    lang = getTopic('lang', metadataOrigin)
    if not lang:
        raise Exception("No language found in 041 and 008.")
    ET.SubElement(m.dc, "dcvalue", element='language', qualifier='none', language=lang).text = catalogue.langText[lang]
    ET.SubElement(m.dc, "dcvalue", element='language', qualifier='iso').text = lang
    
    aleph_id = getTopic('aleph_id', metadataOrigin)
    ET.SubElement(m.dc, "dcvalue", element='identifier', qualifier='aleph').text = aleph_id
    doi = getTopic('doi', metadataOrigin)
    if doi:
        ET.SubElement(m.dc, "dcvalue", element='identifier', qualifier='doi').text = doi
    isbns = getTopic('isbns', metadataOrigin)
    if isbns:
        for isbn in isbns:
            ET.SubElement(m.dc, "dcvalue", element='identifier', qualifier='isbn').text = isbn
    issn = getTopic('issn', metadataOrigin)
    if issn:
        ET.SubElement(m.dc, "dcvalue", element='identifier', qualifier='issn').text = issn
    
    title = getTopic('title', metadataOrigin)
    if not title: 
        raise Exception('No title')
    ET.SubElement(m.dc, "dcvalue", element='title', qualifier='none', language = lang).text = title
    
    title2 = getTopic('alternative', metadataOrigin)
    if title2:
        lang2 = getTopic('alternative_lang', metadataOrigin)
        if not lang2 and lang in ['cs_CZ','sk_SK']:
            lang2 = 'en_US'
        if not lang2 and lang in ['en_US']:
            lang2 = 'cs_CZ'
        if not lang2:
            raise Exception('Unknown langue of alternative title')
        ET.SubElement(m.dc, "dcvalue", element='title', qualifier='translated', language=lang2).text = title2

    abstract = getTopic('abstract', metadataOrigin)
    if abstract:
        ET.SubElement(m.dc, "dcvalue", element='description', qualifier='abstract', language=lang).text = abstract
    abstract2 = getTopic('abstract2', metadataOrigin)
    abstract3 = getTopic('abstract3', metadataOrigin)
    if abstract2 and abstract3:
        assert "Thomas Schelling's  Beitrag" in abstract or 'volatilitu menových' in abstract 
        ET.SubElement(m.dc, "dcvalue", element='description', qualifier='abstract', language='en_US').text = abstract2
        ET.SubElement(m.dc, "dcvalue", element='description', qualifier='abstract', language='cs_CZ').text = abstract3
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
        ET.SubElement(m.dc, "dcvalue", element='description', qualifier='abstract', language=lang2).text = abstract2
   
    author = sumTopic('author', metadataOrigin)
    if author:
        for a in author:
            ET.SubElement(m.dc, "dcvalue", element='contributor', qualifier='author').text = a
    editor = sumTopic('editor', metadataOrigin)
    if editor:
        for e in editor:
            ET.SubElement(m.dc, "dcvalue", element='contributor', qualifier='editor').text = e
    other = getTopic('other', metadataOrigin)
    if other:
        ET.SubElement(m.dc, "dcvalue", element='contributor', qualifier='other').text = other

    pages = getTopic('pages', metadataOrigin)
    ET.SubElement(m.dcterms, "dcvalue", element='pages', qualifier='none').text = pages

    year = getTopic('year', metadataOrigin)
    if year:
        ET.SubElement(m.dc, "dcvalue", element='date', qualifier='issued').text = year

    keywords = sumTopic('keywords', metadataOrigin)
    if keywords:
        for keyword in keywords:
            ET.SubElement(m.dc, "dcvalue", element='subject', qualifier='none', language='en_US').text = keyword

    return m
