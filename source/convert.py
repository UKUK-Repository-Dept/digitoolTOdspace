
origin = {
        '.': ['. .'],
        '. F': ['.F'],
        'fakulta.': ['fakulta,', 'fakzulta.', 'práce.','fakultadgg'],
        'Katedra': [ 'Kateda', 'katedra', 'Katerdra', 'Katerda', 'Katdra', 'Katedrar', 'Katedta' ],
        'Univerzita Karlova.': [ 
            'Univerzita Karlova,', 'Univerzita Karlova v Praze.', 'Univerzita Karlova. Univerzita Karlova.'
            'Univerzita .', 'Uverzita Karlova.', 'Univerzita karlova.', 
            ],
        ' lékařská': ['. lékařská'], #odstraňuju tečky z lekařských fakult abych mohla parsovat #TODO vrátit

        '1 lékařská fakulta': ['Lékařská fakulta. 1'],
        '2 lékařská fakulta': ['Lékařská fakulta. 2'],
        '3 lékařská fakulta': ['Lékařská fakulta. 3'],
        'teologická': ['telogická', 'teologická'],
        'Filozofická': ['Filozofikcá', 'Filozofciká', 'Filozoficka', 'Filozofivká', 'Fiolozofická',],
        'psychologie': ['psyvhologie', 'psychlogie', 'pésychologie', 'psychologie', 
            'pdychologie','psachologie','psycholigie','Psychologie','psychologie (1951-1975)','psycholohie',
            'pychologie', 
            'sociální psychologie', #vyčteno z metadatad 69891, že je to spiš překlep než jiná katedra
            'obecné a pedagogické psychologie' # vyčena z 711171
            ],
        'andragogiky a ': ['nadragogiky a ','andragogika '],
        'sociologie': ['socioloogie'],
        'Fakulta sociálních věd': ['Faculty of Social Sciences'],
        'Univerzita Karlova.': ['Univerzita Karlova (Praha).', 'Univerzita Karlova. (Praha)',
            'Univerzita Karlova. Univerzita Karlova.',
            'Univerzita .','Uverzita Karlova.','Univerzita Karlova v Praze.', 
            'Univerzita karlova.', 'Univerzita Karlova .', 'Univerzita Karlova,', 'Univerzita Karlova '],
        }

title = {
        '(Bc.)': ['(Bc..)'], 
        '(Mgr.)': ['(Mgr)', '( Mgr)', '(Mgr,)', '(Mgr,.)', '(Mgr..)', '(Mgt.)', '(mgr.)',],
        '(PhD.)': ['(Phd.)'],
        '(PhDr.)': ['(Phdr.)'],
        }

