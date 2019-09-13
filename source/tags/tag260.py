import catalogue
import string
import unicodedata

def convertTag260(tag,oai_id,categorize):
    ret = {}
    
    if not 'a' in tag.keys():
        pass #kašlem na to
        #categorize.categorize_item(oai_id,"260 Není podpole 'a'")
    else:
        assert len(tag['a']) == 1
        place = tag['a'][0].upper()
        place = unicodedata.normalize('NFD', place).encode('ascii', 'ignore').decode("utf-8")
        if len([ letter for letter in place if letter in string.ascii_uppercase ]) < 3:
            if not ('S' in string.ascii_uppercase and 'L' in string.ascii_uppercase):
                pass #kašlem na to
                #categorize.categorize_item(oai_id,"260 Není podpole 'a' {}".format(place))
        ret['place'] = tag['a'][0]

    if not 'c' in tag.keys():
        categorize.categorize_item(oai_id,"260 Není podpole 'c'")
        return ret
    if 'c' in tag.keys():
        assert len(tag['c']) == 1
        year = tag['c'][0] 
        #dohodlá normazizace
        if year[0] == '[' and year[-1] == ']': 
            year = year[1:-1] 
        if year == 'asi 1968':
            year = '1968?'
        if len(year) == 4 or (len(year) == 5 and year[4] == '?') and year[:4].isdigit():
            if year[3] == '?': #hack ať abych kontrolovala i přibližné roky
                yearHack = year[:3] + '0' 
            else:
                yearHack = year[:4]
            assert 1900 < int(yearHack) < 2019, year
            ret['year'] = year
        else:
            categorize.categorize_item(oai_id,"260 Neuzavřená závorka {}".format(year))
    
    for k in tag.keys():
        assert k in 'abc'
    return {}
