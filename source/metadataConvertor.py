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
                name = name.replace(':','')
                names = sorted(name.replace(',',' ').replace('-',' ').split())
                for name in names:
                    if 'vypracoval' in name:
                        continue
                    name = name.strip()
                    yield name
            if name1 == None:
                return True
            name1 = list(normaliseName(name1))
            name2 = list(normaliseName(name2))
            if not len(name1) == len(name2):
               return False
            for i in range(len(name1)):
                if len(name1[i]) > len(name2[i]):
                    first, second = name2[i], name1[i]
                else:
                    first, second = name1[i], name2[i]
                if len(first) == 2 and first[1] == '.' and first[0] == second[0]: 
                    continue #iniciály
                if not first == second:
                    return False
            return True


        result  = None
        resultTag = None
        for tag in self.metadata:
            if not tagName in  self.metadata[tag].keys():
                continue
            result2 = self.metadata[tag][tagName]
            error_msg = 'Different {} {}:"{}" {}: "{}"'.format(tagName, resultTag, result, tag, result2)
            personTagNames = ['author','advisor','commitee','consultant']
            if tagName in personTagNames and not comparePeople(result,result2):
                pass # TODO ručne projít před finálním exportem
                #print(self.oai_id,error_msg)
                #self.categorize.categorize_item(self.oai_id,error_msg)
            elif tagName not in personTagNames and result and result != result2:
                self.categorize.categorize_item(self.oai_id,error_msg)
            result = result2
            resultTag = tag
        return result

    def convertMarc(self, metadata):
        #if self.oai_id != '001529410,1138075':
        #    return
        self.degree = None #TODO smazat
        ret = {}
        mandatory = {
                '100': tag100.convertTag100, #autor
                '245': tag245.convertTag245, #titul, autor #TODO kontrola dle mailu od Iry, počkat na nový export 
                '260': tag260.convertTag260, #místo vydání a datum 
                '502': tag502.convertTag502, #kvalifikační práce
                #'710': tag710.convertTag710, #fakulta, katedra #TODO nový mail,povinny
                }
        obligatory = {
                '008': otherTag.convertTag008,#jazyk na pozici 35-37
                '041': tag041.convertTag041,  # jazyk 
                '246': tag246.convertTag246,  # titulek v překladu #TODO upozornit na chybějící podpole s jazykem 
                #'520': tag520.convertTag520,  # abstrakt #TODO dořešit jazyky
                #'526': otherTag.convertTag526,# předmět TODO jen devět kousku
                '600': otherTag.convertTag600,# keywords osoba
                '610': otherTag.convertTag610,# keywords organizace
                '630': otherTag.convertTag630,# keywords knihy
                '648': otherTag.convertTag648,# keywords období
                '650': tag650.convertTag650,  # keywords 
                '651': otherTag.convertTag651,# keywords zeměpis
                #'655': tag655.convertTag655,  # druh práce ignorujeme 9/9 případů lhal
                '700': tag700.convertTag700,  # vedoucí, oponent,.. #TODO roky ve stejném poli hlásit!
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
            #print(self.oai_id)
            #print(metadata)
            #print(self.metadata)
            self.categorize.categorize_item(self.oai_id,"No faculty")
        
        author = self.__getMetadata('author')
        if not author: 
            raise Exception('No author')
        advisor = self.__getMetadata('advisor')
        #TODO ruční kontrola
        #if '700' in self.metadata.keys() and 'advisor' in self.metadata['700'] and not 'advisor' in self.metadata['245']:
        #    print('700')
        commitee = self.__getMetadata('commitee')
        consultant = self.__getMetadata('consultant')
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
