import catalogue, convert
import tags.commonTag



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
