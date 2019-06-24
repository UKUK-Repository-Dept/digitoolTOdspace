import re

class MetadataConvertor:
    
    def __init__(self, categorize):
        self.categorize = categorize
    
    typesDC = [ 
            '{http://purl.org/dc/elements/1.1/}title', # na konci je všude [rukopis], před tím to je ok
            '{http://purl.org/dc/elements/1.1/}creator', #vice hodnot katedry by šlo teoreticky třídit
            '{http://purl.org/dc/elements/1.1/}type', # viz type_type, ale neoveřené bo kodování
            '{http://purl.org/dc/elements/1.1/}date', # rok 2002 nebo [2002]
            '{http://purl.org/dc/elements/1.1/}publisher', # většinou Praha, občas jiné město občas bordel
            '{http://purl.org/dc/elements/1.1/}language', # cajk pár hodnot
            '{http://purl.org/dc/elements/1.1/}description', #totalně růné mnoho tisiciznakových
            '{http://purl.org/dc/elements/1.1/}subject', #někdy keywords, někdy fakulta, někdy 'bakalářská práce'
            '{http://purl.org/dc/elements/1.1/}identifier', #dva typy odkazů
            '{http://purl.org/dc/elements/1.1/}rights', # u 17 objektů, něco z toho nejsou regulerni stringy
            '{http://purl.org/dc/elements/1.1/}relation',# jen jednou - odpad
            ]
    type_tyes = [
            'text',
            'dizertace',
            'manuscriptext',
            'manuscripttext',
            'diplomovÃ© prÃ¡cefd132022czenas',
            'rigorÃ³znÃ­ prÃ¡cefd132407czenas',
            'bakalÃ¡ÅskÃ© prÃ¡cefd132403czenas',
            'zÃ¡vÄ<U+009B>reÄ<U+008D>nÃ© prÃ¡ce',
            'habilitaÄ<U+008D>nÃ­ prÃ¡ce',
            ]
    language_values = [ 'cze', 'ger', 'eng', 'slo', 'fre', 'pol' ]
    example_return = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Pokus" } 
                ]}
    
    thesisName = [ "Mgr.","Bc.","PhDr.","PhD.","PhDr","Doc.","ThDr.",'RNDr.', 'MUDr.','JUDr.','ThD.' ]
    thesisNameConvert = {
            'Mgr': 'Mgr.',
            'Phdr.': 'PhDr.',
            'Mgr,': 'Mgr.',
            'Bc..': 'Bc.',
            'mgr.': 'Mgr.',
            'Phd.': 'PhD.',
            'Mgt.': 'Mgr.',
        }
    thesisLevel = {
        "Diplomová práce":"TODO",
        "Bakalářská práce":"TODO",
        "Rigorózní práce":"TODO",
        "Habilitační práce":"TODO",
        "Dizertační práce":"Doktorský",
        }
    thesisGrantorFaculty = {
        'Filozofická fakulta',
        'Filozoficko-historická fakulta',
        'Fakulta sociálních věd a publicistiky',
        'Fakulta sociálních věd',
        'Pedagogická fakulta',
        'Fakulta humanitních studií',
        'Husova evangelická bohoslovecká fakulta', #TODO vážně všechny tři?
        'Husova československá evangelická fakulta',
        'Husova československá evangelická fakulta bohoslovecká',
        'Komenského evangelická bohoslovecká fakulta',
        'Komenského bohoslovecká fakulta v Praze',
        'Evangelická teologická fakulta',
        'Matematicko-fyzikální fakulta',
        '1 lékařská fakulta',
        '2 lékařská fakulta',
        '3 lékařská fakulta',
        }

    preconvert = {
        "81846": 'Diplomová & Rigorózní práce--Univerzita Karlova. Filozofická fakulta. Katedra psychologie, 2000',
        '74098': 'Diplomová práce (Mgr.)--Univerzita Karlova. Filozofická fakulta. Katedra sociologie, 1997',
        '98661': 'Bakalářská práce (Bc.)--Univerzita Karlova. 2. lékařská fakulta, 2004',
        '17196': 'Diplomová & Rigorózní práce--Univerzita Karlova. Matematicko-fyzikální fakulta, 2004',
        '62940': 'Diplomová & Rigorózní práce—Univerzita Karlova. Filozofická fakulta. Katedra psychologie,1998',
        '89739': 'Rigorózní práce (PhDr.)--Univerzita Karlova. Filozofická fakulta. Ústav informačních studií a knihovnictví, 2005',
        '81829': 'Diplomová & Rigorózní práce--Univerzita Karlova. Filozofická fakulta. Katedra psychologie, 1999'
        }

    def convertType(self, tag502, oai_id):
        #TODO Diplomová práce (Bc.)
        def convertTypeCorrect(tag502):
            itemClass, origin = tag502.split("--")
            itemClass = itemClass.strip()
            level, name = itemClass.split('(')
            level = level.strip()
            if not level in self.thesisLevel.keys():
                raise Exception("Unknown thesis level {}".format(level))
            name = name[:-1].strip()
            if name in self.thesisNameConvert.keys():
                name = self.thesisNameConvert[name]
            if not name in self.thesisName:
                raise Exception("Unknown title {}".format(thesisName))
            origin, year = origin.split(",")
            year = year.strip()
            assert 1919 < int(year) < 2007
            origin = origin.strip()
            if "Univerzita Karlova. " == origin[:20]:
                origin = origin[20:]
            if '.' in origin:
                faculty, department = origin.split(".",1)
            else:
                faculty, department = origin, None
            if not faculty in self.thesisGrantorFaculty:
                raise Exception("Unknown faculty {}".format(faculty))
            #print('hurá',itemClass, faculty, department, year)
        
        if tag502 == []:
            pass #TODO
            return
        elif oai_id in self.preconvert:
            tag502 = [self.preconvert[oai_id]]
        elif oai_id in ['67121', '69887', '71407' ]:
            pass #TODO potřebují ruční zásah
            return
        elif oai_id in [ '74355', '59305', '67481' ]:
            return # nesmyslný rok TODO
        elif oai_id in [ '75140', '77462', '77463'  ]:
            return # nesmyslná fakulta či katedra
        elif len(tag502) == 1 and tag502[0] == 'Diplomová práce':
            pass #TODO
            return
        elif tag502[0] == 'Diplomová práce':
            tag502=tag502[1:]
        elif len(tag502) > 1 and tag502[1] == 'Diplomová práce':
            tag502=tag502[:1]
        elif len(tag502) > 1 and tag502[1] == tag502[0]:
            tag502=tag502[:1]
        #print(oai_id,tag502)
        assert len(tag502) == 1
        tag = tag502[0].strip()
        if not "--" in tag:
            tag = tag.replace('-','--',1)
            tag = tag.replace('—','--',1)
            tag = tag.replace('–','--',1)
        tag = tag.replace('. .','.',1)
        tag = tag.replace('Univerzita .','Univerzita Karlova.',1)
        tag = tag.replace('Uverzita','Univerzita',1)
        tag = tag.replace('Univerzita karlova.','Univerzita Karlova.',1)
        tag = tag.replace('Univerzita Karlova,','Univerzita Karlova.',1)
        tag = tag.replace('Univerzita Karlova.F','Univerzita Karlova. F',1)
        tag = tag.replace('Univerzita Karlova v Praze.','Univerzita Karlova.',1)
        tag = tag.replace('Univerzita Karlova. Univerzita Karlova.','Univerzita Karlova.',1)
        tag = tag.replace('Univerzita Karlova. Katedra psychologie','Univerzita Karlova. Filozofikcá fakulta. Katedra psychologie',1)
        tag = tag.replace('Univerzita Karlova. Katedra věd o zemích Asie a Afriky','Univerzita Karlova. Filozofikcá fakulta. Katedra věd o zemích Asie a Afriky',1)
        tag = tag.replace('Univerzita Karlova. Katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
        tag = tag.replace('Univerzita Karlova. katedra andragogiky a personálního řízení','Univerzita Karlova. Filozofikcá fakulta. Katedra andragogiky a personálního řízení',1)
        tag = tag.replace('Univerzita Karlova. Institut mezinárodních studií','Univerzita Karlova. Fakulta sociálních věd. Institut mezinárodních studií',1)
        tag = tag.replace('Filozofikcá','Filozofická',1)
        tag = tag.replace('Filozofciká','Filozofická',1)
        tag = tag.replace('Filozoficka','Filozofická',1)
        tag = tag.replace('Filozofivká','Filozofická',1)
        tag = tag.replace('Fiolozofická','Filozofická',1)
        tag = tag.replace('telogická','teologická',1)
        tag = tag.replace('fakulta,','fakulta.',1)
        tag = tag.replace('fakzulta.','fakulta.',1)
        tag = tag.replace('1. lékařská', '1 lékařská')
        tag = tag.replace('2. lékařská', '2 lékařská')
        tag = tag.replace('3. lékařská', '3 lékařská')
        tag = tag.replace('Disert', 'Dizert')
        tag = tag.replace('Dizertace', 'Dizertační práce')
        tag = tag.replace('Disetační', 'Dizertační')
        tag = tag.replace('Dizertá', 'Dizerta')
        try: 
            1919 < int(tag[-4:]) < 2007
        except:
            return #TODO
        if ". " == tag[-6:-4]:
            tag = tag[:-6] + ", " + tag[-4:]
        if "a." == tag[-6:-4]:
            tag = tag[:-6] + "a, " + tag[-4:]
        if "a " == tag[-6:-4]:
            tag = tag[:-6] + "a, " + tag[-4:]
        if "e " == tag[-6:-4]:
            tag = tag[:-6] + "e, " + tag[-4:]
        if ",," == tag[-6:-4]:
            tag = tag[:-6] + ", " + tag[-4:]
        try:
            return convertTypeCorrect(tag)
        except:
            #print(oai_id, tag502)
            pass #TODO

    def convertYear(self, year):
        if year[0] == '[':
            year = year[1:]
        if len(year) > 4 and year[-1] == ']':
            year = year[:-1]
        if len(year) > 4 and year[4] == '?':
            year = year[:-1]
        if 'prosinec ' in year:
            year = year[9:]
        if 'jen' in year:
            year = year[8:]
        assert len(year) == 4
        assert int(year) > 1919
        assert int(year) < 2019
        return year

    def convertMarc(self, metadata, oai_id):
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
        self.convertType(hui,oai_id)
        return converted

    def convertDC(self, record, oai_id):
        for tag, value in record:
            if 'date' in tag:
                if oai_id in ['77317','77441','71436','75970']: # TODO špatné metadata
                    continue
                year = self.convertYear(value)
            if 'language' in tag:
                assert value in self.language_values
            if 'description' in tag:
                pass
                #if len(value) > 300:
                #    print(oai_id,len(value))
            #if 'relation' in tag:
            #    print(oai_id,len(value))
            #    print(value)
        return self.example_return
    

    typesRecord = [ 
            '{http://purl.org/dc/elements/1.1/}title', 
            '{http://purl.org/dc/elements/1.1/}creator', 
            '{http://purl.org/dc/elements/1.1/}type', 
            '{http://purl.org/dc/elements/1.1/}date', 
            '{http://purl.org/dc/elements/1.1/}publisher', 
            '{http://purl.org/dc/elements/1.1/}language', 
            '{http://purl.org/dc/elements/1.1/}description', 
            '{http://purl.org/dc/elements/1.1/}subject', 
            '{http://purl.org/dc/elements/1.1/}identifier', 
            '{http://purl.org/dc/elements/1.1/}rights', 
            '{http://purl.org/dc/elements/1.1/}relation',
            '{http://purl.org/dc/elements/1.1/}source',
            '{http://purl.org/dc/elements/1.1/}format',
            '{http://purl.org/dc/elements/1.1/}contributor',
            '{http://purl.org/dc/elements/1.1/}coverage',
            ]
    def convertRecord(self, record, oai_id):
        for tag, value in record:
            if tag == '{http://purl.org/dc/elements/1.1/}title': 
                #print(value) # více hodnot, nadpis a mnoho []
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}creator': 
                #print(value) # sousta prázdných
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}type': 
                #print(value) #stejne jako DC
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}date': 
                #print(value) #soupousta prazdnych pár celých datumu 
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}publisher': 
                #print(value) # většinou Univerzita Karlova v Praze, sem tam None, fakulta
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}description': 
                #print(value) # abscract nebo description nebo None 
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}subject': 
                #print(value) # keywords, knivoni zarazeni, příjmeni, None
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}identifier': 
                #print(value) # většinou None někdy 0361-5235
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}rights': 
                #print(value) # 99%None sem tam Karlova universita
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}relation':
                #print(value) # nazev journalu nebo None 
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}source':
                #print(value) # většinou None sem tam 14260/13
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}format':
                #print(value) # None application.pdf 871-876 1-12
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}contributor':
                #print(value) # jméno či None
                pass
            elif tag == '{http://purl.org/dc/elements/1.1/}coverage':
                #print(value) # None
                pass
            else:
                raise Exception("Unknown tag")
        return self.example_return

    def printMetadata(self,metadata):
        for tag, value in metadata:
            print(tag, value)
