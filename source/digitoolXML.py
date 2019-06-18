#!/usr/bin/python3
import os
import requests, json
import xml.etree.ElementTree as ET

def tag(root,tag):
    try:
        subtree=list(r for r in root if tag in r.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

class DigitoolXML:
    def __init__(self, dirname, skip_missing = False):
        self.dirname = dirname
        self.xml_dirname = dirname+'/digital_entities'
        self.skip_missing = skip_missing

    def get_attachements(self, oai_id, full=False):
        if self.skip_missing:
            try:
                tree = ET.parse(self.xml_dirname+'/'+str(oai_id)+".xml")
            except:
                return
        else:
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
                if relation_type == "include":
                    pid = relation.find('pid').text
                    subrecords.append(pid)
        for record in subrecords:
            yield from self.get_attachements(record,full)


    def get_category(self, filename):
        tree = ET.parse(self.xml_dirname+"/"+filename)
        root = tree.getroot()
        label = tag(tag(tag(root,"digital_entity"),"control"),"label")
        note = tag(tag(tag(root,"digital_entity"),"control"),"note")
        ingest = tag(tag(tag(root,"digital_entity"),"control"),"ingest_name")
        return (label.text,ingest.text,note.text)
