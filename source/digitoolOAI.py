import requests
import json
import xml.etree.ElementTree as ET
import digitoolXML #TODO SMAZAT
# http://www.openarchives.org/OAI/openarchivesprotocol.html

def tag(root,tag):
    try:
        subtree=list(child for child in root if tag in child.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

class Digitool:
    server = "dingo.ruk.cuni.cz:8881"
    metadataPrefix = "oai_dc"
    identifierPrefix = "oai:DURCharlesUniPrague.cz:"
    metadata_types = { 
            '{http://www.openarchives.org/OAI/2.0/oai_dc/}dc':'dc',
            '{http://www.openarchives.org/OAI/2.0/}record':'record',
            }

    #TODO 
    mistery = [ # nejspíš neaktualizace oai
            23450, 14220, 14175, 1333924, 14704, 14706, 14681, 24331, 23521, 14222, 14254, 14294, 
            14767, 15333, 46706, 14708, 46205, 14182, 14177, 50214, 14293, 14186, 14680, 14675, 
            14183, 14221, 14678, 15064, 14631, 52563, 14682, 14685, 14766, 52626, 23520, 43163, 
            14164, 14217, 14185, 14147, 15062, 14679, 14632, 15332, 15061, 14684, 14683, 17946, 
            23532, 14224, 14219, 15330, 1333901 ] 
    otherTrash = [ 1553331, 92518 ]


    def __init__(self,oai_set):
        self.oai_set = oai_set
        self.skipItems = self.mistery + self.otherTrash 

    def download_list(self):
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
            if int(oai_id) in self.skipItems:
                continue
            header = tag(record,"header")
            if 'status' in header.attrib and header.attrib['status'] == 'deleted':
                continue
            d = "23.7.2019" + '/digital_entities'
            oai_ids.append(oai_id)
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
