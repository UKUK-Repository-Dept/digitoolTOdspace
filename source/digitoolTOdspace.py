#!/usr/bin/python3
import os, click
from digitoolXML import DigitoolXML
from dspace import Dspace
import filenameConvertor
import metadataConvertor
from categorize import Categorize
import problematicGroup as bugs
import logging
import urllib3 #disable warnings about http an gull
import time
from sap import createArchive

#xml_dirname = "DUR01/2019-10-01"
xml_dirname = "Cerge/2019-12-19"
digitool_category = "oai_kval"
#server = "gull"
server = "dodo"

loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}
output = ['no','list','id_on_row','with_reason']
@click.group()
def cli():
    pass

@cli.command()
def statistic():
    dtx = DigitoolXML(xml_dirname)
    oai_ids = dtx.getList()
    print('záznamů ',len(oai_ids))
    allTags = []
    for oai_id in oai_ids:
        metadata = dtx.get_metadata(oai_id)['marc']
        allTags.extend(metadata.keys())
    statistic = []
    for tag in set(allTags):
        statistic.append((allTags.count(tag),tag))
    statistic = sorted(statistic,reverse=True)
    for count, tag in statistic:
        print(tag,';',count,';')


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
    categorize = Categorize(dtx)

    for oai_id in oai_ids:
        digitoolMetadata = dtx.get_metadata(oai_id)['marc']
        parsedMetadata = metadataConvertor.convertMarc(categorize, oai_id, digitoolMetadata)
        convertedMetadata = metadataConvertor.createDC(server,categorize, oai_id, parsedMetadata, digitoolMetadata)
        attachements = list(dtx.get_attachements(oai_id))
        fc = filenameConvertor.FilenameConvertor(categorize)
        attachementsDescription = fc.generate_description(oai_id,attachements)
        
        if archive:
            createArchive(oai_id, xml_dirname, convertedMetadata, attachementsDescription, copyfile)

if __name__ == '__main__':
    cli()
