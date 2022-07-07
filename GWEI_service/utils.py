import uuid, os, hashlib, time
from data import IMG_FOLDERS

def img_name_to_folder(raw_filename, save=False):
    if save:
        if not os.path.isdir(IMG_FOLDERS):
            os.mkdir(IMG_FOLDERS)
    return IMG_FOLDERS

def img_file_exist(filename):
    return os.path.isfile(os.path.join(img_name_to_folder(filename), filename))
