import catalogue

def convertTag655(tag655,oai_id,categorize):
    ret = {}
    if 'a' in tag655.keys():
        if len(tag655['a']) > 1:
            categorize.categorize_item(oai_id,"655: More than one degree {}".format(tag655['a']))
            return ret
        degree = tag655['a'][0]
        if degree in ['disertace','Disertační práce']: # výjimka schválena Iry
            degree = 'dizertační práce'
        if not degree in catalogue.categoryToTypeTitle.keys():
            categorize.categorize_item(oai_id,"655: Unknown study degree".format(degree))
            return ret
        ret['degree'] = catalogue.categoryToTypeTitle[degree]
        return ret
    # datum mám ignorovat
    for key in tag655.keys():
        if not key in 'a27':
            raise Exception("Unkown key")
    return ret
