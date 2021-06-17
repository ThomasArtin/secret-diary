import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import glob


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


diary_path = 'Diaries/'
diary_path = os.path.join(os.path.dirname(__file__), diary_path)

key_seed = input('enter password :')

diaries = []

for diary in glob.glob(diary_path+'*.txt'):

    diaries.append(diary)
    encrypt_file(diary,key_seed)

to_quit = input('press any key to quit')


for diary in diaries:

    decrypt_file(diary,key_seed)


