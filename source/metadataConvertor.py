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
    
    def convertDC(self, metadata1):
        metadata = {}
        for tag, value in metadata1:
            metadata.setdefault(tag,[]).append(value)
        
        if not "{http://purl.org/dc/elements/1.1/}language" in metadata.keys():
            self.categorize.categorize_item(self.oai_id, "unknown language")
        #print(metadata["{http://purl.org/dc/elements/1.1/}language"])
        #print(metadata["{http://purl.org/dc/elements/1.1/}title"])
        for tag, value in metadata.items():
            if tag == "{http://purl.org/dc/elements/1.1/}type":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}format":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}identifier":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}language":
                pass
            elif tag == "{http://purl.org/dc/terms/}isPartOf":
                pass
            elif tag == "{http://purl.org/dc/terms/}extent":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}title":
                pass
            elif tag == "{http://purl.org/dc/terms/}translated":
                pass
            elif tag == "{http://purl.org/dc/terms/}alternative":
                pass
            elif tag == "{http://purl.org/dc/terms/}alternativeTranslated":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}creator":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}subject":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}description ":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}publisher ":
                pass
            elif tag == "{http://purl.org/dc/terms/}advisor":
                pass
            elif tag == "{http://purl.org/dc/terms/}referee ":
                pass
            elif tag == "{http://purl.org/dc/terms/}created":
                pass
            elif tag == "{http://purl.org/dc/terms/}dateAccepted":
                pass
            elif tag == "{http://purl.org/dc/terms/}name":
                pass
            elif tag == "{http://purl.org/dc/terms/}level":
                pass
            elif tag == "{http://purl.org/dc/terms/}discipline":
                pass
            elif tag == "{http://purl.org/dc/terms/}grantor":
                pass
            elif tag == "{http://purl.org/dc/elements/1.1/}collection":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}rights":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}description":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}studyID":
                 pass
            elif tag == "{http://purl.org/dc/terms/}dateofbirth":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}publisher":
                 pass
            elif tag == "{http://purl.org/dc/terms/}decriptionAbstract":
                 pass
            elif tag == " {http://purl.org/dc/terms/}referee":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}status":
                 pass
            elif tag == "{http://purl.org/dc/terms/}tableOfContents":
                 pass
            elif tag == "{http://purl.org/dc/terms/}abstract":
                 pass
            elif tag == " {http://purl.org/dc/elements/1.1/}contributor":
                 pass
            elif tag == "{http://purl.org/dc/terms/}referee":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}date":
                 pass
            elif tag == "{http://purl.org/dc/terms/}valid":
                 pass
            elif tag == "{http://purl.org/dc/terms/}available":
                 pass
            elif tag == "{http://purl.org/dc/terms/}issued":
                 pass
            elif tag == "{http://purl.org/dc/terms/}modified":
                 pass
            elif tag == "{http://purl.org/dc/terms/}dateCopyrighted":
                 pass
            elif tag == "{http://purl.org/dc/terms/}medium":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}contributor":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}source":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}coverage":
                 pass
            elif tag == "{http://purl.org/dc/terms/}spatial":
                 pass
            elif tag == "{http://purl.org/dc/terms/}temporal":
                 pass
            elif tag == "{http://purl.org/dc/terms/}accessRights":
                 pass
            elif tag == "{http://purl.org/dc/terms/}license":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}thesisDegree":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}contributor":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}source":
                 pass
            elif tag == "{http://purl.org/dc/terms/}isReplacedBy":
                 pass
            elif tag == "{http://purl.org/dc/terms/}provenance":
                 pass
            elif tag == "{http://purl.org/dc/terms/}educationLevel":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}relation":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}link":
                 pass
            elif tag == "{http://purl.org/dc/terms/}isVersionOf":
                 pass
            elif tag == "{http://purl.org/dc/terms/}hasVersion":
                 pass
            elif tag == "{http://purl.org/dc/terms/}replaces":
                 pass
            elif tag == "{http://purl.org/dc/terms/}requires":
                 pass
            elif tag == "{http://purl.org/dc/terms/}hasPart":
                 pass
            elif tag == "{http://purl.org/dc/terms/}isReferencedBy":
                 pass
            elif tag == "{http://purl.org/dc/terms/}references":
                 pass
            elif tag == "{http://purl.org/dc/terms/}isFormatOf":
                 pass
            elif tag == "{http://purl.org/dc/terms/}hasFormat":
                 pass
            elif tag == "{http://purl.org/dc/terms/}conformsTo":
                 pass
            elif tag == "{http://purl.org/dc/terms/}audience":
                 pass
            elif tag == "{http://purl.org/dc/terms/}provenance":
                 pass
            elif tag == "{http://purl.org/dc/terms/}rightsHolder":
                 pass
            elif tag == "{http://purl.org/dc/terms/}dateSubmitted":
                 pass
            elif tag == "{http://purl.org/dc/terms/}mediator":
                 pass
            elif tag == "{http://purl.org/dc/terms/}educationLevel":
                 pass
            elif tag == "{http://purl.org/dc/terms/}bibliographicCitation":
                 pass
            elif tag == "{http://purl.org/dc/terms/}isRequiredBy":
                 pass
            elif tag == "{http://purl.org/dc/elements/1.1/}ins":
                 pass
            else:
                raise Exception("Unknown tag {}.".format(tag))

