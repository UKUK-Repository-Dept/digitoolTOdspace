#!/usr/bin/python3
import os
import click
from digitoolOAI import Digitool
from digitoolXML import DigitoolXML
from dspace import Dspace
from filenameConvertor import FilenameConvertor
from metadataConvertor import MetadataConvertor
from categorize import Categorize
import problematicGroup as bugs

#xml_dirname = "28.5.2019"
xml_dirname = "18.6.2019"
digitool_category = "oai_kval"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--group', prompt='group', type=click.Choice(['all','oai','forgot','noattachement','weird','502']), help='Choose group to categorize')
def categorize(group):
    #TODO všechny dalši skupiny viz ostatni TODO

    dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx)
    oai_ids = Digitool(digitool_category).download_list()
    if group == 'oai':
        bugs.oai(oai_ids,dtx,c)
    elif group == 'forgot':
        bugs.forgot_attachements(oai_ids,dtx,c,xml_dirname+"/ls_streams.txt")
    elif group == 'noattachement': 
        bugs.no_attachements(oai_ids,dtx,c)
    elif group == 'weird':
        bugs.weird_attachements(oai_ids,dtx,c)
    elif group == '502':
        bugs.tag502(oai_ids,dtx,c)
    elif group == 'all':
        bugs.forgot_attachements(oai_ids,dtx,c,xml_dirname+"/ls_streams.txt")
        bugs.no_attachements(oai_ids,dtx,c)
        bugs.weird_attachements(oai_ids,dtx,c)
        bugs.tag502(oai_ids,dtx,c)
    print(c)


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
    c = MetadataConvertor(categorize)
    originalMetadata = dt.get_metadata(record)
    originalMetadataXML = dtx.get_metadata(oai_id)
    convertedMetadata = "TODO"
    #if originalMetadata is None:
    #    raise Exception("No metadata in {}".format(oai_id))
    #if 'dc' in originalMetadata.keys(): #3112
    #    convertedMetadata = c.convertDC(originalMetadata['dc'], oai_id)
    #if 'record' in originalMetadata.keys(): #358, žádný průnik
    #    convertedMetadata = c.convertRecord(originalMetadata['record'], oai_id)
    if 'marc' in originalMetadataXML.keys():
        convertedMetadata2 = c.convertMarc(originalMetadataXML['marc'], oai_id)
    #else:
    #    raise Exception("No metadata in {}".format(oai_id))

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
    c = MetadataConvertor(categorize)
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
