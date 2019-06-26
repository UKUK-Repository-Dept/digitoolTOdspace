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
    archiv = [ 55067, 92174, 92176, 92204, 92013, 90458, 105049, 105381, 105369, 105371, 
            54933, 90456, 62921, 92170, 92182, 90305, 90294, 89032, 90450, 90455, 90459, 92069, 
            90446, 92186, 90489, 91982, 91608, 91612, 91928, 90461, 90470, 90452, 92217, 90314, 
            82518, 92085, 91998, 90477, 90478, 84003, 92171, 92168, 92197, 90493, 89027, 56213, 
            92194, 92047, 90465, 90467, 90472, 90479, 90453, 90445, 90325, 92173, 92180, 88940, 
            89035, 90485, 90468, 96739, 89034, 61688, 88880, 90474, 90484, 90336, 99996 ]
    archiv2 = [55324, 92559, 63024, 91637, 91641, 89042, 89043, 89030, 91609, 89036]
    archiv3 = [ 88879, 88883, 91638]
    mistery = [ # nejspíš neaktualizace oai
            23450, 14220, 14175, 1333924, 14704, 14706, 14681, 24331, 23521, 14222, 14254, 14294, 
            14767, 15333, 46706, 14708, 46205, 14182, 14177, 50214, 14293, 14186, 14680, 14675, 
            14183, 14221, 14678, 15064, 14631, 52563, 14682, 14685, 14766, 52626, 23520, 43163, 
            14164, 14217, 14185, 14147, 15062, 14679, 14632, 15332, 15061, 14684, 14683, 17946, 
            23532, 14224, 14219, 15330, 1333901 ] 
    deletedPreview = [ #TODO smazat
            526472, 527202, 527192, 526876, 526670, 526700, 527190, 527555, 526690, 526683, 
            527573, 526661, 527421, 528171, 526617, 526480, 527569, 527455, 526657, 526482, 
            527309, 527567, 528039, 527908, 528037, 529482, 529884, 530221, 527164, 526479, 
            526576, 526702, 526677, 527546, 526633, 527196, 527203, 526419, 527911, 526460, 
            527317, 527554, 526665, 526411, 527566, 526663, 527930, 527953, 528031, 529191, 
            527579, 527163, 526477, 526671, 526953, 526588, 527314, 527552, 526691, 527574, 
            527209, 527198, 526490, 527465, 527307, 527367, 526442, 526701, 527974, 527239, 
            26495, 527434, 526473, 526632, 526607, 526462, 526465, 526585, 527319, 526446, 
            26377, 526656, 526484, 527240, 527467, 526485, 526443, 529127, 528144, 527969, 
            28778, 527189, 526378, 526635, 526655, 526668, 527565, 527199, 526422, 526459, 
            526491, 526418, 526515, 526513, 526420, 527316, 526421, 526445, 526877, 527575, 
            26481, 527236, 527596, 526659, 526687, 526866, 528038, 527916, 529128, 526640, 
            527323, 527544, 527284, 526478, 527572, 526945, 526744, 526483, 527973, 526662,
            527966, 527308, 527238, 526463, 526669, 526698, 527580, 528298, 527964, 527773, 
            27896, 527917, 527913, 529493, 528316, 527981, 526476, 526875, 527530, 527960, 
            26689, 527315, 527578, 526440, 526613, 527457, 526754, 526413, 527923, 527146, 
            26581, 526593, 527322, 526584, 527967, 527919, 526556, 528143, 526511, 526487, 
            26537, 526461, 526586, 526437, 527951, 95055, 527937, 527897, 95056, 529708, 
            29654, 526432, 526441, 526707, 527234, 526672, 526493, 526612, 527972, 526685, 
            26557, 526492, 528297, 527420, 527237, 526686, 526488, 527918, 527980, 528122, 
            18211, 95029, 529903, 526417, 527188, 526649, 526674, 527464, 526952, 526673, 
            26703, 526433, 526660, 526697, 526539, 526676, 527320, 526658, 526634, 526436, 
            27197, 526637, 526611, 527318, 527321, 526589, 526692, 526704, 526454, 527200, 
            27576, 526435, 527195, 526609, 526439, 526755, 95035, 527880, 528224, 529488, 
            27978, 526753, ]
    deletedPreview2 = [ #TODO smazat
            55325, 527553, 527456, 528284, 528369, 528390, 528236, 92560, 527547, 528367, 528286, 
            95031, 529214, 528260, 526495, 526377, 528371, 528222, 528421, 528425, 528321, 
            528315, 528778, 526481, 528314, 528267, 528245, 526438, 528283, 528282, 528290, 
            5026, 527896, 526689, 527201, 526581, 526537, 528373, 528255, 529654, 528006, 
            2519, 526557, 528368, 528370, 95034, 118211, 95033, 529904, 526703, 527197, 
            26641, 527576, 528422, 528480, 526467, 527978, 529195,
            528779, 95026, 529655, 92519, 526641, 526509,
            ]
    otherTrash = [ 1553331, 92518 ]

    def __init__(self, dirname):
        self.dirname = dirname
        self.xml_dirname = dirname+'/digital_entities'
        self.skipItems = self.archiv + self.archiv2 + self.archiv3 + self.mistery + \
                self.deletedPreview + self.deletedPreview2 + self.otherTrash 

    def get_attachements(self, oai_id, full=False):
        if int(oai_id) in self.skipItems:
            return
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
    
    def get_metadata(self, oai_id):
        def parseMarc(value):
            tree = ET.fromstring(value)
            for field in tree:
                if field.tag == '{http://www.loc.gov/MARC21/slim}datafield':
                    for subfield in field:
                        yield (field.attrib,subfield.text)
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
                res['marc'] = list(parseMarc(value.text))
            elif metadataType.text == 'dc':
                res['dc'] = list(parseDC(value.text))
                pass
            else:
                raise Exception("unknown format")
        return res

    def get_category(self, oai_id):
        if int(oai_id) in self.skipItems:
            return
        tree = ET.parse(self.xml_dirname+"/"+oai_id+".xml")
        root = tree.getroot()
        label = tag(tag(tag(root,"digital_entity"),"control"),"label")
        note = tag(tag(tag(root,"digital_entity"),"control"),"note")
        ingest = tag(tag(tag(root,"digital_entity"),"control"),"ingest_name")
        return (label.text,ingest.text,note.text)
