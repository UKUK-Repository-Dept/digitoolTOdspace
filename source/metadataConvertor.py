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
    
    def convertMarc(self, metadata):
        converted = []
        hui = []
        for tags, value in metadata:
            tag = tags['tag']
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
                raise Exception("Unknown tag {}".format(tag))
        convertRealTag502(hui,self.oai_id,self.categorize)
        return converted
            
    dcParsed = '''
{http://purl.org/dc/elements/1.1/}language
{http://purl.org/dc/elements/1.1/}title
{http://purl.org/dc/terms/}translated
{http://purl.org/dc/terms/}alternative
{http://purl.org/dc/terms/}alternativeTranslated
'''
    dcSkipped = '''
{http://purl.org/dc/terms/}abstract
{http://purl.org/dc/terms/}isPartOf
{http://purl.org/dc/terms/}extent
{http://purl.org/dc/elements/1.1/}collection
{http://purl.org/dc/terms/}issued
{http://purl.org/dc/elements/1.1/}type
{http://purl.org/dc/elements/1.1/}format
{http://purl.org/dc/elements/1.1/}identifier
{http://purl.org/dc/elements/1.1/}creator
{http://purl.org/dc/elements/1.1/}contributor
{http://purl.org/dc/elements/1.1/}subject
{http://purl.org/dc/terms/}issued
{http://purl.org/dc/terms/}name
{http://purl.org/dc/terms/}level
{http://purl.org/dc/terms/}grantor
{http://purl.org/dc/elements/1.1/}collection
{http://purl.org/dc/elements/1.1/}studyID
{http://purl.org/dc/elements/1.1/}publisher
{http://purl.org/dc/terms/}advisor
{http://purl.org/dc/terms/}created
{http://purl.org/dc/terms/}dateAccepted
{http://purl.org/dc/terms/}dateofbirth
{http://purl.org/dc/elements/1.1/}description
{http://purl.org/dc/terms/}discipline
{http://purl.org/dc/terms/}referee
{http://purl.org/dc/elements/1.1/}status
{http://purl.org/dc/elements/1.1/}rights
{http://purl.org/dc/terms/}medium
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
        print(metadata[tag][0],metadata['{http://purl.org/dc/elements/1.1/}title'])

        tag = '{http://purl.org/dc/terms/}translated'
        if tag in metadata.keys():
            pass #skutečne překlad titulku (druhý jazky z en, cz)

        tag = '{http://purl.org/dc/terms/}alternative'
        if tag in metadata.keys():
            pass #skutečne podtitulek

        tag = '{http://purl.org/dc/terms/}alternativeTranslated'
        if tag in metadata.keys():
            pass #skutečne překlad podtitulku (druhý jazky z en, cz)

        for tag in metadata.keys():
            if not tag in (self.dcParsed + self.dcSkipped).split('\n'):
                raise Exception("Unknown tag {}.".format(tag))

