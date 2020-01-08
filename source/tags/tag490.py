def convertTag(tag, oai_id):
    ret = {} 
    series = ''
    if type(tag) == str:
        ret['series'] = series
        return ret #to tu nema byt ale kdyz uz je..
    for name in tag['a']:
        if name[-2:] == ' ;':
            name = name[:-2]
        series = series + name
    if 'v' in tag.keys():
        assert len(tag['v']) == 1
        series = series + tag['v'][0]
    ret['series'] = series
    return ret 
