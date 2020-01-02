def convertTag(tag, oai_id):
    ret = {} 
    if 'a' in tag.keys():
        ret['grantNumbers'] = tag['a']
    grantAgency = []
    if 'b' in tag.keys():
        grantAgency += tag['b']
    if 'c' in tag.keys():
        grantAgency += tag['c']
    if grantAgency:
        ret['grantAgency'] = grantAgency
    for key in tag.keys():
        assert key in 'abce'
    return ret

