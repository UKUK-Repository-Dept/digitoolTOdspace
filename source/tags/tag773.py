def convertTag(tag, oai_id):
    ret = {} 

    if '9' in tag.keys():
        assert len(tag['9']) == 1
        year = tag['9'][0].split(', ')[-1]
        ret['year'] = year
    if 'z' in tag.keys():
        ret['isbns'] = tag['z']

    used = 'ktdg'
    source = ''
    for key in used:
        if key in tag.keys():
            for item in tag[key]:
                source = source + ', ' + item
    source = source[2:]
    ret['source'] = source 

    ignored = 'bqwx'
    for key in tag.keys():
        assert key in used+'9z'+ignored

    return ret
