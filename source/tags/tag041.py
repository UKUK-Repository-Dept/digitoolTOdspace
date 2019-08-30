
def convertTag041(tag041,oai_id,categorize):
    ret = {}
    if 'a' in tag041.keys():
        ret['lang'] = tag041['a'][0]
    if 'b' in tag041.keys():
        ret['alternative_lang'] = tag041['b']
    return ret
