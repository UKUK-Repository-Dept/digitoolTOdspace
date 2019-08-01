class Categorize():
    ingests = ["ksp", "mff", "psy", "uisk", "12345"] 
    notes = [["HTF"],["FFUk","FF","FF UK","FFUK"],["etf","ETF"],["MFF"],["PF"],["FTVS"],["2LF","LF2","2LF -"],["FSV","FSV IMS","FSV_IKSZ","FSV ISS","FSV IPS"],["FHS"],["3LF"]]
    category = {}


    def __init__(self, dtx, export='list'):
        self.dtx = dtx
        self.category = {}
        for tag in self.ingests:
            self.category[tag] = {}
        self.category['other ingest'] = {}
        for tags in self.notes:
            self.category[str(tags)] = {}
        self.category['other note'] = {}
        self.category['None note'] = {}
        assert export in ['no','list','id_on_row','with_reason']
        self.export = export

    def categorize_list(self, oai_ids, descriptions):
        for oai_id in oai_ids:
            self.categorize_ingest(oai_id, descriptions)
    
    def categorize_item(self, oai_id, description):
        self.__categorize_ingest(oai_id, description)
    
    def __categorize_ingest(self, oai_id, description):
        if  self.dtx.get_category(oai_id):
            label, ingest, note = self.dtx.get_category(oai_id)
        else:
            return
        for tag in self.ingests:
            if ingest != None and tag in ingest:
                self.category[tag].setdefault(oai_id,[]).append(description)
        if ingest == None:
            self.__categorize_note(oai_id, description, note)
        else:
            other = True
            for tag in self.ingests:
                if tag in ingest:
                    other = False
            if other:
                self.category['other ingest'].setdefault(oai_id,[]).append(description)
    
    def __categorize_note(self, oai_id, description, note):
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

    def __str__(self):
        sum = 0
        output = ""
        if self.export == 'no':
            return output
        for tag, list_id in self.category.items():
            sum += len(list_id)
            output = output + tag + " " + str(len(list_id)) + "\n"
            if self.export == 'id_on_row':
                output = output + "\n"
                for id in list_id:
                    output = output + str(id) + "\n"
            elif self.export == 'with_reason':
                output = output + "\n"
                for oai_id, reasons in self.category['psy'].items():
                     output = output + str(oai_id) + " " + str(reasons) + "\n"
                pass
        output = output + "\n" + "celkem " + str(sum)
        return output
