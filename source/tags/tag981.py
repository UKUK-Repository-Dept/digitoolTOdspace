
def convertTag981(tag981,oai_id,categorize):
    ret = {}
    if 'a' in tag981.keys():
        if len(tag981['a']) == 2 and tag981['a'][0] == tag981['a'][1]:
            tag981['a'] = tag981['a'][:1]
        assert len(tag981['a']) == 1
        level = tag981['a'][0]
        if level in catalogue.levelToTitle.keys():
            ret['degree'] = [ convert.degree[level] ]
        else:
            categorize.categorize_item(oai_id,"Unknown degree {}".format(level))
    for key in tag981.keys():
        if not key in 'a':
            raise Exception("Unkown key")
    return ret
