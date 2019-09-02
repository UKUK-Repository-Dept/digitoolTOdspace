
def convertTag246(tag246,oai_id,categorize):
    ret = {}
    if 'b' in tag246.keys():
        ret['alternative'] = "{} {}".format(tag246['a'][0],tag246['b'][0])
    else:
        ret['alternative'] = tag246['a'][0]
    return ret

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
