#TODO aktualizovat pro Cerge
def distance(word1,word2):
    word1 = word1.split('_',1)[1]
    word2 = word2.split('_',1)[1]
    diff = 0
    if len(word2) > len(word1):
        word1, word2 = word2, word1
    diff += len(word1) - len(word2)
    for i in range(len(word2)):
        if word1[i] != word2[i]:
            diff += 1
    return diff

class FilenameConvertor:
    side = [
            ( ['vedouci'], "Posudek vedoucího" ),
            ( ['opon'], "Posudek oponenta" ),
            ( ['posud'], "Posudek" ),
            ( ['foto','příloh','_Obr.','_teze','grafy','summary','config','Dodatky','clanek','Resume','install','manual'], "Příloha" ),
            ( ['Priloh','pril'], "Příloha" ),
            ( ['chyby'], "Chyby" ),
            ( ['literatura','_lit.'], "Literatura" ),
        ]
    main = [ # na poradi zalezi, pokud je zarovet RP a DP beru jako DP
        ( ['hab'], "Habilitační práce"),
        ( ['rigorózni','rigo','Dis','RP','phd'], "Rigorózní práce"),
        ( ['DP','Diplomova','Diplomka','diplomka','diplomova','dp','dP','dip','DIP','dis'], "Diplomová práce"),
        ( ['BC','bp','BP','Bakaraska','baklarka','Bc','Bakalarska','bakalarka','bakalarska'], "Bakalářská práce"),
        ]

    def match(self, dictionary, name):
        for tags, match in dictionary:
            for tag in tags:
                if tag in name:
                    return match

    #def generate_description(self, oai_id, files, degree):
    def generate_description(self, oai_id, files):
        attachement = []
        mainFiles = []
        for filename, filetype in files:
            if '_index.html' in filename or '_thumbnail.jpg' in filename:
                continue
            #matchMain = self.match(self.main, filename)
            matchSide = self.match(self.side, filename)
            if matchSide != None:
                if matchSide == "Příloha?":
                    print(filename)
                attachement.append((filename,filetype,matchSide))
                continue
            #if matchMain != None:
            #    if degree and matchMain != degree:
                    #err_msg = "Different degree file: {} metadata: {}".format(matchMain,degree)
                    #print(oai_id, err_msg) #asi nebudeme konrolovat
                    #self.categorize.categorize_item(oai_id, err_msg)
            mainFiles.append((filename,filetype))
        
        if len(mainFiles) > 2:
            if sum([ 1 for f,t in mainFiles if t == 'application/pdf']) == 1:
                for f,t in mainFiles:
                    if t == 'application/pdf':
                        attachement.append((f,t,'Text práce'))
                    else:
                        attachement.append((f,t,'Příloha'))
            else:
                for f,t in mainFiles:
                    if t == 'application/pdf':
                        attachement.append((f,t,'Text práce'))
                    else:
                        attachement.append((f,t,'Text práce v doc'))
            return attachement
        elif len(mainFiles) == 0:
            ret = []
            for filename, filetype, trash in attachement:
                ret.append((filename, filename, "Text práce"))
            return ret
        elif len(mainFiles) == 1:
            filename, filetype = mainFiles[0]
            if filetype != 'application/pdf': 
                pass
                #self.categorize.categorize_item(oai_id, "text práce není v pdf")
            else:
                return attachement + [(filename, filetype, "Text práce")]
        elif len(mainFiles) == 2:
            filename1, filetype1 = mainFiles[0]
            filename2, filetype2 = mainFiles[1]
            if filetype1 == filetype2 == 'application/pdf':
                return attachement + [(filename1, filetype1, "Text práce"), (filename2, filetype2, "Text práce")]
            if filetype1 != 'application/pdf' and filetype2 != 'application/pdf':
                pass
                #self.categorize.categorize_item(oai_id, "text práce není v pdf")
            if filetype2 == 'application/pdf':
                filename1, filename2 = filename2, filename1
                filetype1, filetype2 = filetype2, filetype1
            assert filetype1 == 'application/pdf'
            assert filetype2 == 'application/msword'
            return attachement + [(filename1, filetype1, "Text práce"), (filename2, filetype2, "Text práce v doc")]

        #self.joinFiles(oai_id mainFiles)
    
    def joinFiles(self, mainFiles):
        if len(mainFiles) > 2:
            if sum([ 1 for f,t in mainFiles if t == 'application/pdf']) == 1:
                return
            else:
                joinFiles = True
        elif len(mainFiles) < 2:
            return
        else:
            filename1, filetype1 = mainFiles[0]
            filename2, filetype2 = mainFiles[1]
            if not filetype1 == filetype2 == 'application/pdf':
                return
        
        diff = [ distance(f,mainFiles[0][0]) for f,t in mainFiles]
        if max(diff) > 1:
            for f,t in mainFiles:
                pass
        else:
            if 'Bulan' in mainFiles[0][0]:
                return
            files = []
            ids = []
            for f,t in mainFiles:
                files.append(f.split('_',1)[1])
                ids.append(f.split('_',1)[0])
            import numpy as np
            files = np.unique(files)
            for i in ids:
                print(i,end = ', ')
            print()
            for f,t in mainFiles:
                print(f,end=' ')
            #print('pdfunite',end=' ')
            #for f in files:
            #    print('*'+f,end=' ')
            newName = ''
            for i in range(len(files[0])):
                if files[0][i] == files[1][i]:
                   newName = newName + files[0][i]
            newName = newName.replace('_.','.')
            print(newName)
            #print(newName,end=' ')
