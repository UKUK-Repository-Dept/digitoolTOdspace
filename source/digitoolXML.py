#!/usr/bin/python3
import os
import requests, json
import logging
import xml.etree.ElementTree as ET

def tag(root,tag):
    try:
        subtree=list(r for r in root if tag in r.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

class DigitoolXML:
    def __init__(self, dirname):
        self.dirname = dirname
        self.xml_dirname = dirname+'/digital_entities'

    def get_relations(self, oai_id): 
        # dostane oai_id a vrátí všechny oai_id od stejné práce
        # (v digitoolu má každá příloha, ale i další věci vlastní 
        # oai_id a mají mezi sebou různý vztah. U kvalifikačěk 
        # v té struktuře bylo tolik chyb, že jsme se rozhodli neřešit 
        # strukturu a druh vztahu, ale brát všechno)
        seen = []
        stack = [oai_id]
        while len(stack) > 0:
            oai_id = stack.pop()
            if oai_id in seen:
                continue
            else:
                seen.append(oai_id)
            tree = ET.parse(self.xml_dirname+'/'+str(oai_id)+".xml")
            root = tag(tag(tree.getroot(),'digital_entity'),'relations')
            for relation in root:
                relation_id = tag(relation,'pid').text
                stack.append(relation_id)
        return seen

    def getList(self):
        # vrátí seznam oai_id, kde za každou práci má právě jedno oai_id a to to které má marc
        oai_ids = []
        path = self.xml_dirname
        seen = []
        for filename in os.listdir(path):
            oai_id = filename.split('.')[0]
            if oai_id in seen:
                continue
            else:
                seen.append(oai_id)
            marc = 0
            for relation in self.get_relations(oai_id):
                seen.append(relation)
                if self.get_metadata(relation):
                    marc += 1
                    oai_ids.append(relation)
            assert marc == 1 
        return oai_ids

    def get_attachements(self, oai_id, seen=None):
        # vrátí všechny přílohy práce na základně jednoho jejího oai_id
        logging.debug("Getting attachement of {}.".format(oai_id))
        for relation in self.get_relations(oai_id):
            tree = ET.parse(self.xml_dirname+'/'+str(relation)+".xml")
            root = tree.getroot()
            for stream_ref in root.findall("./*stream_ref"):
                filename = stream_ref.find('file_name').text
                if filename != None:
                    mime_type = stream_ref.find('mime_type').text
                    yield filename, mime_type
    
    def get_metadata(self, oai_id):
        # vrátí metadata z daného oai_id (ale to musí být to co má marc, nikoliv jiná příloha)
        def parseMarc(value):
            metadata = {}
            tree = ET.fromstring(value)
            for field in tree:
                tag = field.attrib
                if field.tag in '{http://www.loc.gov/MARC21/slim}datafield':
                    for subfield in field:
                        #index = str(tag['tag'])+'-'+str(tag['ind1'])+'-'+str(tag['ind2'])
                        index = tag['tag']
                        if subfield.text != None:
                            code = subfield.attrib['code']
                            metadata.setdefault(index,{})
                            metadata[index].setdefault(code,[])
                            metadata[index][code].append(subfield.text)
                if field.tag == '{http://www.loc.gov/MARC21/slim}controlfield':
                    index = tag['tag']
                    metadata[index] = field.text
            return metadata
        logging.debug("Getting metadata of {}.".format(oai_id))        
        tree = ET.parse(self.xml_dirname+"/"+str(oai_id)+".xml")
        root = tree.getroot()
        mds = tag(tag(root,"digital_entity"),"mds")
        for child in mds:
            name = tag(child,"name")
            metadataType = tag(child,"type")
            value = tag(child,"value")
            if name.text != 'descriptive':
                continue
            if metadataType.text == 'marc':
                return parseMarc(value.text)
            else:
                raise Exception("unknown format")

