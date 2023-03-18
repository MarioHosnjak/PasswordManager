#WINDOWS
#run init() -> python -c 'import pwManager; pwManager.init()' "masterPassword"
#run put() -> python -c 'import pwManager; pwManager.put()' "masterPassword" "address" "password"
#run get() -> python -c 'import pwManager; pwManager.get()' "masterPassword" "address"

#LINUX
#run init() -> python3 -c 'import pwManager; pwManager.init()' "masterPassword"
#run put() -> python3 -c 'import pwManager; pwManager.put()' "masterPassword" "address" "password"
#run get() -> python3 -c 'import pwManager; pwManager.get()' "masterPassword" "address"

from sys import argv

#PBKDF2
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

#AES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Util import Counter

#SHA-256
from Crypto.Hash import SHA256

tag_size = 16

def init():
    password = argv[1]
    salt = get_random_bytes(16)
    #Generate a key
    key = PBKDF2(password, salt, 32, count=310000, hmac_hash_module=SHA512)
    #Hash the key
    hash_obj = SHA256.new()
    hash_obj.update(key)
    hash_value = hash_obj.digest()
    #Save the salt and hash
    file1 = open("baza.txt","wb+")
    file1.write(salt+hash_value+b'\n')
    print("Password manager initialized.")
    file1.close()

def put():
    masterPassword = argv[1]
    address = argv[2]
    password = argv[3]

    oldKey = evaluateKey(masterPassword)
    if not oldKey:
        return

    i, existingSalt = findInFile(oldKey, address)
    if i:
        newSalt = get_random_bytes(16)
        ctxt1 = encrypt(oldKey, address, newSalt)
        ctxt2 = encrypt(oldKey, password, newSalt)
        replaceLine(ctxt1, ctxt2, i, newSalt)
    else:
        salt = get_random_bytes(16)
        ctxt1 = encrypt(oldKey, address, salt)
        ctxt2 = encrypt(oldKey, password, salt)
        file1 = open("baza.txt","ab")
        file1.write(salt + ctxt1 + ctxt2)
        file1.close()
    print("Stored password for " + address)


def encrypt(key, plaintext, salt):
    cipher = AES.new(key, AES.MODE_EAX, nonce=salt)
    paddedPlaintext = pad(bytes(plaintext, 'utf-8'), 16)
    paddedPlaintext = enlarge_string(paddedPlaintext)
    ctxt, tag = cipher.encrypt_and_digest(paddedPlaintext)
    return ctxt + tag

def decrypt(key, ciphertext, salt):
    cipher = AES.new(key, AES.MODE_EAX, nonce=salt)
    ctxt = ciphertext[:len(ciphertext)-tag_size]
    tag = ciphertext[len(ciphertext)-tag_size:]
    try:
        plaintext = cipher.decrypt_and_verify(ctxt, tag)
        return plaintext
    except ValueError:
        print("Error: ciphertext is invalid or key is incorrect")
        
def evaluateKey(masterPassword):
    file1 = open("baza.txt","rb+")
    firstLine = file1.read(48)
    salt = firstLine[:16]
    oldKeyHash = firstLine[16:48]
    file1.close()

    newKey = PBKDF2(masterPassword, salt, 32, count=310000, hmac_hash_module=SHA512)

    hash_obj = SHA256.new()
    hash_obj.update(newKey)
    hash_value = hash_obj.digest()

    if(hash_value != oldKeyHash):
        print("Master password incorrect or integrity check failed.")
        return False
    else:
        return newKey

def findInFile(key, address):
    file1 = open("baza.txt","rb")
    file1.seek(16+32+len('\n'))
    i = 1
    while 1==1:
        pair = file1.read(512+16)
        if not pair:
            return False, None
        salt = pair[:16]
        cipherTxt = encrypt(key, address, salt)
        if cipherTxt in pair:
            return i, salt
        i = i + 1
    file1.close()

def replaceLine(cipherTxt1, cipherTxt2, i, salt):
    file1 = open("baza.txt", "rb+")
    file1.seek(16+32+len('\n')+(512+16)*(i-1))

    #DELETE NEXT 512 BYTES
    pos = file1.tell()
    file1.seek(pos + 512 + 16)
    data = file1.read()
    file1.seek(pos)
    file1.write(data)
    file1.truncate()

    file1.write(salt + cipherTxt1 + cipherTxt2)
    file1.close()

def get():
    masterPassword = argv[1]
    address = argv[2]

    oldKey = evaluateKey(masterPassword)
    if not oldKey:
        return

    i, existingSalt = findInFile(oldKey, address)
    if i:
        file1 = open("baza.txt", "rb")
        file1.seek(16+32+len('\n')+(512+16)*(i-1)+256+16)
        password = file1.read(256)
        file1.close()
        password = decrypt(oldKey, password, existingSalt)
        password = remove_trailing_whitespace(password)
        password = str(unpad(password, 16), 'utf-8')
        print("Password for " + address + " is: " + password + ".")
    else:
        print('Master password incorrect or integrity check failed.')

def printAll():
    file1 = open("baza.txt", "rb")
    lines = file1.read()
    print(lines)
    file1.close()

def enlarge_string(string):
    while len(string) < 256-16:
        string += b' '
    return string

def remove_trailing_whitespace(string):
    return string.rstrip(b' ')