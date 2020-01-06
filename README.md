Digitool to dspace importer of CERGE source

# Install & run
```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
python3 source/digitoolTOdspace.py --help 
```

# Detailed converting instruction

Prepare structure for source data
```
FOLDER='Cerge'
mkdir -p $FOLDER/$(date +%F)
```

Download xml with metadata:
````
scp -r novotj@dingo.is.cuni.cz:/exlibris/dtl/j3_1/digitool/home/profile/export/export_Jitka/$FOLDER/digital_entities $FOLDER/$(date +%F)/digital_entities
```

Download list of assets for quick testing of metadata: (recommended for thesis)
```
ssh novotj@dingo.is.cuni.cz "ls /exlibris/dtl/j3_1/digitool/home/profile/export/export_Jitka/$FOLDER/streams/ > /home/novotj/ls_streams.txt"
scp -r novotj@dingo.is.cuni.cz:/home/novotj/ls_streams.txt $FOLDER/$(date +%F)
```
or download all assets: (recommended for Cerge)
```
scp -r novotj@dingo.is.cuni.cz:/exlibris/dtl/j3_1/digitool/home/profile/export/export_Jitka/$FOLDER/streams/ $FOLDER/$(date +%F)/streams/
```

Create simple archive format:
```
python3 source/digitoolTOdspace.py convert --archive --copyfile
```

Upload simple archive format:
```
scp -r output/* novotj@gull.is.cuni.cz:/dspace/cerge
```

Login to gull:
```
ssh novotj@gull.is.cuni.cz
sudo -i -u dspace
```

Import the first three items:

```
ls /dspace/cerge/ | head -n 3 | while read -r ID ; do /opt/dspace/bin/dspace import -a -e jitkaucw@gmail.com -s /dspace/cerge/$ID -c 284 -m /dspace/mapfile_zaloha/cerge/$ID; done
```
