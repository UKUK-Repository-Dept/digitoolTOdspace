class FilenameConvertor:
    #TODO odhadovat z metadat
    def __init__(self, categorize):
        self.categorize = categorize

    side = [
            ( ['vedouci'], "Posudek vedoucího" ),
            ( ['opon'], "Posudek oponenta" ),
            ( ['posud'], "Posudek" ),
            ( ['Priloh','pril','foto','příloh','grafy','summary','config','Dodatky','clanek'], "Příloha" ),
            ( ['chyby'], "Chyby" ),
            ( ['literatura'], "Literatura" ),
        ]
    main = [
        ( ['BC','bp','BP','Bakaraska','baklarka','Bc','Bakalarska','bakalarka','bakalarska'], "Bakalářská práce"),
        ( ['DP','Diplomova','Diplomka','diplomka','diplomova','dp','dP','dip','DIP'], "Diplomová práce"),
        ( ['rigorózni','rigo','Dis','RP','phd'], "Rigorózní práce"),
        ]
    weird = [(['DT-config_guide','Dodatky','clanek','posudek'], "TODO")]
            

    def match(self, dictionary, name):
        matches = []
        for tags, match in dictionary:
            for tag in tags:
                if tag in name:
                    matches.append(match)
                    break
        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]
        else:
            raise Exception("More matches. {}".format(name))

    def generate_description(self, files):
        if len(files) == 1:
            filename, filetype = files[0]
            if filetype == 'application/pdf':
                if self.match(self.side, filename):
                    oai_id = filename.split('_')[0]
                    self.categorize.categorize_item(oai_id,"hlavní soubor {} vypadá jako příloha".format(filename))
                else:
                    try:
                        match = self.match(self.main, filename)
                    except Exception as e:
                        if "DP" in filename and ( "RP" in filename or "rigo" in filename):
                            return [(filename, filetype, "Závěrečná práce")]
                        else:
                            raise e
                    if match:
                        return [(filename, filetype, match)]
                    else:
                        return [(filename, filetype, "Závěrečná práce")]
            else:
                oai_id = filename.split('_')[0]
                self.categorize.categorize_item(oai_id,"jediná příloha není pdf, ale {}".format(filetype))
        else:
            side = 0
            for filename, filetype in files:
                try:
                    match = self.match(self.side, filename)
                except Exception as e:
                    if "posudek_oponent" in filename:
                        match = "Posudek oponenta" 
                    elif "posudek_vedouci" in filename:
                        match = "Posudek vedoucího"
                    else:
                        raise e
                if match == None:
                    side += 1
            if side == 1:
                res = []
                for filename, filetype in files:
                    try:
                        match = self.match(self.side, filename)
                    except Exception as e:
                        if "posudek_oponent" in filename:
                            match = "Posudek oponenta" 
                        elif "posudek_vedouci" in filename:
                            match = "Posudek vedoucího"
                        else:
                            raise e
                    if match != None:
                        res.append( (filename, filetype, match) )
                    else:
                        try:
                            match = self.match(self.main, filename)
                        except Exception as e:
                            if "DP" in filename and ( "RP" in filename or "rigo" in filename):
                                match = "Závěrečná práce"
                            else:
                                raise e
                        res.append( (filename, filetype, match) )
                return res
            else:
                res = []
                for filename, filetype in files:
                    res.append( (filename, filetype, None) )
                return res
                #return str(files)+str(side) # 57
        return []

