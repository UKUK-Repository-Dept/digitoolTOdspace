import  tags.commonTag

def __deleteBackslash(title):
    title = title.strip()
    if title[:2] == '/ ':
        title = title[2:]
    if title[-1] == '/':
        if '/' in title[:-1]:
            if not ' /' in title[:-1]:
                title = title[:-1]
        else:
            title = title[:-1]
    return title.strip()

rules = {
        'author': ['vypracovala','vypracoval','autorka','autor:'],
        'advisor': [ 
            'supervisor', 'ved. dipl. prác', 'školitel', 'vedúci', 'ved. dipl. prcáe',
            'ved. dipl. p.', 'ved. dipl.', 'vedoucí diplomové práve', 'vedoucí diplomové',
            'vedoucí diplomové vedoucí', 'vedoucí' ],
        'committe': ['oponent práce', 'oponent','commitee'],
        'consultant': ['konzultantka práce', 'konzultanti ', 'konzult.','consultant',
            'konzultant práce','konzultant rigorózní práce', 'konzultant ', 'konzultantka ',
            ]
}

def __splitCreator(source, rules, oai_id, categorize):
    res = {}
    for part in source.split(';'):
        creatorType = None
        if part == '':
            continue
        if 'Univ' in part:
            creatorType = 'origin'
            continue # fakultu tady ignoruju #TODO porovnat až budu mit nevylněné
        for creator, tags in rules.items():
            for tag in tags: # na pořadí if záleži
                if ('ved' in part or 'škol' in part or 'Ved' in part)  and 'áce' in part:
                    creatorType = 'advisor'
                    remove = part.split('áce')[0]+'áce'
                    break
                if tag in part:
                    creatorType = creator
                    remove = tag
                    break
                if part == source.split(';')[0] and creator == 'author':
                    creatorType = 'author'
                    remove = ''
        if creatorType:
            res[creatorType] = part.replace(remove,'').strip()
        else:
            categorize.categorize_item(oai_id,"245: No creator category")
            raise Exception('no Creator category')
    return res

def convertTag245(tag245, oai_id, categorize):

    res = {}
    
    if len(tag245['a']) == 1:
        title = tag245['a'][0]
        res['title'] = __deleteBackslash(title)
    if 'b' in tag245.keys():
        alternative = tag245['b'][0]
        res['alternative'] = __deleteBackslash(alternative)
    if 'c' in tag245.keys():
        creator = tag245['c'][0]
        res.update(__splitCreator(creator, rules, oai_id, categorize))
    if 'p' in tag245.keys():
        alternative = tag245['p'][0]
    for key in tag245.keys():
        if not key in 'abchpn':
            raise Exception('Unknown key')
    

    d = [
        ('title','[diplomová práce]'),
        ('title','[rigorózní práce]'),
        ('title','[disertační práce]'),
        ('title','[1996]'),
        ('title',' -FF-'),
        ('alternative','[diplomová práce]'),
        ('alternative','[rigorózní práce]'),
        ('alternative',' -FF-'),
            ]
    for creator, delete in d:
        if creator in res:
            if delete in res[creator]:
                #if delete in res[creator]:
                #    print(oai_id,tag245)
                res[creator] = res[creator].replace(delete, '').strip()
   
    res = { k:v for k,v in res.items() if not v in ['','není uveden','neuveden'] }
    for key, value in res.items():
        if value[0] == ':':
            value = value[1:]
            #print(oai_id,tag245)
        if value[0] == '[':
            value = value[1:]
        if value[-1] == ']':
            value = value[:-1]
        res[key] = value

    if 'advisor' in res.keys() and ', konz' in res['advisor']:
        res['advisor'] = res['advisor'].split(',')[0]
    if 'author' in res.keys() and ',' in res['author']:
        if ', vedoucí ' in res['author']:
            res['author'] = res['author'].split(',')[0]
        else:
            #print(res['author']) #TODO co s rozenyma 
            pass
    for tag in ['title','alternative']:
        if tag in res.keys() and ';' in res[tag]:
            res[tag] = res[tag].split(';')[0]

    for tag in rules.keys():
        if tag in res.keys():
            res[tag] = tags.commonTag.surnameFirst(res[tag]) 

    if 'author' in res.keys():
        if 'vypracoval' in res['author']:
            print('au',tag245)
    return res
'''
tag 245
1) je správně věci níže nepřenést do dspace, ale ani nenahlásit vám?
        ('title','[diplomová práce]'),
        ('title','[rigorózní práce]'),
        ('title','[disertační práce]'),
        ('title','[1996]'),
        ('title',' -FF-'),
        ('alternative','[diplomová práce]'),
        ('alternative','[rigorózní práce]'),
        ('alternative',' -FF-'),

pole 245
ad 1) něco z toho opravime hromadne u nas, pokud to pujde. Něco jsou chyby napr. –FF-
ad 2) to muze byt v poradku. Ono pole 245 podpole c dle katalogizačních pravidel ma obsahovat to, co je na titulnim listu (coz muze způsobovat rozdil ve jmenech v poli 245 c a 100) a pripadne se tam muzou dopsat informace, které knihovnik povazuje za dulezite pro uzivatele
ad 3) Zaznam, který ma v poli 245 v podpoli a hned jako první : bude chyba. Na to se musíme podivat
ad 4) to bych ignorovala

pole 245
ad 1)
000416966 {'a': ['Klinické využití sebeposuzovací škály depresivity CDI u dětí -FF- /'], 'c': ['Jiří Štěpo ; ved. práce Marek Preiss']}
000417297 {'a': ['O žalování -FF- /'], 'c': ['Petr Bakalář ; ved. práce Jaroslav Koťa']}
...
3) koukam že není jako první, vzniklo to během mého parsování
př ['Karel Kočner ; vedoucí práce: Mireia Ryšková']
má 2x dvojtečky a všude jinde je to bez ní

Pole 245
ad 1) text –FF- jsme hromadne odstranili ze všech zaznamu v cele naší bazi. Co se tyce textu jako diplomova práce v nazvu, tak z nize uvedeného jsem to vyhodila. Celkove je to ale spis jen zbytecny udaj nez chyba, takze to v cele naší bazi opravovat nebudeme.
ad 3) opraveno. Fakticky to ale není chyba. Obecne cele pole 245 je pro strojovou kontrolu problematicke. Opisuje se tam obsah titulního listu. Krasnym prikladem toho, ze kontrola strojem pro pole 245 je problemova je podpole c a jmena. Na titulnim liste je napsane napr. Jana Novakova, rozena Stankova. Knihovnik to dle pravidel opise. Pak ale do pole 100 napise Novakova, Jana. Z pohledu katalogizace je to v poradku, ale z pohledu stroje je to logicky chyba. Takze kontroly pole 245 povazuju za ukoncene. Ještě dodelam ty jmena, která jsi posilala, část jsou preklepy, ale zbytek je v poradku a nemá smysl tim ztrácet cas.
'''
