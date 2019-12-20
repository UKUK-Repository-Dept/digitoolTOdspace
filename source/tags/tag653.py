
def convertTag653(tag653,oai_id):
    ret = {}
    assert 'a' in tag653.keys()
    ret = {'keywords': tag653['a']}
    for key in tag653.keys():
        if not key in 'a':
            raise Exception("653: Unkown key {}".format(key))
    return ret
