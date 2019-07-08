import re
from tag502 import convertTag502
from tag245 import convertTag245
import catalogue
import otherTag

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
        
        degree = self.__getMetadata('degree', ret)
        if not degree: 
            pass #print(self.oai_id) #TODO  19 záznamů

        for tag in metadata.keys():
            pass #TODO ručně vytvořen soubor cetnostiTagu
            #python3 source/digitoolTOdspace.py categorize --group marc --no-output| sort | uniq -c | sort -k 1 -g
            #print(tag)


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
                raise Exception("Unknown tag {}.".format(tag))

