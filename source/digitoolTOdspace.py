#!/usr/bin/python3
import os
import click
from digitoolOAI import Digitool
from digitoolXML import DigitoolXML
from dspace import Dspace
from filenameConvertor import FilenameConvertor
from metadataConvertor import Metadata
from categorize import Categorize
import aleph
import problematicGroup as bugs
import logging

xml_dirname = "2019-09-04"
#xml_dirname = "Cerge/2019-09-05"
digitool_category = "oai_kval"


@click.group()
def cli():
    pass


categories = {
    'all_problems_for_hanka': bugs.all_attachements,
    'all_items_in_oai': bugs.oai,
    'attachments_not_linked_to_oai': bugs.forgot_attachements,
    'ittems_without_attachments': bugs.no_attachements,
    'not_in_aleph': bugs.not_in_aleph,
    'weird_attachments': bugs.weird_attachements,
    'no_502': bugs.no502,
    'only_dc': bugs.only_dc,
    'not_valid_502': bugs.tag502,
    'not_valid_marc': bugs.marc,
    'aleph': bugs.aleph,
    }
output = ['no','list','id_on_row','with_reason']
loggingMap = {'error':logging.ERROR, 'info':logging.INFO, 'debug':logging.DEBUG}


@cli.command()
@click.option('--group', prompt='group', type=click.Choice(categories.keys()), help='Choose group to categorize')
@click.option('--output', default='list', type=click.Choice(output), help='Output print format')
@click.option('--log', default='error', type=click.Choice(loggingMap.keys()), help='Logging level')
def categorize(group,output,log):
    logging.getLogger().setLevel(loggingMap[log])
    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx, output)
    oai_ids = Digitool(digitool_category,xml_dirname).download_list()
    categories[group](oai_ids,dtx,c)
    print(c)

@cli.command()
@click.option('--log', default='error', type=click.Choice(loggingMap.keys()), help='Logging level')
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

@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
def dspace(dspace_admin_passwd, dspace_admin_username):
    metadata = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Od jinud" } 
                ]}
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    #ds.handle("123456789/23900")
    #ds.new_item(273,metadata,["lorem-ipsum.pdf"])
    ds.delete_all_item(273)
    #ds.post_new_bitstream(5781,"lorem-ipsum.pdf")
    #ds.delete_bitstream([6654,6655])
    #ds.list_bitstream()
    ds.logout()

def convertItem(oai_id, test):
    dt = Digitool(digitool_category) 
    record = dt.get_item(oai_id)
    
    dtx = DigitoolXML(xml_dirname)
    categorize = Categorize(dtx)
    originalMetadata = dtx.get_metadata(oai_id)
    if 'marc' in originalMetadata.keys():
        pass
        c = Metadata(categorize,oai_id)
        convertedMetadata = c.convertMarc(originalMetadata['marc'])
    else:
        raise Exception("No marc metadata in {}".format(oai_id))

    attachements = list(dtx.get_attachements(oai_id))
    if test:
        #click.clear()
        print("converting ",oai_id)
        print("\noriginalMetadata:")
        #for i in originalMetadata:
        #    c.printMetadata(originalMetadata[i])
#        print('xml',originalMetadataXML)
        print("\nconvertedMetadata:")
        print("\nattachements:")
        print(attachements)
        #checked = click.confirm("Is converting OK?", default=True)
        checked = True
        return (checked, convertedMetadata, attachements)
    else:
        return (False, convertedMetadata, attachements)

@cli.command()
@click.option('--item', default=104691, help='Digitool OAI id of the item')
@click.option('--test/--no-test', default=False, help='Ask user to check convert')
def convert_item(item, test):
    convertItem(item, test)

@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
@click.option('--test/--no-test', default=False, help='Ask user to check convert')

@click.option('--run/--no-run', default=False, help='Pushih converted data to server')
def convert(dspace_admin_passwd, dspace_admin_username, test, run):
    oai_ids = Digitool(digitool_category).download_list()
    dtx = DigitoolXML(xml_dirname)
    categorize = Categorize(dtx)
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)

    problems = []
    for oai_id in oai_ids:
        checked, convertedMetadata, attachements = convertItem(oai_id, test)
        if not checked:
            problems.append(oai_id)
        if run:
            ds.new_item(273,converted_metadata,[("lorem-ipsum.pdf","application/pdf","Dokument")])
    if test:
        click.clear()
        print("problems",problems)
    ds.logout()

if __name__ == '__main__':
    cli()
