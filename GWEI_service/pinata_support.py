import os,time, json
import requests, uuid
from data import config

def pinata_push(file, path = None, name = 'name'):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload={
        'pinataOptions': json.dumps({"cidVersion": 1}),
        'pinataMetadata': json.dumps({"name": "Genesis GWEI NFT",
            "description": "Commemorative NFT collection for "
            "the genesis Global Web3 Eco Innovation Summit (GWEI) held at The Marina Sand Bay Convention "
            "Centre on 14th July 2022, co-hosted by the Singapore University of Social Science and DeFiDAO News. "
            "%s "
            "Minted time %s." %(name,time.asctime( time.localtime(time.time()) ))})
            }

    if path:
        file_with_path = os.path.join(path, file)
    else:
        file_with_path = file

    with open(file_with_path,'rb') as f:
        files=[
          ('file',(file, f, 'application/octet-stream'))
        ]

        headers = {
            'pinata_api_key': config['pinata_api_key'],
            'pinata_secret_api_key': config['pinata_api_secret']
        }
        while True:
            try:
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                break
            except requests.exceptions.ProxyError:
                continue
    if response.status_code == 200:
        return response.json()['IpfsHash']
    else:
        raise ConnectionError(response.text)

def pinata_img_hash_to_json(img_hash, path = None, name = 'name'):
    filename = uuid.uuid1().hex + '.json'
    raw_filename = filename
    if path:
        filename = os.path.join(path, filename)
    data = {"name": "Genesis GWEI NFT",
        "description": "Commemorative NFT collection for "
            "the genesis Global Web3 Eco Innovation Summit (GWEI) held at The Marina Sand Bay Convention "
            "Centre on 14th July 2022, co-hosted by the Singapore University of Social Science and DeFiDAO News. ",
        "image": "ipfs://"+img_hash,
        "mint to": name,
        "timestamp": str(int(time.time()))
        }
    with open(filename, 'w') as f:
        json.dump(data, f)
    return raw_filename
