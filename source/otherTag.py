import catalogue, convert
import commonTag


def convertTag100(tag100,oai_id,categorize):
    ret = {}
    if 'a' in tag100.keys():
        assert len(tag100['a']) == 1, tag100
        author = tag100['a'][0]
        if author[-1] == ',':
            author = author[:-1]
        ret['author'] = author
    if 'c' in tag100.keys():
        pass # print(oai_id,tag100['c']) # zbytečné př 'sociologie Dr ml r.obhaj.
    if 'd' in tag100.keys():
        pass #print(oai_id,tag100['d']) #TODO narozeni (a umrti) autora
    if 'q' in tag100.keys():
        #print(oai_id,tag100['q'])
        pass # TODO 4x rok obhájení i když tam má být  "Fuller form of name (NR)"
    if '4' in tag100.keys():
        if not tag100['4'][0] in ['dis','aut','ths']:
            pass
    if '7' in tag100.keys():
        pass # print(tag100['7']) #108 ks 'jk01100092' 'xx0058281'
    for key in tag100.keys():
        if not key in 'acdq47':
            raise Exception("Unkown key")
    return ret

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
