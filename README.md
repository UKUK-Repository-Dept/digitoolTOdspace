Digitool to dspace importer.

This tool was to delevelop to import set of object and found those which need manual repair in digitool before importing.

Primary source is digitool xml file export and we use digitool oai to chceck if the origin has all attachment link to some file with metatadata and to determine parent object.

# Install & run
```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
pytest
python3 source/digitoolTOdspace.py --help 
```

