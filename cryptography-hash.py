import hashlib, binascii, os
import hmac
import scrypt

# 1. Calculate Hashes - SHA256, SHA3-265, SHA512, RIPEMD160

msg = 'exercise-cryptography'

data = msg.encode("utf8")

sha256 = hashlib.sha256(data).digest()
print("SHA256: ", binascii.hexlify(sha256))

sha3_256 = hashlib.sha3_256(data).digest()
print("SHA3-256: ", binascii.hexlify(sha3_256))

sha512 = hashlib.sha512(data).digest()
print("SHA512: ", binascii.hexlify(sha512))

ripemd160 = hashlib.new('ripemd160', data).digest()
print("RIPEMD-160: ", binascii.hexlify(ripemd160))

# 2. Calculate HMAC-SHA-256
shared_key = "secret"

#shared_key.encode("utf8")

#key = binascii.unhexlify(shared_key.encode("utf8"))

def hmac_sha256(key, data):
    return hmac.new(shared_key.encode("utf8"), data, hashlib.sha256).digest()

print("HMAC: ", binascii.hexlify(hmac_sha256(shared_key.encode("utf8"), data)))

# 3. Derive Key by Password using SCrypt

password = "secret"
salt = "mysalt"

my_salt = salt.encode("utf8")

print("Salt: ", binascii.hexlify(my_salt))

key256 = scrypt.hash(password, my_salt, 16384, 16, 1, 32)
print("Derived Key: ", binascii.hexlify(key256))

key512 = scrypt.hash(password, my_salt, 16384, 16, 1, 64)
print("Derived Key: ", binascii.hexlify(key512))
