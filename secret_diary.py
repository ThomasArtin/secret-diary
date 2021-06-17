import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import glob
import pickle

####################################################################
####################################################################
def read_file(file):
    with open(file,'rb') as f:
        data = f.read()
    f.close()
    return data

def write_file(file,data):
    open(file, "w").close()
    with open(file,'wb') as f:
        f.write(data)
    f.close()

def seed_to_key(seed):
    backend = default_backend()
    salt = b"\xb9\x1f|}'S\xa1\x96\xeb\x154\x04\x88\xf3\xdf\x05"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = base64.urlsafe_b64encode(kdf.derive(seed.encode('ascii')))
    return key

def encrypt_file(file,seed):
    data = read_file(file)
    key = seed_to_key(seed)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    write_file(file,encrypted)

def decrypt_file(file,seed):
    data = read_file(file)
    key = seed_to_key(seed)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    write_file(file,decrypted)
####################################################################
####################################################################

previous_exists = False

diary_path = 'Diaries'
diary_path = os.path.join(os.path.dirname(__file__), diary_path)

if not os.path.exists(diary_path):
    os.makedirs(diary_path)

existing_diaries = glob.glob(diary_path+'/*.txt')

if(len(existing_diaries) != 0):

    meta_dir = 'meta'
    meta_dir = os.path.join(os.path.dirname(__file__), meta_dir)
    meta_diaries = 'previous.pkl'

    previous_diaries = []
    diaries = []

    key_seed = input('enter password :\n')


    if not os.path.exists(meta_dir):
        os.makedirs(meta_dir)
    else:
        previous_exists = True

    if previous_exists:

        with open(meta_dir + '/ ' + meta_diaries, 'rb') as f:

            previous_diaries  = pickle.load(f)

        for diary in glob.glob(diary_path+'/*.txt'):
            diaries.append(diary)
            if diary in previous_diaries:
                decrypt_file(diary,key_seed)

    else:
        for diary in glob.glob(diary_path+'/*.txt'):

            diaries.append(diary)





    to_quit = input('press any key to quit\n')

    with open(meta_dir + '/ ' + meta_diaries, 'wb') as f:
        
        pickle.dump(diaries, f)

    for diary in diaries:

        encrypt_file(diary,key_seed)


