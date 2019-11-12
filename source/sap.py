import os

def createArchive(oai_id, xml_dirname, metadata, attachements):
    outputDirectory = 'output/' + str(oai_id)

    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    
    f = open(outputDirectory+'/contents','w')
    for filename, filetype, description in attachements:
        filepath = xml_dirname + '/streams/' + filename
        os.system('cp '+filepath+' '+outputDirectory)
        row = filename + '\t'
        row += 'bundle:ORIGINAL\t'
        row += 'permissits:-r '
        if 'Posudek' in description:
            row += "'Admin'"
        else:
            row += "'IPshibAuthenticatedUniMember'"
        row += '\tdescription:'+description
        row += '\n'
        f.write(row)
    f.close()

    #print(metadata,attachements)
