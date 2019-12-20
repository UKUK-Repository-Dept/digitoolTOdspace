#!/usr/bin/python3
import os, click, logging
import urllib3 #disable warnings about http an gull

from digitoolXML import DigitoolXML #TODO promazat
import filenameConvertor #TODO přepsat
import metadataConvertor #TODO přepsat

xml_dirname = "Cerge/2019-12-19"
loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}
output = ['no','list','id_on_row','with_reason']

@click.group()
def cli():
    pass

#TODO smazat TODO, print, categorize, zbytecne komenty
#tabulka cela
#exportovat vsechno do SAF
#nahrad na gull a otestovat
#promazat catalogue
#napsat navod

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
        #print(convertedMetadata)
        attachements = list(dtx.get_attachements(oai_id))
        fc = filenameConvertor.FilenameConvertor()
        attachementsDescription = fc.generate_description(oai_id,attachements)

        if archive:
            outputDirectory = 'output/' + str(oai_id)
            
            if not os.path.exists(outputDirectory):
                os.mkdir(outputDirectory)

            #create metadatada files 
            convertedMetadata.save(outputDirectory)

            #create contents file
            f = open(outputDirectory+'/contents','w')
            for filename, filetype, description in attachements:
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
