
def convertTag520(tag520,oai_id,categorize):
    ret = {}
    assert 'a' in tag520.keys()
    if len(tag520['a']) > 1:
        if '8' in tag520.keys():
            language = tag520['8']
        elif  '9' in tag520.keys():
            language = tag520['9']
        else:
            raise Exception('520: no language')
        if  len(tag520['a']) > 2:
            return ret #TODO domluva o jazycích
            #print(oai_id,tag520)
        for abstract in tag520['a']:
            if len(abstract) < 100:
                categorize.categorize_item(oai_id,"502: Too short abstract '{}'".format(abstract))
                return ret
        ret['abstract'] = tag520['a'][0]
        ret['lang'] = language[0]
        ret['alternative_abstract'] = tag520['a'][1]
        if len(language) > 1:
            ret['alternative_lang'] = language[1]
        return(ret)
    abstract = tag520['a'][0]
    if len(abstract) < 100:
        categorize.categorize_item(oai_id,"502: Too short abstract '{}'".format(abstract))
        return ret
    ret['abstract'] = abstract
    if '8' in tag520.keys():
        ret['lang'] = tag520['8'][0]
    if '9' in tag520.keys():
        ret['lang'] = tag520['9'][0]
    if 'b' in tag520.keys():
        categorize.categorize_item(oai_id,"502: Abstract in digitool '{}'".format(abstract))
    for key in tag520.keys():
        if not key in 'ab89':
            raise Exception("520: Unkown key {}".format(key))
    return ret
