# PasswordManager
Simple terminal operated password manager written in Python

## How to use

### WINDOWS
Initialize a new .txt database with a new master password ---> python -c 'import pwManager; pwManager.init()' "masterPassword"
Add a new address-password pair or change password ---> python -c 'import pwManager; pwManager.put()' "masterPassword" "address" "password"
Get the password of the specified address ---> python -c 'import pwManager; pwManager.get()' "masterPassword" "address"

### LINUX
Initialize a new .txt database with a new master password ---> python3 -c 'import pwManager; pwManager.init()' "masterPassword"
Add a new address-password pair or change password ---> python3 -c 'import pwManager; pwManager.put()' "masterPassword" "address" "password"
Get the password of the specified address ---> python3 -c 'import pwManager; pwManager.get()' "masterPassword" "address"

## Technologies used
- PBKDF2 - Key derivation
- SHA256 - Key hashing
- AES + EAX - Data encryption and decryption

## Testing in Linux OS
To test the functionality of this password manager simply run the *test.sh* shell script.
