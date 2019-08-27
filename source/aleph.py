import xml.etree.ElementTree as ET

def openAleph(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    records = []
    for record in root:
        metadata = {}
        for field in record:
            tag = field.attrib
            if field.tag == '{http://www.loc.gov/MARC21/slim}datafield':
                #index = str(tag['tag'])+'-'+str(tag['ind1'])+'-'+str(tag['ind2'])
                index = tag['tag']
                for subfield in field:
                    if subfield.text != None:
                        code = subfield.attrib['code']
                        metadata.setdefault(index,{})
                        metadata[index].setdefault(code,[])
                        metadata[index][code].append(subfield.text)
            if field.tag == '{http://www.loc.gov/MARC21/slim}controlfield':
                index = tag['tag']
                metadata[index] = field.text
            else:
                pass
        records.append(metadata)
    return records
