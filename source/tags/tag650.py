
def convertTag650(tag650,oai_id):
    ret = {}
    if not 'a' in tag650:
        raise Exception('650: No keywords')
    ret['keywords'] = tag650['a']
    return ret
