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
import time
from sap import createArchive

#xml_dirname = "DUR01/2019-10-01"
xml_dirname = "Cerge/2019-12-19"
digitool_category = "oai_kval"
#server = "gull"
server = "dodo"

loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}
@click.group()
def cli():
    pass


categories = {
    'all_problems': bugs.all_attachements,
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

operations=['handle','delete_collection','delete_bitstream','total_size']
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
    ds = Dspace(server,dspace_admin_username,dspace_admin_passwd)
    if operation == 'total_size':
        # pozor na původní balíčky
        # https://gull.is.cuni.cz/admin/item?administrative-continue=4c773a89622b298c69750d5f7537327a6b343850&submit_bitstreams
        size = ds.total_size()
        print(size/1000/1000/1000.0)
    if operation == 'handle':
        handle = arg[0]
        ds.handle(handle) # př "123456789/86"
    if operation == 'delete_bitstream':
        bitstream = arg[0]
        ds.delete_bitstream(bitstream)
    if operation == 'delete_collection':
        ds.delete_all_item(int(arg[0]))
    ds.logout()


@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
@click.option('--run/--no-run', default=False, help='Push to converted data to server')
@click.option('--archive/--no-archive', default=False, help='Create Simlpe Archive Formate')
@click.option('--catalogue/--no-catalogue', default=False, help='Create list of id, collection')
@click.option('--log', default='error', type=click.Choice(loggingMap.keys()), help='Logging level')
def convert(dspace_admin_passwd, dspace_admin_username, run, archive, catalogue, log):
    #TODO aleph, weird_attachmement by měli být nulové a ostatní by tak měli zustat
    logging.getLogger().setLevel(loggingMap[log])
    if log == 'error':
        urllib3.disable_warnings()
    dtx = DigitoolXML(xml_dirname)
    oai_ids = dtx.getList()
    categorize = Categorize(dtx)
    if run:
        ds = Dspace(server,dspace_admin_username,dspace_admin_passwd,xml_dirname=xml_dirname)
    records = aleph.openAleph("dtl_2006.xml")
    if catalogue:
        f = open('output/'+server,'w')

    count = 0
    #for oai_id in oai_ids:
    facultysum = {}
    for oai_id in oai_ids:
        count += 1
        digitoolMetadata = dtx.get_metadata(oai_id)['marc']
        #aleph_id = aleph.normalise(digitoolMetadata['001'])
        #originalMetadata = records[aleph_id]
        metadataTopic = metadataConvertor.convertMarc(categorize, oai_id, digitoolMetadata)
        convertedMetadata, collection = metadataConvertor.createDC(server,categorize, oai_id, metadataTopic, digitoolMetadata)
        #print(metadataTopic)
        attachements = list(dtx.get_attachements(oai_id))
        fc = filenameConvertor.FilenameConvertor(categorize)
        attachementsDescription = fc.generate_description(oai_id,attachements)
        
        #if collection == None:
        #    raise Exception('Unknown faculty')
        # 
        #if collection == 248:
        #    for row in convertedMetadata['metadata']:
        #        if row['key'] == 'dc.title':
        #            print(row['value'])
        #        if row['key'] == 'dc.description.faculty':
        #            print(row['value'])
        if False:
            for row in convertedMetadata['metadata']:
                print(row)
            print(attachementsDescription)
        if run:
            ds.new_item(collection,convertedMetadata,attachementsDescription)
        if archive:
            createArchive(oai_id, xml_dirname, convertedMetadata, attachementsDescription)
        if catalogue:
            f.write("{} {}\n".format(oai_id, collection))
        #for row in convertedMetadata['metadata']:
        #    if row['key'] == 'dc.description.faculty':
        #        faculty =  row['value']
    #    if faculty not in facultysum:
    #        facultysum[faculty] = 1
    #    else:
    #        facultysum[faculty] +=1
    #    if count % 1000 == 0:
    #        time.sleep(1)
    if run:
        ds.logout()
    if catalogue:
        f.close()

    if facultysum:
        print(facultysum)

if __name__ == '__main__':
    cli()
