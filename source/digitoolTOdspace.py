#!/usr/bin/python3
import os
import click
from digitoolXML import DigitoolXML
from dspace import Dspace
import filenameConvertor
import metadataConvertor
from categorize import Categorize
import aleph
import problematicGroup as bugs
import logging
import urllib3 #disable warnings about http an gull

xml_dirname = "DUR01/2019-10-01"
#xml_dirname = "Cerge/2019-09-05"
digitool_category = "oai_kval"
dspaceCollection = 279 

loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}
@click.group()
def cli():
    pass


categories = {
    'all_problems_for_hanka': bugs.all_attachements,
    'all_items_in_oai': bugs.oai,
    'forgot_attachements': bugs.forgot_attachements,
    'ittems_without_attachments': bugs.no_attachements,
    'not_in_aleph': bugs.not_in_aleph,
    'weird_attachments': bugs.weird_attachements,
    'only_dc': bugs.only_dc,
    'aleph': bugs.aleph_metadata,
    }
output = ['no','list','id_on_row','with_reason']


@cli.command()
@click.option('--group', prompt='group', type=click.Choice(categories.keys()), help='Choose group to categorize')
@click.option('--output', default='list', type=click.Choice(output), help='Output print format')
@click.option('--log', default='error', type=click.Choice(loggingMap.keys()), help='Logging level')
def categorize(group,output,log):
    logging.getLogger().setLevel(loggingMap[log])
    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx, output)
    oai_ids = dtx.getList()
    categories[group](oai_ids,dtx,c)
    print(c)

@cli.command()
def statistic(log):
    logging.getLogger().setLevel(loggingMap[log])
    records = aleph.openAleph("dtl_2006.xml")
    print('záznamů ',len(records))
    allTags = []
    for metadata in records:
        allTags.extend(metadata.keys())
    statistic = []
    for tag in set(allTags):
        statistic.append((allTags.count(tag),tag))
    statistic = sorted(statistic,reverse=True)
    for count, tag in statistic:
        print(tag,count)

operations=['handle','new_item','delete_collection','delete_bitstream']
@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
@click.option('--operation', prompt='operation', type=click.Choice(operations))
@click.argument('arg', nargs=-1)
def dspace(dspace_admin_passwd, dspace_admin_username, operation,arg):
    metadata = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Od jinud" } 
                ]}
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    if operation == 'handle':
        handle = arg[0]
        ds.handle(handle) # př "123456789/86"
    if operation == 'new_item':
        ds.new_item(dspaceCollection,metadata,[("lorem-ipsum.pdf",'application/pdf','soubor')])
    if operation == 'delete_bitstream':
        bitstream = arg[0]
        ds.delete_bitstream(bitstream)
    if operation == 'delete_collection':
        ds.delete_all_item(dspaceCollection)
    ds.logout()

def convertItem(dtx, categorize, oai_id, originalMetadata, ds, run):
    
    metadataTopic = metadataConvertor.convertMarc(categorize, oai_id, originalMetadata)
    convertedMetadata, collection = metadataConvertor.createDC(categorize, oai_id, metadataTopic, originalMetadata)
    attachements = list(dtx.get_attachements(oai_id))
    fc = filenameConvertor.FilenameConvertor(categorize)
    attachementsDescription = fc.generate_description(oai_id,attachements)
    if False:
        click.clear()
        print("converting ",oai_id)
        print("\noriginalMetadata:")
        for key in originalMetadata.keys():
            print(key,originalMetadata[key])
        print("\nconvertedMetadata:")
        for row in convertedMetadata['metadata']:
            print(row)
        print("\nattachements:")
        print(attachementsDescription)
        #checked = click.confirm("Is converting OK?", default=True)
    if run:
        #ds.new_item(collection,convertedMetadata,attachementsDescription) #to zaverecne
        ds.new_item(dspaceCollection,convertedMetadata,attachementsDescription)
        #ds.new_item(dspaceCollection,convertedMetadata,[("lorem-ipsum.pdf","application/pdf","Dokument")])

@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
@click.option('--run/--no-run', default=False, help='Pushih converted data to server')
@click.option('--log', default='error', type=click.Choice(loggingMap.keys()), help='Logging level')
def convert(dspace_admin_passwd, dspace_admin_username, run, log):
    #TODO aleph, weird_attachmement by měli být nulové a ostatní by tak měli zustat
    logging.getLogger().setLevel(loggingMap[log])
    if log == 'error':
        urllib3.disable_warnings()
    dtx = DigitoolXML(xml_dirname)
    oai_ids = dtx.getList()
    categorize = Categorize(dtx)
    ds = Dspace(dspace_admin_username,dspace_admin_passwd,xml_dirname=xml_dirname)
    records = aleph.openAleph("dtl_2006.xml")
    
    for oai_id in oai_ids:
    #for i in range(5):
    #    oai_id = oai_ids[i]
    #    print(i)
    #for oai_id in [oai_ids[4]]:
        
        digitoolMetadata = dtx.get_metadata(oai_id)['marc']
        aleph_id = aleph.normalise(digitoolMetadata['001'])
        #if aleph_id != '000732536':
        #    continue
        originalMetadata = records[aleph_id]
        convertItem(dtx, categorize, oai_id, originalMetadata, ds, run)
    ds.logout()

if __name__ == '__main__':
    cli()
