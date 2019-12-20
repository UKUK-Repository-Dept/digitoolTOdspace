Digitool to dspace importer of CERGE source

# Install & run
```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
pytest
python3 source/digitoolTOdspace.py --help 
```

# File export from digitool
```
FOLDER='Cerge'
ssh novotj@dingo.is.cuni.cz "ls /exlibris/dtl/j3_1/digitool/home/profile/export/export_Jitka/$FOLDER/streams/ > /home/novotj/ls_streams.txt"
mkdir -p $FOLDER/$(date +%F)
scp -r novotj@dingo.is.cuni.cz:/home/novotj/ls_streams.txt $FOLDER/$(date +%F)
scp -r novotj@dingo.is.cuni.cz:/exlibris/dtl/j3_1/digitool/home/profile/export/export_Jitka/$FOLDER/digital_entities $FOLDER/$(date +%F)/digital_entities
```

Import on gull #TODO jen jedna zbírka
```
cat /dspace/kvalifikacni2006/gull | while read -r id col ; do /opt/dspace/bin/dspace import -a -e jitkaucw@gmail.com -s /dspace/kvalifikacni2006/$id -c $col -m /tmp/mapfile/$id; done
```
