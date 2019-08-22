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

    def categorize_item(self, oai_id, description):
        self.__categorize_ingest(oai_id, description)
    
    def __categorize_ingest(self, oai_id, description):
        try:
            label, ingest, note = self.dtx.get_category(oai_id)
        except:
            label, ingest, note = None, None, None 
        if ingest == None:
            self.__categorize_note(oai_id, description, note)
        else:
            tags = [tag for tag in self.ingests if tag in ingest]
            if tags == []:
                self.category['other ingest'].setdefault(oai_id,[]).append(description)
            else:
                self.category[tags[0]].setdefault(oai_id,[]).append(description)
    
    def __categorize_note(self, oai_id, description, note):
        if note == None:
            self.category['None note'].setdefault(oai_id,[]).append(description)
        else:
            tags = [tags for tags in self.notes if note in tags]
            if tags == []:
                self.category['other note'].setdefault(oai_id,[]).append(description)
            else:
                self.category[str(tags[0])].setdefault(oai_id,[]).append(description)

    def __str__(self):
        sum = 0
        output = ""
        if self.export == 'no':
            return output
        for tag, list_id in self.category.items():
            sum += len(list_id)
            if len(list_id) > 0:
                output = output + tag + " " + str(len(list_id)) + "\n"
            if self.export == 'id_on_row':
                if len(list_id) > 0:
                    for id in list_id:
                        output = output + str(id) + "\n"
                    output = output + "\n"
            elif self.export == 'with_reason':
                if len(list_id) > 0:
                    for oai_id, reasons in self.category[tag].items():
                        output = output + str(oai_id) + " " + str(reasons) + "\n"
                    output = output + "\n"
        output = output + "celkem " + str(sum)
        return output
