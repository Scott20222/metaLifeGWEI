from web3 import Web3
from abi import metaMasterABI, collectionABI
from data import *
from web3.exceptions import BadFunctionCallOutput, TransactionNotFound
from eth_abi.abi import decode_abi

web3 = Web3(Web3.HTTPProvider(config['specturm_endpoint']))

meta_master_contract = web3.eth.contract(address=web3.toChecksumAddress(config['meta_master_address']),abi=metaMasterABI)

collection_address = web3.toChecksumAddress(config['collection_address'])

collection_contract = web3.eth.contract(address=collection_address,abi=collectionABI)

def get_config_bug():
    try:
        meta_master_contract.functions.feeCollector().call()
    except BadFunctionCallOutput:
        return 'Invalid metamaster address'
    try:
        collection_owner = meta_master_contract.functions.collectionOwner(collection_address).call()
    except BadFunctionCallOutput:
        return 'Invalid collection address'
    if collection_owner == '0x0000000000000000000000000000000000000000':
        return 'Invalid collection address'
    return None

def get_nonce(address):
    address = web3.toChecksumAddress(address)
    nonce_chain = web3.eth.get_transaction_count(address)
    if address == web3.toChecksumAddress(config['miner_address']):
        try:
            nonce = int(System.get(key=address).value)
        except:
            nonce = nonce_chain
            System.create(key=address, value=str(nonce))
    return max(nonce, nonce_chain)

def add_nonce(address):
    address = web3.toChecksumAddress(address)
    item = System.get(key=address)
    item.value = str(int(item.value)+1)
    item.save()

def mint_nft(ipfs_hash, to_address = None):
    miner_address = web3.toChecksumAddress(config['miner_address'])
    nonce = get_nonce(miner_address)
    if to_address is None:
        to_address = miner_address
    mint_txn = meta_master_contract.functions.mint(
        collection_address,
        to_address,
        ipfs_hash,
        ).buildTransaction({
        'chainId': 20180430,
        'gas': 300000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce
        })
    signed_txn = web3.eth.account.sign_transaction(mint_txn, private_key=config['miner_private_key'])
    _hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    add_nonce(miner_address)
    return _hash.hex()

def transfer_nft(token_id, to_address):
    miner_address = web3.toChecksumAddress(config['miner_address'])
    nonce = get_nonce(miner_address)
    txn = meta_master_contract.functions.transfer(
        collection_address,
        token_id,
        web3.toChecksumAddress(to_address),
        ).buildTransaction({
        'chainId': 20180430,
        'gas': 300000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce
        })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=config['miner_private_key'])
    _hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    add_nonce(miner_address)
    return _hash.hex()

def query_mint_tx_status(tx_hash):
    try:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
    except TransactionNotFound:
        return 2, None
    if receipt['status'] == 1:
        for log in receipt['logs']:
            if log['topics'][0].hex() == '0xf3cea5493d790af0133817606f7350a91d7f154ea52eaa79d179d4d231e50102':
                token_id, to_address = decode_abi(['uint', 'address'], bytes.fromhex(log['data'][2:]))
                if web3.toChecksumAddress(to_address) == web3.toChecksumAddress(config['miner_address']):
                    return 3, token_id
                else:
                    return 4, token_id
    elif receipt['status'] == 0:
        return 2, None
    else:
        return 5, None
