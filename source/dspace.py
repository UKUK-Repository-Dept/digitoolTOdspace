import requests
import json
import xml.etree.ElementTree as ET
import os
import logging
            

class Dspace:
    url = "https://gull.is.cuni.cz/rest"
    headers= { 
        "content-type": "application/json",
        }


    def __init__(self, user, passwd, xml_dirname=""):
        self.user = user 
        self.passwd = passwd
        self.login = {
            'email': self.user,
            'password': self.passwd
        }
        response = requests.post(
            self.url+'/login', 
            headers=self.headers, 
            json=self.login
            )
        response.raise_for_status()
        self.token = response.text
        self.headers["rest-dspace-token"]= self.token
        self.assets = xml_dirname + "/streams/"
    
    def logout(self):
        response = requests.post(
            self.url+'/logout', 
            headers=self.headers, 
            )
        response.raise_for_status()
        self.token = response.text

    
    def list_bitstream(self):
        response = requests.get(
            self.url+'/items/5781/bitstreams', 
            headers=self.headers, 
            )
        for key in json.loads(response.text)[0].keys():
            print(key+":")
            for bitstream in json.loads(response.text):
                print(bitstream[key])
    
    def post_new_bitstream(self, item_id, filename, filetype, description=None):
        files = { #TODO tady to nesmí být
            'file': open(self.assets + filename,'rb')
        }
        params={
            'name': filename,
            'description': description,
            'mineType': filetype,
        }
        response = requests.post(
            self.url+'/items/'+str(item_id)+'/bitstreams/',
            headers=self.headers,
            files=files,
            verify=False,
            params=params,
        )
        tree = ET.fromstring(response.text)
        for field in tree:
            if field.tag == 'id':
                bitstream_id = field.text
        if 'Posudek' in description:
            response = requests.get(
                self.url+'/bitstreams/'+str(bitstream_id)+'/policy', 
                headers=self.headers, 
                )
            policy_id = json.loads(response.text)[0]['id']
            response = requests.delete(
                self.url+'/bitstreams/'+str(bitstream_id)+'/policy/'+str(policy_id), 
                headers=self.headers, 
                )
            response = requests.post(
                self.url+'/bitstream/'+str(bitstream_id)+'/policy', 
                headers=self.headers,
                json=[{
                    'action':'WITHDRAWN_READ',
                    "epersonId":-1,
                    "groupId":0,
                    "resourceId":bitstream_id,
                    "resourceType":"bitstream",
                    "rpDescription":"Need check for personal data.",
                    "rpName":"review",
                    "rpType":"TYPE_CUSTOM",
                    "startDate":'1111-01-01',
                    "endDate":'9999-01-09',
                    }], 
                )
    
    def delete_bitstream(self,bitstream):
        response = requests.delete(
                self.url+'/bitstreams/'+str(bitstream),
                headers=self.headers,
                )

    def handle(self, handle):
        response = requests.get(
            self.url+'/handle/'+handle, 
            headers=self.headers, 
            )
        if response.status_code == 404:
            logging.error("No handle {}.".format(handle))
            return
        handle_json = json.loads(response.text)
        for key in handle_json.keys():
            print(key,handle_json[key])
    
    def new_item(self, collection_id, metadata, files):
        response = requests.post(
            self.url+'/collections/'+str(collection_id)+'/items', 
            headers=self.headers,
            json=metadata, 
            )
        if response.status_code == 500:
            for m in metadata['metadata']:
                if m['key'] == 'dc.identifier.aleph':
                    aleph_id = m['value']
            logging.error("{}".format(aleph_id))
            print(metadata['metadata'])
            return
        root = ET.fromstring(response.text)
        subtree=list(r for r in root if "id" in r.tag)[0]
        dspace_id = int(subtree.text)
        for filename, filetype, description in files:
            self.post_new_bitstream(dspace_id, filename, filetype, description)
    
    def total_size(self):
        size = 0
        offset = 0
        while True:
            #print(offset, size)
            params={
                'offset': offset,
            }
            offset += 100
            response = requests.get(
                self.url+'/bitstreams',
                headers=self.headers,
                params=params,
                )
            if len(json.loads(response.text)) == 0:
                return size
            for item in json.loads(response.text):
                size += item['sizeBytes']
                #print(item)
    
    def delete_item(self, item_id):
        response = requests.get(
            self.url+'/items/'+str(item_id)+'/bitstreams', 
            headers=self.headers,
            )
        for item in json.loads(response.text):
            self.delete_bitstream(item['id'])
        response = requests.delete(
                self.url+'/items/'+str(item_id)+'/metadata',
                headers=self.headers,
                )
        response = requests.delete(
                self.url+'/items/'+str(item_id),
                headers=self.headers,
                )


    
    def delete_all_item(self, collection_id):
        itemSize = 42
        while itemSize > 0:
            response = requests.get(
                self.url+'/collections/'+str(collection_id)+'/items', 
                headers=self.headers,
                )
            if response.status_code == 404:
                logging.error("No collection {}.".format(collection_id))
                return
            itemSize = len(json.loads(response.text))
            for item in json.loads(response.text):
                self.delete_item(item['id'])
