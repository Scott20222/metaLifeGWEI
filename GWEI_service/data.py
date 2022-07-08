import peewee
import json, time
from web3 import Web3
from eth_abi.abi import decode_abi

with open('config.json') as f:
    config = json.load(f)

db = peewee.SqliteDatabase('/var/run/data/' + config['db_name'])
#db = peewee.SqliteDatabase('test.db')

IMG_FOLDERS = '/var/run/data/imgs'

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Mints(BaseModel):
    mint_id = peewee.AutoField()
    token_id = peewee.IntegerField(null=True)
    name = peewee.CharField()
    email = peewee.CharField()
    address = peewee.CharField(null=True)
    status = peewee.IntegerField(default=0,index=True)
        #0:created 9:ipfs_img_done 1:ipfs_json_done 2:mint_tx_sent 3:minted_to_miner 4:minted_to_client 5:tx_failed
    photo = peewee.CharField()
    ipfs_uri = peewee.CharField(null=True)
    ipfs_hash = peewee.CharField(null=True)
    mint_tx = peewee.CharField(null=True)
    update_time = peewee.IntegerField(null=True)
    def save(self, *args, **kwargs):
        self.update_time = int(time.time())
        return super(Mints, self).save(*args, **kwargs)

class System(BaseModel):
    key = peewee.CharField(index=True)
    value = peewee.CharField()

try:
    System.get()
except:
    _init = True
else:
    _init = False

if _init:
    print('initing database')
    db.create_tables([Mints, System])
    System.create(key='created', value='aye')
