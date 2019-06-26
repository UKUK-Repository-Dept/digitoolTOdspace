import re
from tag502 import convertRealTag502

class Metadata:
    
    example_return = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Pokus" } 
                ]}
    
    def __init__(self, categorize, oai_id):
        self.categorize = categorize
        self.oai_id = oai_id
        metadata = {}
    
    def convertMarc(self, metadata1):
        metadata = {}
        for tag, value in metadata1:
            if value != None:
                index = str(tag['tag'])+'-'+str(tag['ind1'])+'-'+str(tag['ind2'])
                metadata.setdefault(index,[]).append(value)
        converted = []
        hui = []
        for tags, value in metadata.items():
            #tag = tags['tag']
            if tag == '040':
                pass
            elif tag == '041':
                pass
            elif tag == '044':
                pass
            elif tag == '072':
                pass
            elif tag == '080':
                pass
            elif tag == '100':
                pass
            elif tag == '245':
                #print(value)
                pass
            elif tag == '246':
                pass
            elif tag == '260':
                pass
            elif tag == '264':
                pass
            elif tag == '300':
                pass
            elif tag == '336':
                pass
            elif tag == '337':
                pass
            elif tag == '338':
                pass
            elif tag == '340':
                pass
            elif tag == '440':
                pass
            elif tag == '500':
                pass
            elif tag == '502':
                hui.append(value)
            elif tag == '504':
                pass
            elif tag == '506':
                pass
            elif tag == '520':
                pass
            elif tag == '526':
                pass
            elif tag == '530':
                pass
            elif tag == '538':
                pass
            elif tag == '540':
                pass
            elif tag == '546':
                pass
            elif tag == '586':
                pass
            elif tag == '600':
                pass
            elif tag == '610':
                pass
            elif tag == '646':
                pass
            elif tag == '648':
                pass
            elif tag == '650':
                pass
            elif tag == '651':
                pass
            elif tag == '653':
                pass
            elif tag == '655':
                pass
            elif tag == '700':
                pass
            elif tag == '710':
                pass
            elif tag == '850':
                pass
            elif tag == '856':
                pass
            elif tag == '910':
                pass
            elif tag == '980':
                pass
            elif tag == '981':
                pass
            elif tag == '988':
                pass
            elif tag == '993':
                pass
            elif tag == '997':
                pass
            elif tag == '998':
                pass
            elif tag == 'FVS':
                pass
            elif tag == 'KLS':
                pass
            elif tag == 'SID':
                pass
            elif tag == 'KVS':
                pass
            else:
                pass
                #raise Exception("Unknown tag {}".format(tag))
        if not '502- - ' in metadata.keys():
            error_msg = "No tag 502"
            self.categorize.categorize_item(self.oai_id,error_msg)
            return
        convertRealTag502(metadata['502- - '],self.oai_id,self.categorize)
        return converted


    # seznam už ověřených / pročištěných
    # transtledet je vždy ten druhý z (en,cz)
    # subject je keywords a '53 - Fyzika' TODO nechat tam?, přidat description? (ve kterém je zadání) 
    # dayAccepted, abscract, name nejsou všude přestože jsou povinné
    # contributor není vyplněn místo toho je advisor a referee
    # do modified vyplnit vlastní datum
    # dc:type vyplnit i pro přílohy
    # identifier je třeba překopat - handle
    # degree vůbec neexistuje
    dcParsed = '''
{http://purl.org/dc/elements/1.1/}language
{http://purl.org/dc/elements/1.1/}title
{http://purl.org/dc/terms/}translated
{http://purl.org/dc/terms/}alternative
{http://purl.org/dc/terms/}alternativeTranslated
{http://purl.org/dc/elements/1.1/}creator
{http://purl.org/dc/elements/1.1/}subject
{http://purl.org/dc/terms/}abstract
{http://purl.org/dc/terms/}advisor
{http://purl.org/dc/terms/}referee
{http://purl.org/dc/terms/}dateAccepted
{http://purl.org/dc/elements/1.1/}type
{http://purl.org/dc/terms/}name
'''
    #tagy mimo evskp
    dcBonus = '''
{http://purl.org/dc/terms/}dateofbirth
{http://purl.org/dc/elements/1.1/}description
'''
    # věci komplet špatně vyplněné či jinak nehodnotné
    dcSkipped = '''
{http://purl.org/dc/elements/1.1/}identifier
{http://purl.org/dc/elements/1.1/}rights
{http://purl.org/dc/elements/1.1/}collection
{http://purl.org/dc/elements/1.1/}studyID
{http://purl.org/dc/elements/1.1/}status
'''
    # publisher & grantor - dělení na fakulty, je vždy stejné?
    # created má občas /
    # medium&formát zkontrolovat podle příloh
    # level a discipline potřebuje učesat a i s type zkontrolovat
    dcTODO = '''
{http://purl.org/dc/elements/1.1/}publisher
{http://purl.org/dc/terms/}grantor
{http://purl.org/dc/terms/}created
{http://purl.org/dc/terms/}medium
{http://purl.org/dc/elements/1.1/}format
{http://purl.org/dc/terms/}level
{http://purl.org/dc/terms/}discipline
'''
    def convertDC(self, metadata1): #14653
        metadata = {}
        for tag, value in metadata1:
            if value != None:
                metadata.setdefault(tag,[]).append(value)
        
        if metadata == {}:
            self.categorize.categorize_item(self.oai_id, "No metadata")
            return
        
        tag = '{http://purl.org/dc/elements/1.1/}title'
        if not tag in metadata.keys():
            self.categorize.categorize_item(self.oai_id, "No title") 
            return
        assert len(metadata[tag]) == 1
        if 'Plán' in metadata[tag][0]:
            self.categorize.categorize_item(self.oai_id, "Mapa nikoliv kvalifikační práce") 
            return
        if 'Test LDAP' in metadata[tag][0] or 'Testovaci' in metadata[tag][0]:
            self.categorize.categorize_item(self.oai_id, "Testovací objekt - smazat.") 
            return
        #print(metadata[tag]) #TODO cca tři blbosti
        
        tag = '{http://purl.org/dc/terms/}abstract'
        if tag in metadata.keys() and metadata[tag] == ['abstract']:
            #tohle všechno jsou nesmysly nebo špatně zařazené věci
            self.categorize.categorize_item(self.oai_id, "Abstract is 'abstract'") 
            return
        
        tag = "{http://purl.org/dc/elements/1.1/}language" 
        if not tag in metadata.keys():
            self.categorize.categorize_item(self.oai_id, "unknown language")
            return
        assert len(metadata[tag]) == 1
      
        # jazkyk v tagu a jazyk titulku letmým pohledem sedí - HURÁ
        #print(metadata[tag][0],metadata['{http://purl.org/dc/elements/1.1/}title'])
        

        tag = '{http://purl.org/dc/elements/1.1/}type'
        tag2 = '{http://purl.org/dc/terms/}name'
        if not tag in metadata.keys():
            if tag2 in metadata.keys():
                if metadata[tag2][0] == 'Mgr.':
                    metadata[tag] = 'diplomová práce'
            self.categorize.categorize_item(self.oai_id, "unknown type of work")
            return
        assert len(metadata[tag]) == 1
        if metadata[tag][0] in ['bakalářksá práce']:
            metadata[tag][0] = 'bakalářská práce'
        if metadata[tag][0] in ['magisterská práce','diplomové práce','diplomová príce']:
            metadata[tag][0] = 'diplomová práce'
        if metadata[tag][0] in ['doktorská práce','disertační práce']:
            metadata[tag][0] = 'dizertační práce'
        if metadata[tag][0] == 'článek':
            self.categorize.categorize_item(self.oai_id, "článek není závěrečná práce")
            return
        if not metadata[tag][0] in ['bakalářská práce','diplomová práce', 'dizertační práce', 'rigorózní práce']:
            self.categorize.categorize_item(self.oai_id, "unknown type of work")
            return
        
            #print(metadata)
            #print(metadata[tag])


        tag = '''
{http://purl.org/dc/elements/1.1/}contributor
        '''
        tag = tag.strip('\n').strip()
        if tag in metadata.keys():
            print('!!!!',metadata[tag])
        
        for tag in metadata.keys():
            if not tag in (self.dcParsed + self.dcBonus + self.dcTODO +  self.dcSkipped).split('\n'):
                print(tag)
                #raise Exception("Unknown tag {}.".format(tag))

