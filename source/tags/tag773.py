def convertTag(tag, oai_id):
    ret = {} 
    #print(tag)

    if '9' in tag.keys():
        ret['year'] = tag['9'][0]
    if 'z' in tag.keys():
        ret['isbns'] = tag['z']
    used = 'kdtg'
    source = ''
    for key in used:
        if key in tag.keys():
            assert len(tag[key]) == 0
            source = source + ', ' + tag[key][0]
    print(soursce)
    ignored = 'bqwx'
    for key in tag.keys():
        assert key in used+'9z'+ignored
    return ret #TODO
