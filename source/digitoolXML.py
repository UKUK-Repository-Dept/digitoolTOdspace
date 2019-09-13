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

    def __skipped_type(self, oai_id):
        tree = ET.parse(self.xml_dirname+'/'+str(oai_id)+".xml")
        root = tree.getroot()
        usage_type = root.findall("./*/*/usage_type")[0].text
        return usage_type in ['ARCHIVE','INDEX']
    
    def get_relations(self, oai_id):
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
                originalMetadataXML = self.get_metadata(relation)
                if 'marc' in originalMetadataXML.keys():
                    marc += 1
                    oai_ids.append(relation)
            #assert marc == 1 #TODO
            if marc == 0:
                pass
                #print(oai_id, end =', ')
                #print(oai_id)

        return oai_ids

    def get_attachements(self, oai_id, seen=None):
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
        def parseDC(value):
            tree = ET.fromstring(value)
            for field in tree:
                yield (field.tag,field.text)
        logging.debug("Getting metadata of {}.".format(oai_id))        
        tree = ET.parse(self.xml_dirname+"/"+str(oai_id)+".xml")
        root = tree.getroot()
        mds = tag(tag(root,"digital_entity"),"mds")
        res = {}
        for child in mds:
            name = tag(child,"name")
            metadataType = tag(child,"type")
            value = tag(child,"value")
            #print(oai_id, name.text, metadataType.text, value.text)
            if name.text != 'descriptive':
                continue
            if metadataType.text == 'marc':
                res['marc'] = parseMarc(value.text)
            elif metadataType.text == 'dc':
                res['dc'] = list(parseDC(value.text))
                pass
            else:
                raise Exception("unknown format")
        return res

    def get_category(self, oai_id):
        tree = ET.parse(self.xml_dirname+"/"+oai_id+".xml")
        root = tree.getroot()
        label = tag(tag(tag(root,"digital_entity"),"control"),"label")
        note = tag(tag(tag(root,"digital_entity"),"control"),"note")
        ingest = tag(tag(tag(root,"digital_entity"),"control"),"ingest_name")
        return (label.text,ingest.text,note.text)
