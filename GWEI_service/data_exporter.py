import xlsxwriter
from data import *
import uuid, os

EXPORTS_FOLDER = 'exports'

if not os.path.isdir(EXPORTS_FOLDER):
    os.mkdir(EXPORTS_FOLDER)

def export_data():
    filename = uuid.uuid1().hex + '.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'name')
    worksheet.write(0, 1, 'email')
    worksheet.write(0, 2, 'address')
    worksheet.write(0, 3, 'ipfs_hash')
    worksheet.write(0, 4, 'mint_tx_hash')
    worksheet.write(0, 5, 'token_id')
    worksheet.write(0, 6, 'status #0:Recorded, 1:IPFS Uploaded, 2:Mint TX sent, 3:Mint to miner, 4:Mint to client')
    row = 1
    for item in Mints.select():
        worksheet.write(row, 0, item.name)
        worksheet.write(row, 1, item.email)
        worksheet.write(row, 2, item.address)
        worksheet.write(row, 3, item.ipfs_hash)
        worksheet.write(row, 4, item.mint_tx)
        worksheet.write(row, 5, item.token_id)
        worksheet.write(row, 6, item.status)
        row += 1
    workbook.close()
    return filename
