import catalogue
import string
import unicodedata

def convertTag260(tag,oai_id,categorize):
    # tag není zařazený protože Iry s Jarem neví co chtěji a nechávají bordel v aleph.
    ret = {}
    
    if not 'a' in tag.keys():
        categorize.categorize_item(oai_id,"260 Není podpole 'a'")
        return ret
    assert len(tag['a']) == 1
    place = tag['a'][0].upper()
    place = unicodedata.normalize('NFD', place).encode('ascii', 'ignore').decode("utf-8")
    if len([ letter for letter in place if letter in string.ascii_uppercase ]) < 3:
        categorize.categorize_item(oai_id,"260 Není podpole 'a'")
        return ret
    ret['place'] = tag['a'][0]

    if not 'c' in tag.keys():
        categorize.categorize_item(oai_id,"260 Není podpole 'c'")
        return ret
    if 'c' in tag.keys():
        assert len(tag['c']) == 1
        year = tag['c'][0]
        if len(year) == 4: # nebo šechny??
            assert 1900 < int(year) < 2019, year
            ret['year'] = tag['c'][0]
    
    for k in tag.keys():
        assert k in 'abc'
    return {}
