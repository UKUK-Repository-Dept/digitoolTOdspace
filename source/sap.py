import os
import xml.etree.cElementTree as ET

class Metadata:
    def __init__(self):
        self.dc = ET.Element("dublin_core")
        self.thesis = ET.Element("dublin_core", schema="thesis")
        #tree = ET.ElementTree(self.dc)
        #tree.write('hui')

    def __str__(self):
        s = ET.tostring(self.dc).decode() + "\n"
        s += ET.tostring(self.thesis).decode()
        return s

def createArchive(oai_id, xml_dirname, metadata, attachements):
    outputDirectory = 'output/' + str(oai_id)
    
    m = Metadata()
    for row in metadata['metadata']:
        key = row['key']
        if key.split('.')[0] == 'dc':
            pass
        elif key.split('.')[0] == 'thesis':
            #print(key)
            pass
        else:
            raise Exception('Key {} do not has a category'.format(key))
    print(m)

    return

    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    
    f = open(outputDirectory+'/contents','w')
    for filename, filetype, description in attachements:
        filepath = xml_dirname + '/streams/' + filename
        os.system('cp '+filepath+' '+outputDirectory)
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

