import os
import requests
import xml.etree.cElementTree as ET
import shutil
import json
from bs4 import BeautifulSoup

class Metadata:
    def __init__(self):
        self.dc = ET.Element("dublin_core")
        self.thesis = ET.Element("dublin_core", schema="thesis")

    def __str__(self):
        s = ET.tostring(self.dc).decode() + "\n"
        s += ET.tostring(self.thesis).decode()
        return s

    def save(self, directory):
        tree = ET.ElementTree(self.dc)
        tree.write(directory+'/dublin_core.xml')
        tree = ET.ElementTree(self.thesis)
        tree.write(directory+'/metadata_thesis.xml')


def createArchive(oai_id, xml_dirname, metadata, attachements):
    outputDirectory = 'output/' + str(oai_id)


    m = Metadata()
    for row in metadata['metadata']:
        key = row['key'].split('.')
        if key[0] == 'dc':
            if key[1] == 'language' and len(key) == 2:
                ET.SubElement(m.dc, "dcvalue", 
                        element='language', 
                        qualifier='none', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'type' and len(key) == 2:
                ET.SubElement(m.dc, "dcvalue", 
                        element='type', 
                        qualifier='none', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'contributor' and len(key) == 2:
                ET.SubElement(m.dc, "dcvalue", 
                        element='contributor', 
                        qualifier='none', 
                        ).text = row['value']
            elif key[1] == 'title' and len(key) == 2:
                ET.SubElement(m.dc, "dcvalue", 
                        element='title', 
                        qualifier='none', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'subject' and len(key) == 2:
                ET.SubElement(m.dc, "dcvalue", 
                        element='subject', 
                        qualifier='none', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'language' and key[2] == 'iso':
                ET.SubElement(m.dc, "dcvalue", 
                        element='language', 
                        qualifier='iso'
                        ).text = row['value']
            elif key[1] == 'title' and key[2] == 'translated':
                ET.SubElement(m.dc, "dcvalue", 
                        element='title', 
                        qualifier='translated',
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'identifier' and key[2] == 'aleph':
                aleph_id = row['value']
                ET.SubElement(m.dc, "dcvalue", 
                        element='identifier', 
                        qualifier='aleph'
                        ).text = row['value']
            elif key[1] == 'description' and key[2] == 'abstract':
                ET.SubElement(m.dc, "dcvalue", 
                        element='description', 
                        qualifier='abstract',
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'description' and key[2] == 'faculty':
                ET.SubElement(m.dc, "dcvalue", 
                        element='description', 
                        qualifier='faculty',
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'subject' and key[2] == 'czenas':
                ET.SubElement(m.dc, "dcvalue", 
                        element='subject', 
                        qualifier='czenas',
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'contributor' and key[2] == 'author':
                ET.SubElement(m.dc, "dcvalue", 
                        element='contributor', 
                        qualifier='author'
                        ).text = row['value']
            elif key[1] == 'contributor' and key[2] == 'referee':
                ET.SubElement(m.dc, "dcvalue", 
                        element='contributor', 
                        qualifier='referee'
                        ).text = row['value']
            elif key[1] == 'contributor' and key[2] == 'advisor':
                ET.SubElement(m.dc, "dcvalue", 
                        element='contributor', 
                        qualifier='advisor'
                        ).text = row['value']
            elif key[1] == 'date' and key[2] == 'issued':
                ET.SubElement(m.dc, "dcvalue", 
                        element='date', 
                        qualifier='issued'
                        ).text = row['value']
            else:
                raise Exception("Not implemented")
        elif key[0] == 'thesis':
            if key[1] == 'degree' and key[2] == 'name':
                ET.SubElement(m.thesis, "dcvalue", 
                        element='degree', 
                        qualifier='name', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'degree' and key[2] == 'discipline':
                ET.SubElement(m.thesis, "dcvalue", 
                        element='degree', 
                        qualifier='discipline', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'degree' and key[2] == 'program':
                ET.SubElement(m.thesis, "dcvalue", 
                        element='degree', 
                        qualifier='program', 
                        language = row['language']
                        ).text = row['value']
            elif key[1] == 'degree' and key[2] == 'department':
                ET.SubElement(m.thesis, "dcvalue", 
                        element='degree', 
                        qualifier='department', 
                        language = row['language']
                        ).text = row['value']
            else:
                raise Exception("Not implemented")
        else:
            raise Exception('Key {} do not has a category'.format(key))


    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

    #create meadtada files 
    m.save(outputDirectory)

    #create handle file if possible
    response = requests.get("https://dspace.cuni.cz/discover?query="+aleph_id+"&submit=")
    soup = BeautifulSoup(response.text,"lxml")
    search_results = soup.findAll("div", {"class":"row ds-artifact-item search-result-item-div"})
    title_search = soup.findAll("h4")
    if len(title_search) > 0:
        tag = title_search[0]
        handle = tag.parent['href']
        item_id = json.loads(requests.get("https://dspace.cuni.cz/rest"+handle).text)['id']
        old_metadata = json.loads(requests.get("https://dspace.cuni.cz/rest/items/"+str(item_id)+"/metadata").text)
        for row in old_metadata:
            if row['key'] == 'dc.identifier.aleph':
                if aleph_id == row['value']:
                    handle = handle[8:]
                    f = open(outputDirectory+'/handle','w')
                    f.write(handle)
                    f.close()

    f = open(outputDirectory+'/contents','w')
    for filename, filetype, description in attachements:
        filepath = xml_dirname + '/streams/' + filename
        os.system("cp '"+filepath+"' "+outputDirectory)
        row = filename + '\t'
        row += 'bundle:ORIGINAL\t'
        row += 'permissits:-r '
        if 'Posudek' in description:
            row += "'Admin'"
        else:
            row += "'IPshibAuthenticatedUniMember'"
        row += '\tdescription:'+description
        row += '\n'
        f.write(row)
    f.close()

    #shutil.make_archive(outputDirectory, 'zip', outputDirectory)

