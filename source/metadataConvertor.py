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

    def __getMetadata(self, tagName):
        def comparePeople(name1,name2):
            def normaliseName(name):
                name = sorted(name.replace(',','').replace('-',' ').split())
                return name
            if name1 == None:
                return True
            name1 = normaliseName(name1)
            name2 = normaliseName(name2)
            if not len(name1) == len(name2):
               return False
            for i in range(len(name1)):
                if not name1[i] == name2[i]:
                    return False
            return True


        result  = None
        resultTag = None
        for tag in self.metadata:
            if not tagName in  self.metadata[tag].keys():
                continue
            result2 = self.metadata[tag][tagName]
            error_msg = 'Different {} {}:"{}" {}: "{}"'.format(tagName, resultTag, result, tag, result2)
            personTagNames = ['author','advisor','committe','consultant']
            if tagName in personTagNames and not comparePeople(result,result2):
                # TODO ručne projít před finálním exportem
                #print(self.oai_id,error_msg)
                self.categorize.categorize_item(self.oai_id,error_msg)
            elif result and result != result2:
                self.categorize.categorize_item(self.oai_id,error_msg)
            result = result2
            resultTag = tag
        return result

    def convertMarc(self, metadata):
        self.degree = None #TODO smazat
        ret = {}
        mandatory = {
                '502': tag502.convertTag502, #kvalifikační práce
                '100': tag100.convertTag100, #autor
                '245': tag245.convertTag245, #titul, autor #TODO kontrola dle mailu od Iry, počkat na nový export 
                '260': tag260.convertTag260, #místo vydání a datum 
                '710': tag710.convertTag710, #fakulta, katedra #TODO nový mail
                }
        obligatory = {
                '700': tag700.convertTag700, # vedoucí, oponent,.. #TODO napsat
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
            self.metadata[tag] = ret
       


        faculty = self.__getMetadata('faculty')
        if not faculty: 
            self.categorize.categorize_item(self.oai_id,"No faculty")
        
        author = self.__getMetadata('author')
        if not author: 
            raise Exception('No author')
        advisor = self.__getMetadata('advisor')
        commitee = self.__getMetadata('commitee')
        advisor = self.__getMetadata('advisor')
        #TODO 'advisor' 'committe' 'consultant'


        self.degree = self.__getMetadata('degree')
        if not self.degree: 
            self.categorize.categorize_item(self.oai_id,"No degre")

        # němčina 42606, azbuka 135200
        #print(self.oai_id)
        #if self.oai_id in ['42606','135200']:
        #    print(self.metadata)
        # TODO pole 008 znak 35-37
        self.lang = self.__getMetadata('lang')
        if not self.lang:
            error_msg = "No language found in 041 and 520."
            self.categorize.categorize_item(self.oai_id,error_msg)
        #TODO lang alternative_lang
