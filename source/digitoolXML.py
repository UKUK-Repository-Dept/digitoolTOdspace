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
    archived_items = [ 55067, 92174, 92176, 92204, 92013, 90458, 105049, 105381, 105369, 105371, 
            54933, 90456, 62921, 92170, 92182, 90305, 90294, 89032, 90450, 90455, 90459, 92069, 
            90446, 92186, 90489, 91982, 91608, 91612, 91928, 90461, 90470, 90452, 92217, 90314, 
            82518, 92085, 91998, 90477, 90478, 84003, 92171, 92168, 92197, 90493, 89027, 56213, 
            92194, 92047, 90465, 90467, 90472, 90479, 90453, 90445, 90325, 92173, 92180, 88940, 
            89035, 90485, 90468, 96739, 89034, 61688, 88880, 90474, 90484, 90336, 99996 ]

    def __init__(self, dirname, skip_missing = False):
        self.dirname = dirname
        self.xml_dirname = dirname+'/digital_entities'
        self.skip_missing = skip_missing

    def get_attachements(self, oai_id, full=False):
        if self.skip_missing:
            try:
                tree = ET.parse(self.xml_dirname+'/'+str(oai_id)+".xml")
            except Exception as e:
                return
        else:
            try:
                tree = ET.parse(self.xml_dirname+'/'+str(oai_id)+".xml")
            except Exception as e:
                raise e
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
