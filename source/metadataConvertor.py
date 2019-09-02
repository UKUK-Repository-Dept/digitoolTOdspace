import re
from tags import * 
import catalogue

class Metadata:
    
    example_return = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Pokus" } 
                ]}
    metadata = {}
    
    def __init__(self, categorize, oai_id):
        self.categorize = categorize
        self.oai_id = oai_id

    def __getMetadata(self, name):
        result  = None
        resultTag = None
        for tag in self.metadata:
            if not name in  self.metadata[tag].keys():
                continue
            if result and result != self.metadata[tag][name]:
                error_msg = 'Different {} {}:"{}" {}: "{}"'.format(name, resultTag, result, tag, self.metadata[tag][name])
                self.categorize.categorize_item(self.oai_id,error_msg)
            result = self.metadata[tag][name]
            resultTag = tag
        return result

    def convertMarc(self, metadata):
        #TODO presat surnameFirst+convertOrigin
        ret = {}
        mandatory = {
                '502': tag502.convertTag502, #kvalifikační práce
                '100': tag100.convertTag100, #autor
                '245': tag245.convertTag245, #titul, autor #TODO kontrola dle mailu od Iry, počkat na nový export 
                '260': tag260.convertTag260, #místo vydání a datum 
                '710': tag710.convertTag710, #fakulta, katedra #TODO nový mail
                }
        obligatory = {
                '655': tag655.convertTag655, # druh práce #TODO ignorovat v 9/9 případů lhal
                '520': tag520.convertTag520, # abstrakt #TODO dořešit jazyky
                '041': tag041.convertTag041, # jazyk 
                '246': tag246.convertTag246, # titulek v překladu  
                '650': tag650.convertTag650, # keywords (bez kontroly obsahu) 
                }

        # Jaro potvrdil následůjící postup
        if '264' in metadata.keys():
            assert '260' not in metadata.keys()
            metadata['260'] = metadata['264']

        for tag in mandatory.keys():
            if not tag in metadata.keys():
                error_msg = "No tag {} in metadata".format(tag)
                self.categorize.categorize_item(self.oai_id,error_msg)
                return
        
        allTags = {**mandatory, **obligatory}
        for tag in allTags.keys():
            if not tag in metadata.keys():
                continue
            ret = allTags[tag](metadata[tag], self.oai_id, self.categorize)
            if ret == None: #TODO smazat, to by se děje jen při chybách
                return
            self.metadata[tag] = ret
       


        faculty = self.__getMetadata('faculty')
        if not faculty: 
            self.categorize.categorize_item(self.oai_id,"No faculty")
        
        # TODO lepši normalizace autora
        #author = self.__getMetadata('author')
        #if not author: 
        #    raise Exception('No author')
        
        self.degree = self.__getMetadata('degree')
        if not self.degree: 
            self.categorize.categorize_item(self.oai_id,"No degre")

        # němčina 42606, azbuka 135200
        self.lang = self.__getMetadata('lang')
        if not self.lang:
            error_msg = "No language found in 041 and 520."
            self.categorize.categorize_item(self.oai_id,error_msg)
        #TODO lang alternative_lang
