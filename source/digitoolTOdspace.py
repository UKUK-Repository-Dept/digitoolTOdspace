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

xml_dirname = "28.5.2019"
digitool_category = "oai_kval"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--group', prompt='group', type=click.Choice(['oai','forgot']), help='Choose group to categorize')
@click.option('--skip/--no-skip', default=False, help='Skip items with known errors')
def categorize(group, skip):
    #TODO všechny dalši skupiny viz ostatni TODO

    if skip:
        dtx = DigitoolXML(xml_dirname, skip_missing=True)
    else:
        dtx = DigitoolXML(xml_dirname)
    c = Categorize(dtx)
    if group == 'oai':
        dt = Digitool(digitool_category) 
        bugs.oai(dt,dtx,c,skip=skip)
    elif group == 'forgot':
        dt = Digitool(digitool_category) 
        bugs.forgot_attachements(dt,dtx,c,xml_dirname+"/ls_streams.txt")
    c.print()

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

@cli.command()
@click.option('--skip/--no-skip', default=False, help='Skip items with known errors')
def descriptions():
    dt = Digitool(digitool_category) 
    dt.download_list()
    if skip:
        dtx = DigitoolXML(xml_dirname, skip_missing=True)
    else:
        dtx = DigitoolXML(xml_dirname)
    c = FilenameConvertor()
    
    problems = []
    for record in dt.list:
        oai_id = dt.get_oai_id(record)
        attachements = list(dtx.get_attachements(oai_id+".xml",full=True))
        if skip:
            if len(attachements) == 0:
                continue
        else:
            if len(attachements) == 0:
                raise Exception("No attachement in {}.",format(oai_id))
        descriptions = c.generate_description(attachements)
        if isinstance(descriptions, list):
            continue
        print(descriptions)

def convertItem(oai_id, test, skip):
    dt = Digitool(digitool_category) 
    record = dt.get_item(oai_id)
    if skip:
        dtx = DigitoolXML(xml_dirname, skip_missing=True)
    else:
        dtx = DigitoolXML(xml_dirname)
    c = MetadataConvertor()
    originalMetadata = dt.get_metadata(record)
    if originalMetadata is None:
        if skip:
            return False
        else:
            raise Exception("No metadata in {}".format(oai_id))
    if 'dc' in originalMetadata.keys(): #3112
        convertedMetadataDC = c.convertDC(originalMetadata['dc'], oai_id)
    if 'record' in originalMetadata.keys(): #358, žádný průnik
        convertedMetadataRecord = c.convertRecord(originalMetadata['record'], oai_id)
    attachements = list(dtx.get_attachements(str(oai_id)+".xml"))
    if test:
        click.clear()
        print("converting ",oai_id)
        print("originalMetadata:\n")
        for i in originalMetadata:
            print(i)
        print("convertedMetadata:\n")
        print("attachements:\n")
        print(attachements)
        checked = click.confirm("Is converting OK?", default=True)
        return (checked, convertedMetadataDC, attachements)
    else:
        return (False, convertedMetadataDC, attachements)

@cli.command()
@click.option('--item', default=104691, help='Digitool OAI id of the item')
@click.option('--test/--no-test', default=False, help='Ask user to check convert')
@click.option('--skip/--no-skip', default=False, help='Skip items with known errors')
def convert_item(item, test, skip):
    convertItem(item, test, skip)

@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
@click.option('--test/--no-test', default=False, help='Ask user to check convert')
@click.option('--run/--no-run', default=False, help='Pushih converted data to server')
@click.option('--skip/--no-skip', default=False, help='Skip items with known errors')
def convert(dspace_admin_passwd, dspace_admin_username, test, run, skip):
    dt = Digitool(digitool_category) 
    dt.download_list()
    if skip:
        dtx = DigitoolXML(xml_dirname, skip_missing=True)
    else:
        dtx = DigitoolXML(xml_dirname)
    c = MetadataConvertor()
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    
    if test:
        problems = []
    for record in dt.list[:10]:
        oai_id = dt.get_oai_id(record)
        checked, convertedMetadata, attachements = convertItem(oai_id, test, skip)
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
