import requests
import logging
import json
import os
import xml.etree.ElementTree as ET
# http://www.openarchives.org/OAI/openarchivesprotocol.html

def tag(root,tag):
    try:
        subtree=list(child for child in root if tag in child.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

class Digitool:
    server = "dingo.ruk.cuni.cz:8881"
    metadataPrefix = "oai_dc" #alternativně "marc21"
    identifierPrefix = "oai:DURCharlesUniPrague.cz:"
    metadata_types = { 
            '{http://www.openarchives.org/OAI/2.0/oai_dc/}dc':'dc',
            '{http://www.openarchives.org/OAI/2.0/}record':'record',
            }
    #http://dingo.ruk.cuni.cz:8881/OAI-PUB?verb=GetRecord&identifier=oai:DURCharlesUniPrague.cz:134895&metadataPrefix=marc21

    def __init__(self,oai_set,xml_dirname):
        self.oai_set = oai_set
        self.xml_dirname = xml_dirname

    def download_list(self):
        oai_ids = []
        path = self.xml_dirname + "/digital_entities"
        for filename in os.listdir(path):
            with open(path+'/'+filename,'r') as f:
                if "<name>descriptive</name>" in f.read():
                    oai_id = filename.split('.')[0]
                    oai_ids.append(oai_id)
        #print(oai_ids)
        return oai_ids

    def download_list_old(self): #OAI is evil and do not show everything which it has
        logging.info('Connecting to OAI.')
        url = ( "http://" + self.server + "/OAI-PUB?" +  
            "verb=ListRecords" + 
            "&metadataPrefix=" + self.metadataPrefix + 
            "&set=" + self.oai_set )
        def recursion(url, resumptionToken):
            if resumptionToken is None:
                response = requests.get(url)
            else:
                response = requests.get(url+"&resumptionToken="+resumptionToken)
            root = ET.fromstring(response.text)
            ListRecord=tag(root,"ListRecords")
            for child in ListRecord:
                if "record" in child.tag: 
                    yield child
                elif "resumptionToken" in child.tag:
                    resumptionToken = child.text
                    yield from recursion(url,resumptionToken)
                else:
                    raise "Unknown tag"
        self.list = list(recursion(url,None))
        oai_ids = []
        for record in self.list:
            oai_id = self.get_oai_id(record)
            header = tag(record,"header")
            if 'status' in header.attrib and header.attrib['status'] == 'deleted':
                continue
            oai_ids.append(oai_id)
        print(len(oai_ids))
        logging.info('OAI list downloaded')
        return oai_ids


    def get_item(self, oai_id):
        url = ( "http://" + self.server + "/OAI-PUB?" +  
            "verb=GetRecord" + 
            "&metadataPrefix=" + self.metadataPrefix + 
            "&identifier=" + self.identifierPrefix + str(oai_id) )
        response = requests.get(url)
        root = ET.fromstring(response.text)
        record = tag(tag(root,"GetRecord"),"record")
        return record

    def get_oai_id(self, record):
        header=tag(record,"header")
        identifier=tag(header,"identifier").text
        return identifier.split(":")[-1]
    
    def get_metadata(self, record):
        try:
            all_metadata=tag(record,"metadata")
        except:
            return
        res = {}
        for metadata in all_metadata:
            metadata_type = self.metadata_types[metadata.tag]
            res[metadata_type] = []
            for child in metadata:
                res[metadata_type].append((child.tag, child.text))
        return res
