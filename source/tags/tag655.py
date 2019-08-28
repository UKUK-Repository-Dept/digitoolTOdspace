

def convertTag655(tag655,oai_id,categorize):
    ret = {}
    if 'a' in tag655.keys():
        ret['degree'] = []
        for level in tag655['a']:
            level = tag655['a'][0]
            level = level[0].upper() + level[1:] #první písmeno má být velké
            for correct, wrongs in convert.degreeTypo.items():
                for wrong in wrongs:
                    level = level.replace(wrong, correct)
            if level in catalogue.levelToTitle.keys():
                if not level in ret['degree']:
                    ret['degree'].append(level)
            else:
                # TODO tady je stucie to je cajk?
                pass #categorize.categorize_item(oai_id,"Unknown degree {}".format(level))
            if ret['degree'] == []:
                return {}
    for key in tag655.keys():
        if not key in 'a27':
            print(key)
            #raise Exception("Unkown key")
    return ret
