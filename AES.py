import hashlib, binascii, hmac
import os, scrypt, secrets
import json, pyaes
from Crypto.Cipher import AES


# 1.1) Symmetric Encryption & Decryption

message = 'exercise-cryptograpy'
password = 'p@$$s0rd~3'

# Scrypt Key Derivation (512 bit = 64 bytes)

salt = os.urandom(32)
print("Salt (256): ", binascii.hexlify(salt))

n = 16384
r = 16
p = 1
derived_key_length = 64

derivedKey = scrypt.hash(password, salt, n, r, p, derived_key_length)
derivedKey_hex = binascii.hexlify(derivedKey)
print("Derived Key: ", derivedKey_hex)

dklen = derived_key_length

# Split Derived Key --> Encryption Key (1st 256 bits)

encryptionKey = derivedKey_hex[:64]
print("Encryption Key: ", encryptionKey)

## for AES CBC (32 bytes)

encryptionKey32 = derivedKey_hex[:32]
print("Encryption Key (32): ", encryptionKey32)

# Split Derived Key --> HMAC Key (2nd 256 bits)

hmacKey = derivedKey_hex[64:]
print("HMAC Key: ", hmacKey)

# AES Message Encryption --> Cipher Text w/ PKCS7 Padding

iv = (secrets.randbelow(256)).to_bytes(16, byteorder = 'big')
print("Initialization Vector (iv16): ", iv)

# block_size = 16

def pad(m):
    return m+chr(16-len(m)%16)*(16-len(m)%16)
    # return m+chr(AES.block_size-len(m)%AES.block_size)*(AES.block_size-len(m)%AES.block_size)

def unpad(ct):
    return ct[:-ct[-1]]
    # return ct[:-ord(ct[-1])]

#aes = pyaes.AESModeOfOperationCBC(encryptionKey32, iv)
aes = AES.new(encryptionKey32, AES.MODE_CBC, iv)
cipherText = aes.encrypt(pad(message).encode('utf8'))
print("Encrypted Message: ", binascii.hexlify(cipherText))

# AES Message Decryption --> Plain Text

aes = AES.new(encryptionKey32, AES.MODE_CBC, iv)
plainText = unpad(aes.decrypt(cipherText))
print("Decrypted Message: ", plainText)

# Hash-based MAC using HMAC-SHA256(message, hmac_key)

def hmac_sha256(key, msg):
    return hmac.new(key, msg, hashlib.sha256).digest()

key = binascii.unhexlify(hmacKey)
msg = message.encode('utf8')
hmac = binascii.hexlify(hmac_sha256(key, msg))

print("HMAC: ", hmac)

outPut = {
    "Scrypt": {
        "dklen": str(dklen),
        "Salt": str(binascii.hexlify(salt)),
        "n": str(n),
        "r": str(r),
        "p": str(p),
    },
    "aes": str(binascii.hexlify(cipherText)),
    "iv": str(binascii.hexlify(iv)),
    "mac": str(hmac),
}

print(json.dumps(outPut))
