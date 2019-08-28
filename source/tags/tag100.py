
def convertTag100(tag100,oai_id,categorize):
    ret = {}
    if 'a' in tag100.keys():
        assert len(tag100['a']) == 1, tag100
        author = tag100['a'][0]
        if author[-1] == ',':
            author = author[:-1]
        ret['author'] = author
    if 'c' in tag100.keys():
        pass #print(oai_id,tag100['c']) # TODO má tam být Dr a pod nikoliv 'psychologie'
    if 'd' in tag100.keys():
        pass #print(oai_id,tag100['d']) #TODO narozeni (a umrti) autora
    if 'q' in tag100.keys():
        #print(oai_id,tag100['q'])
        pass # TODO 4x rok obhájení i když tam má být  "Fuller form of name (NR)"
    if '4' in tag100.keys():
        if not tag100['4'][0] in ['dis','aut','ths']:
            pass
    if '7' in tag100.keys():
        pass # print(tag100['7']) #108 ks 'jk01100092' 'xx0058281'
    for key in tag100.keys():
        if not key in 'acdq47':
            raise Exception("Unkown key")
    return ret
