
def convertTag246(tag246,oai_id,categorize):
    ret = {}
    if 'b' in tag246.keys():
        ret['alternative'] = "{} {}".format(tag246['a'][0],tag246['b'][0])
    else:
        ret['alternative'] = tag246['a'][0]
    return ret
