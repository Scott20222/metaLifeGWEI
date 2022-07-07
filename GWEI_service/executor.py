import time
from utils import img_name_to_folder
from data import *
from web3_support import *
from pinata_support import *

def execute_ipfs():
    for item in Mints.select().where(Mints.status == 0):
        ipfs_hash = pinata_push(item.photo, path=img_name_to_folder(item.name), name = item.name)
        Mints.update(ipfs_hash=ipfs_hash, status=1).where(Mints.mint_id == item.mint_id).execute()
        time.sleep(0.1)

def execute_mint():
    for item in Mints.select().where(Mints.status == 1):
        tx_hash = mint_nft(item.ipfs_hash, item.address)
        Mints.update(mint_tx=tx_hash, status=2).where(Mints.mint_id == item.mint_id).execute()
        time.sleep(0.1)

def execute_check():
    for item in Mints.select().where(Mints.status == 2):
        new_status, token_id = query_mint_tx_status(item.mint_tx)
        if new_status != 2:
            Mints.update(token_id=token_id, status=new_status).where(Mints.mint_id == item.mint_id).execute()
        time.sleep(0.1)

if __name__ == '__main__':
    while True:
        execute_ipfs()
        time.sleep(1)
        execute_mint()
        time.sleep(1)
        execute_check()
        time.sleep(1)
