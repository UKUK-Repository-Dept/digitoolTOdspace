#!/usr/bin/python3
import os, click, logging
import urllib3 #disable warnings about http an gull

from digitoolXML import DigitoolXML #přepsat 
import metadataConvertor 

xml_dirname = "Cerge/2020-01-02"
loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}

@click.group()
def cli():
    pass

#TODO 
#smazat TODO, print
#tabulka cela
#napsat navod
#otestovat nahravani bez prilohy, s prilohou, metadata

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
@click.option('--copyfile/--no-copyfile', default=False, help='Copy files to SAF')
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

        if archive:
            outputDirectory = 'output/' + str(oai_id) + '/' + str(oai_id)
            
            if not os.path.exists(outputDirectory):
                os.mkdir(outputDirectory)

            #create metadatada files 
            convertedMetadata.save(outputDirectory)

            #create contents file
            f = open(outputDirectory+"/contents","w")
            for filename, filetype in attachements:
                if filename == 'undefined':
                    continue
                if '_thumbnail.jpg' in filename or '_index.html' in filename: 
                    continue
                if filetype not in ['application/pdf','text/html']:
                    raise Exception("new type of document")
                if copyfile:
                    filepath = xml_dirname + "/streams/" + filename
                    os.system("cp '"+filepath+"' "+outputDirectory)
                row = createRow(filename,"Příloha")
                f.write(row)
            if copyfile:
                filepath = xml_dirname + "/digital_entities/" + oai_id + ".xml" 
                os.system("cp '"+filepath+"' "+outputDirectory)
            row = createRow(oai_id + ".xml", "metadata")
            f.write(row)
            f.close()

def createRow(filename, description):
        row = filename + '\t'
        row += 'bundle:ORIGINAL\t'
        row += 'permissits:-r Anonymous' #TODO otestovat
        row += '\tdescription:'+description
        row += '\n'
        return row

if __name__ == '__main__':
    cli()
