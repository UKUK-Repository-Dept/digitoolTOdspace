import catalogue

def convertTag260(tag,oai_id,categorize):
    if not 'a' in tag.keys():
        categorize.categorize_item(oai_id,"Není podpole 'a'")
        #print(tag)
        return
    if tag['a'] != ['Praha,']:
        #print(tag)
        pass
    if 'b' in tag.keys():
        #print(oai_id,tag['b'])
        pass
    if 'c' in tag.keys():
        assert len(tag['c']) == 1
        year = tag['c'][0]
        if not len(year) == 4:
            print(oai_id,year)
        else:
            assert 1900 < int(year) < 2019, year
        pass
    for k in tag.keys():
        assert k in 'abc'
