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
                '245': tag245.convertTag245, #titul,autor #TODO kontrola dle mailu od Iry, počkat na nový export 
                '260': tag260.convertTag260, #místo vydání a datum (vyhazovat jen překlepy) # kontrola dle mailu, počkat na nový export
                '710': tag710.convertTag710, #fakulta, katedra #TODO kontrola dle mailu, počkat na nový export
                }
        obligatory = {
                '655': tag655.convertTag655, # TODO čekám na mail
                '520': tag520.convertTag520, # abstrakt #TODO čekám na mail
                '041': tag041.convertTag041, # jazyk 
                '246': tag246.convertTag246, # titulek v překladu  
                '650': tag650.convertTag650, # keywords (bez kontroly obsahu) 
                }

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
        
        author = self.__getMetadata('author')
        if not author: 
            raise Exception('No author')
        
        self.degree = self.__getMetadata('degree')
        if not self.degree: 
            self.categorize.categorize_item(self.oai_id,"No degre")

        #TODO lang alternative_lang
