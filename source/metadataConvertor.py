import re
import tag502, tag245, otherTag
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
        for tag in self.metadata:
            if not name in  self.metadata[tag].keys():
                continue
            if result and result != self.metadata[tag][name]:
                error_msg = 'Different {} "{}" "{}"'.format(name, result, self.metadata[tag][name])
                self.categorize.categorize_item(self.oai_id,error_msg)
            result = self.metadata[tag][name]
        return result

    def convertMarc(self, metadata):
        ret = {}

        mandatory = {
                '502':tag502.convertTag502, #kvalifikační práce
                '100':otherTag.convertTag100, #autor
                '245':tag245.convertTag245, #titul,autor
                #'260':otherTag.convertTag260, #místo vydání (vyhazovat jen překlepy)
                '710':otherTag.convertTag710, #fakulta, katedra
                }
        for tag in mandatory.keys():
            if not tag in metadata.keys():
                error_msg = "No tag {} in metadata".format(tag)
                self.categorize.categorize_item(self.oai_id,error_msg)
                return
            ret = mandatory[tag](metadata[tag], self.oai_id, self.categorize)
            if ret == None: #TODO smazat to jsou categorize veci
                return
            self.metadata[tag] = ret


        for tag in metadata.keys():
            if tag[:3] == '981': # degree
                ret['981'] = otherTag.convertTag981(metadata[tag], self.oai_id, self.categorize)
            if tag[:3] == '655': # degree TODO
                ret['655'] = otherTag.convertTag655(metadata[tag], self.oai_id, self.categorize)
        
        for tag in metadata.keys(): #TODO
            #>3000
            # zjevne preklepy
            #if tag[:3] == '260': # TODO místo vydání, rok nízká míra bordelu
            #>50 (jen výběr zajímavějších)
            #if tag[:3] == '520': # abstrakt
            #if tag[:3] == '041': # jazyk
            #if tag[:3] == '246': # titulek v překladu  
            
            if False:  
                print(tag, metadata[tag])
        
        faculty = self.__getMetadata('faculty')
        if not faculty: 
            self.categorize.categorize_item(self.oai_id,"No faculty")
        
        author = self.__getMetadata('author')
        if not author: 
            raise Exception('No author')
        
        self.degree = self.__getMetadata('degree')
        if not self.degree: 
            self.categorize.categorize_item(self.oai_id,"No degre")
