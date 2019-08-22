import xml.etree.ElementTree as ET

def openAleph(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    records = []
    for record in root:
        metadata = {}
        for field in record:
            if field.tag in ['{http://www.loc.gov/MARC21/slim}datafield','{http://www.loc.gov/MARC21/slim}controlfield']:
                for subfield in field:
                    tag = field.attrib
                    index = str(tag['tag'])+'-'+str(tag['ind1'])+'-'+str(tag['ind2'])
                    if subfield.text != None:
                        code = subfield.attrib['code']
                        metadata.setdefault(index,{})
                        metadata[index].setdefault(code,[])
                        metadata[index][code].append(subfield.text)
            else:
                pass
        records.append(metadata)
    return records
