def convertTag(tag, oai_id):
    ret = {}
    if 'u' in tag.keys():
        ret['urls'] = tag['u']
    return ret 
