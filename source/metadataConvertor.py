import re
from tag502 import convertTag502
from tag245 import convertTag245
import catalogue
import otherTag
import dublinCore

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

    def __getMetadata(self, name, allTags):
        result  = None
        for tag in allTags:
            if name in allTags[tag].keys():
                if result and result != allTags[tag][name]:
                    #TODO zaniklé faktuly kde se tvořilo vs ty kde se digitalizovalo
                    #TODO 143 neshodujících se jmen půl napůl chyby a ekvivalentní zápisy
                    #TODO 51 dizectanční vs rigorozní vs bakalářská 
                    error_msg = 'Different {} "{}" "{}"'.format(name, result, allTags[tag][name])
                    self.categorize.categorize_item(self.oai_id,error_msg)
                    #if name == 'degree':
                    #    print(error_msg)
                    #raise Exception(error_msg)
                result = allTags[tag][name]
        return result
                


    def convertMarc(self, metadata):
        #for key in metadata.keys():
        #    for key2 in metadata.keys():
        #        if key[:3] == key2[:3] and key != key2:
        #            print(key, key2)
        ret = {}

        # diplomkový speciál
        #TODO z 502 by šlo vytáhnout víc informaci
        if not '502- - ' in metadata.keys():
            error_msg = "No tag 502"
            self.categorize.categorize_item(self.oai_id,error_msg)
        else:
            ret502 = convertTag502(metadata['502- - '],self.oai_id,self.categorize)
            if ret502:
                ret['502'] = ret502

        for tag in metadata.keys():
            if tag[:3] == '245': # titek, autor
                tag245 = metadata[tag]
                ret['245'] = convertTag245(tag245,self.oai_id,self.categorize)
            if tag[:3] == '710': # fakulta, katedra
                tag710 = metadata[tag]
                ret['710'] = otherTag.convertTag710(tag710, self.oai_id, self.categorize)
            if tag[:3] == '100': # autor
                ret['100'] = otherTag.convertTag100(metadata[tag], self.oai_id, self.categorize)
            if tag[:3] == '981': # degree
                ret['981'] = otherTag.convertTag981(metadata[tag], self.oai_id, self.categorize)
            if tag[:3] == '655': # degree TODO
                ret['655'] = otherTag.convertTag655(metadata[tag], self.oai_id, self.categorize)
        
        for tag in metadata.keys(): #TODO
            #>3000
            #if tag[:3] == '040': #př {'a': ['ABD001'], 'b': ['cze'], 'c': ['ABD001'], 'd': ['ABD001']}
            #if tag[:3] == 'SID': # vždy {'a': ['Z39'], 'b': ['CKS01']}
            #if tag[:3] == '260': # TODO místo vydání, rok nízká míra bordelu
            #if tag[:3] == '910': # př  {'a': ['ABD107']}  
            #if tag[:3] == '300': # počet stran vysoká míra bordelu př  {'a': ['131 s. :'], 'b': ['příl.']} {'a': ['Obsahuje bibliografii na s. 123 - 140, tab., grafy, příl.']}
            #>2000
            #if tag[:3] == '980': # př (vždy?) {'a': ['application.pdf']}
            #if tag[:3] == '700': # TODO jména, roky a další
            #>1000
            #if tag[:3] == '500': # strany s literaturou, 'Příl.', a hrozně moc bordelu
            #if tag[:3] == '650': # keywords; střední míra bordelu
            #if tag[:3] == '504': # strany s literaturou a nesourodý formát
            #>50 (jen výběr zajímavějších)
            #if tag[:3] == '520': # abstrakt
            #if tag[:3] == '041': # jazyk
            #if tag[:3] == '246': # titulek v překladu?  
            #if tag[:3] == '072': # téma - přidat do keywords?
            #if tag[:3] == '653': # keywords  
            #if tag[:3] == '526': # studijní obor  
            #if tag[:3] == '586': # známka 
            if False:  
                print(tag, metadata[tag])
        
        faculty = self.__getMetadata('faculty', ret)
        if not faculty: 
            pass #TODO 40 kousků, ale některé mají 650, či ingest
        
        author = self.__getMetadata('author', ret)
        if not author: 
            raise Exception('No author')
        
        self.degree = self.__getMetadata('degree', ret)
        if not self.degree: 
            pass #print(self.oai_id) #TODO  19 záznamů

        for tag in metadata.keys():
            pass #TODO ručně vytvořen soubor cetnostiTagu
            #python3 source/digitoolTOdspace.py categorize --group marc --no-output| sort | uniq -c | sort -k 1 -g
            #print(tag)
