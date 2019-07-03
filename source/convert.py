
origin = {
        '.': ['. .'],
        '. F': ['.F'],
        'fakulta.': ['fakulta,', 'fakzulta.', 'práce.'],
        'Katedra': [ 'Kateda', 'katedra', 'Katerdra', 'Katerda', ],
        'Univerzita Karlova.': [ 
            'Univerzita Karlova,', 'Univerzita Karlova v Praze.', 'Univerzita Karlova. Univerzita Karlova.'
            'Univerzita .', 'Uverzita Karlova.', 'Univerzita karlova.', 
            ],

        ' lékařská': ['. lékařská'], #odstraňuju tečky z lekařských fakult abych mohla parsovat #TODO vrátit
        'teologická': ['telogická', 'teologická'],
        'Filozofická': ['Filozofikcá', 'Filozofciká', 'Filozoficka', 'Filozofivká', 'Fiolozofická',],
        'psychologie': ['psyvhologie', 'psychlogie', 'pésychologie', 'psychologie', ],
        'andragogiky a ': ['nadragogiky a ','andragogika '],
        'sociologie': ['socioloogie'],
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

