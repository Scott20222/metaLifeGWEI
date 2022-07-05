from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import uuid, os, hashlib, time
from data import *
from web3_support import *
from data_exporter import export_data, EXPORTS_FOLDER

app = Flask(__name__)
app.secret_key = "yibor!!!"

CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'HEAD', 'POST', 'OPTIONS'],supports_credentials=True)

def api_response(data, errorCode = 0):
    return jsonify({'success': errorCode == 0, 'msg': data, 'code': errorCode, 'timestamp': int(time.time())})

def img_name_to_folder(raw_filename, save=False, hashing=True):
    if hashing:
        folder = str(int(hashlib.sha1(raw_filename.encode()).hexdigest()[:2],16))
    else:
        folder = raw_filename
    path = os.path.join(IMG_FOLDERS, folder)
    if save:
        if not os.path.isdir(IMG_FOLDERS):
            os.mkdir(IMG_FOLDERS)
        if not os.path.isdir(path):
            os.mkdir(path)
    return path

def img_file_exist(filename):
    return os.path.isfile(img_name_to_folder(filename, hashing = False))

@app.route('/upload', methods=['POST'])
def app_upload_file():
    if 'file' not in request.files:
        return api_response('No file included', 104)
    file = request.files['file']
    filename = uuid.uuid1().hex + '.' + file.filename.rsplit('.', 1)[-1].lower()
    file.save(img_name_to_folder(filename, True))
    return api_response(filename)

@app.route('/creat', methods=['POST'])
def app_creat_nft():
    try:
        name = str(request.json['name'])
        email = str(request.json['email'])
        photo = str(request.json['photo'])
        wallet = request.json.get('wallet')
    except KeyError:
        return api_response('invalid input', 101)
    if wallet:
        try:
            wallet = web3.toChecksumAddress(wallet)
        except ValueError:
            return api_response('invalid wallet address', 101)
    if not img_file_exist(photo):
        return api_response('please upload photo first', 102)
    Mints.create(name=name,email=email,photo=photo,address=wallet)
    return api_response('success')

@app.route('/export', methods=['GET','POST'])
def app_export_data():
    filename = export_data()
    return send_from_directory(EXPORTS_FOLDER, filename, as_attachment=False)

if __name__ =='__main__':
    app.run(port=5050, debug = True)
