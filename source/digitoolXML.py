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

    def get_attachements(self, oai_id, full=False, seen=None):
        if seen == None:
            seen = [oai_id]
        logging.info("Getting attachement of {}.".format(oai_id))        
        tree = ET.parse(self.xml_dirname+'/'+str(oai_id)+".xml")
        root = tree.getroot()
        for stream_ref in root.findall("./*stream_ref"):
            filename = stream_ref.find('file_name').text
            if filename != None:
                if full:
                    mime_type = stream_ref.find('mime_type').text
                    yield filename, mime_type
                else:
                    yield filename
        subrecords = []
        for relations in root.findall("./*relations"):
            for relation in relations:
                relation_type = relation.find('type').text
                pid = relation.find('pid').text
                if pid in seen:
                    continue
                #if not self.__skipped_type(pid): #teď děláme exporty se všim
                subrecords.append(pid)
        seen = seen + subrecords
        for new_id in subrecords:
            yield from self.get_attachements(new_id,full=full,seen=seen)
    
    def get_metadata(self, oai_id):
        def parseMarc(value):
            metadata = {}
            tree = ET.fromstring(value)
            for field in tree:
                if field.tag == '{http://www.loc.gov/MARC21/slim}datafield':
                    for subfield in field:
                        tag = field.attrib
                        index = str(tag['tag'])+'-'+str(tag['ind1'])+'-'+str(tag['ind2'])
                        if subfield.text != None:
                            code = subfield.attrib['code']
                            metadata.setdefault(index,{})
                            metadata[index].setdefault(code,[])
                            metadata[index][code].append(subfield.text)
            return metadata
        def parseDC(value):
            tree = ET.fromstring(value)
            for field in tree:
                yield (field.tag,field.text)
        tree = ET.parse(self.xml_dirname+"/"+str(oai_id)+".xml")
        root = tree.getroot()
        mds = tag(tag(root,"digital_entity"),"mds")
        res = {}
        for child in mds:
            name = tag(child,"name")
            metadataType = tag(child,"type")
            value = tag(child,"value")
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
