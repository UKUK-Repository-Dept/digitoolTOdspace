#!/usr/bin/python3
import os, click, logging
import urllib3 #disable warnings about http an gull

from digitoolXML import DigitoolXML #přepsat 
import metadataConvertor #TODO přepsat

xml_dirname = "Cerge/2019-12-19"
loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}

@click.group()
def cli():
    pass

#TODO 
#smazat TODO, print, zbytecne komenty
#tabulka cela
#exportovat vsechno do SAF
#nahrad na gull a otestovat
#napsat navod
#vypisovat ignorovate tagy do spesl tagu
#nahravat xml jako prilohu

@cli.command()
def statistic():
    dtx = DigitoolXML(xml_dirname)
    oai_ids = dtx.getList()
    click.echo("záznamů {}".format(len(oai_ids)))
    allTags = []
    for oai_id in oai_ids:
        metadata = dtx.get_metadata(oai_id)['marc']
        allTags.extend(metadata.keys())
    statistic = []
    for tag in set(allTags):
        statistic.append((allTags.count(tag),tag))
    statistic = sorted(statistic,reverse=True)
    for count, tag in statistic:
        click.echo("{}; {};".format(tag,count))


@cli.command()
@click.option('--archive/--no-archive', default=False, help='Create Simple Archive Formate')
@click.option('--copyfile/--no-copyfile', default=False, help='Copy files to SAF') #TODO napsat
@click.option('--log', default='error', type=click.Choice(loggingMap.keys()), help='Logging level')
def convert(archive,copyfile,log):
    logging.getLogger().setLevel(loggingMap[log])
    if log == 'error':
        urllib3.disable_warnings()
    dtx = DigitoolXML(xml_dirname)
    oai_ids = dtx.getList()

    for oai_id in oai_ids:
        digitoolMetadata = dtx.get_metadata(oai_id)['marc']
        parsedMetadata = metadataConvertor.parseMarc(digitoolMetadata, oai_id)
        convertedMetadata = metadataConvertor.createDC(oai_id, parsedMetadata, digitoolMetadata)
        #print(oai_id, parsedMetadata, convertedMetadata)
        attachements = list(dtx.get_attachements(oai_id))
        attachementsDescription = None
        if len(attachements) == 0:
            pass #TODO otestovat nahravani
        elif attachements[0][0] == 'undefined':
            pass #TODO
            #print(oai_id,attachements)
        else:
            # z příloh vyřadím náhledy a indexy
            attachementsDescription = []
            for (filename, filetype) in attachements:
                if '_thumbnail.jpg' in filename or '_index.html' in filename: 
                    continue
                if filetype != 'application/pdf':
                    pass #TODO kouknout se na obsah tech html
                    #print(oai_id,attachements)
                attachementsDescription.append((filename,filetype,'TODO to co je videt'))
            assert len(attachementsDescription) == 1

        if archive:
            outputDirectory = 'output/' + str(oai_id)
            
            if not os.path.exists(outputDirectory):
                os.mkdir(outputDirectory)

            #create metadatada files 
            convertedMetadata.save(outputDirectory)

            #create contents file
            if attachementsDescription:
                f = open(outputDirectory+'/contents','w')
                for filename, filetype, description in attachementsDescription:
                    filepath = xml_dirname + '/streams/' + filename
                    if copyfile:
                        os.system("cp '"+filepath+"' "+outputDirectory)
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

if __name__ == '__main__':
    cli()
