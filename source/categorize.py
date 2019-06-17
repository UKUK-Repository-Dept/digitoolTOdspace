class Categorize():
    ingests = ["ksp", "mff", "psy", "Dousova", "uisk", "Hubl", "smes", "nadm_velikost", "12345"] 
    notes = [["HTF"],["FFUk","FF","FF UK","FFUK"],["etf","ETF"],["MFF"],["PF"],["FTVS"],["2LF","LF2","2LF -"],["FSV","FSV IMS","FSV_IKSZ","FSV ISS","FSV IPS"],["FHS"],["3LF"]]
    category = {}

    def __init__(self, dtx):
        self.dtx = dtx
        self.category = {}
        for tag in self.ingests:
            self.category[tag] = {}
        self.category['other ingest'] = {}
        for tags in self.notes:
            self.category[str(tags)] = {}
        self.category['other note'] = {}
        self.category['None note'] = {}

    def categorize_list(self, oai_ids, descriptions, skip=False):
        for oai_id in oai_ids:
            self.categorize_ingest(oai_id, descriptions, skip)
    
    def categorize_item(self, oai_id, description, skip=False):
        self.categorize_ingest(oai_id, description, skip)
    
    def categorize_ingest(self, oai_id, description, skip=False):
        if skip:
            try:
                label, ingest, note = self.dtx.get_category(oai_id+".xml")
            except:
                return
        else:
            label, ingest, note = self.dtx.get_category(oai_id+".xml")
        for tag in self.ingests:
            if ingest != None and tag in ingest:
                self.category[tag].setdefault(oai_id,[]).append(description)
        if ingest == None:
            self.categorize_note(oai_id, description, note)
        else:
            other = True
            for tag in self.ingests:
                if tag in ingest:
                    other = False
            if other:
                self.category['other ingest'].setdefault(oai_id,[]).append(description)
    
    def categorize_note(self, oai_id, description, note):
        for tags in self.notes:
            if note != None and note in tags:
                self.category[str(tags)].setdefault(oai_id,[]).append(description)
        if note == None:
            self.category['None note'].setdefault(oai_id,[]).append(description)
        else:
            other = True
            for tags in self.notes:
                for tag in tags:
                    if tag == note:
                        other = False
            if other:
                self.category['other note'].setdefault(oai_id,[]).append(description)

    def print(self):
        sum = 0
        for tag, list_id in self.category.items():
            sum += len(list_id)
            print(tag,len(list_id))
        print("celkem",sum)
