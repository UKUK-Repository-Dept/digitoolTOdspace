
def convertTagC15(tagC15,oai_id):
    ret = {}
    if not 'a' in tagC15.keys():
        return {} #TODO
    assert 'a' in tagC15.keys()
    ret['abstract'] = tagC15['a'][0]
    
    if 'b' in tagC15.keys():
        ret['abstract2'] = tagC15['b'][0]
    if 'c' in tagC15.keys():
        ret['abstract3'] = tagC15['c'][0]
    for key in tagC15.keys():
        if not key in 'abc':
            raise Exception("C15: Unkown key {}".format(key))
    return ret
