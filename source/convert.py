
origin = {
        '.': ['. .'],
        '. F': ['.F'],
        'fakulta.': ['fakulta,', 'fakzulta.', 'práce.','fakultadgg','fakulta v Praze','fakluta'],
        'Katedra': [ 'Kateda', 'katedra', 'Katerdra', 'Katerda', 'Katdra', 'Katedrar', 'Katedta' ],
        'Univerzita Karlova.': [ 
            'Univerzita Karlova,', 'Univerzita Karlova v Praze.', 
            'Univerzita Karlova v Praze,', 'Univerzita Karlova V Praze.', 
            'Univerzita Karlova. Univerzita Karlova.', 
            'Univerzita .', 'Uverzita Karlova.', 'Univerzita karlova.', 
            'Univerzita Karlova (Praha).', 'Univerzita Karlova. (Praha)', 'Uverzita Karlova.',
            'Univerzita karlova.', 'Univerzita Karlova .',
            'Karlova univerzita.', 'Karlova Univerzita.','Karlova Univerzita v Praze.',
            ],
        ' lékařská': ['. lékařská'], #odstraňuju tečky z lekařských fakult abych mohla parsovat #TODO vrátit

        '1 lékařská fakulta': ['Lékařská fakulta. 1'],
        '2 lékařská fakulta': ['Lékařská fakulta. 2'],
        '3 lékařská fakulta': ['Lékařská fakulta. 3'],
        'teologická': ['telogická', 'teologická','teol,ogická'],
        'Filozofická': ['Filozofikcá', 'Filozofciká', 'Filozoficka', 'Filozofivká', 'Fiolozofická','Filizofická'],
        'psychologie': ['psyvhologie', 'psychlogie', 'pésychologie', 'psychologie', 
            'pdychologie','psachologie','psycholigie','Psychologie','psychologie (1951-1975)','psycholohie',
            'pychologie', 
            'sociální psychologie', #vyčteno z metadatad 69891, že je to spiš překlep než jiná katedra
            'obecné a pedagogické psychologie' # vyčena z 711171
            ],
        'andragogiky a ': ['nadragogiky a ','andragogika '],
        'sociologie': ['socioloogie'],
        'Fakulta sociálních věd': ['Faculty of Social Sciences'],
        'Matematicko': ['Matemeticko'],
        'humanitních ': ['humanitní '],
        'Evangelická': ['Evangelikcá'],
        'Katedra pastorační a sociální práce': [
            'Sociální a pastorační fakulta',
            'Sociální a pastorační činnost',
            'Sociální a pastorační práce',
            'Sociálaní a pastorační fakulta',
            ]
        }

title = {
        '(Bc.)': ['(Bc..)'], 
        '(Mgr.)': ['(Mgr)', '( Mgr)', '(Mgr,)', '(Mgr,.)', '(Mgr..)', '(Mgt.)', '(mgr.)',],
        '(PhD.)': ['(Phd.)'],
        '(PhDr.)': ['(Phdr.)'],
        }

degree = {
    'dp': "Diplomová práce",
    'bc': "Bakalářská práce",
    'rg': "Rigorózní práce",
    'hb': "Habilitační práce",
    'dz': "Dizertační práce",
        }

degreeTypo = {
    "Diplomová práce": [ "Diplomové práce", ],
    "Bakalářská práce": [ "Bakalářské práce", ],
    "Dizertační práce": [ "Disertace","Dizertace", "Disertační práce" ],
    "Rigorózní práce": [ "Závěrečné práce", "Rigorozní práce"  ],
    }
