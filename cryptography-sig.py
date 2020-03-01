import eth_keys, binascii
import bitcoin, hashlib
import base58

#1 Ethereum Signature Creator

privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(
    "97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"))
print("Private Key (64 hex digits): ", privKey)

signature = privKey.sign_msg(b'exercise-cryptography')

#print('Signature: [v = {0}, r = {1}, s = {2}]'.format(hex(signature.v),
    #hex(signature.r), hex(signature.s)))
print("Signature (130 hex digits): ", signature)

msg = b'exercise-cryptography'
print('Message:', msg)


print()

#2 Ethereum Signature to Address

pubKey = signature.recover_public_key_from_msg(b'exercise-cryptography')

#pubKey = eth_keys.keys.PublicKey.recover_from_msg(b'exercise-cryptography', signature)

#pubKey = privKey.public_key

address = pubKey.to_checksum_address()
print("Ethereum Address: ", address)

print()

#3.1 Ethereum Signature to Verifier: Bool == TRUE

msg = b'exercise-cryptography'

address = "0xa44f70834a711F0DF388ab016465f2eEb255dEd0"

signature = eth_keys.keys.Signature(binascii.unhexlify('acd0acd4eabd1bec05393b33b4018fa38b69eba8f16ac3d60eec9f4d2abc127e3c92939e680b91b094242af80fce6f217a34197a69d35edaf616cb0c3da4265b01'))

signer_pubKey = signature.recover_public_key_from_msg(msg)

signer_address = signer_pubKey.to_checksum_address()
print("Signer Address: ", signer_address)
print("Signature Valid?: ", signer_address == address)

print()

#3.2 Ethereum Signature to Verifier: BOOL == FALSE

msg = b'exercise-cryptography'

address = "0xa44f70834a711F0DF388ab016465f2eEb255dEd0"

signature = eth_keys.keys.Signature(binascii.unhexlify('5550acd4eabd1bec05393b33b4018fa38b69eba8f16ac3d60eec9f4d2abc127e3c92939e680b91b094242af80fce6f217a34197a69d35edaf616cb0c3da4265b01'))

signer_pubKey = signature.recover_public_key_from_msg(msg)

signer_address = signer_pubKey.to_checksum_address()
print("Signer Address: ", signer_address)
print("Signature Valid?: ", signer_address == address)

print()

#4 Private Key to Bitcoin Address

def private_key_to_public_key(privKeyHex: str) -> (int, int):
    privateKey = int(privKeyHex, 16)
    return bitcoin.fast_multiply(bitcoin.G, privateKey)

def pubkey_to_address(pubKey: str, magic_byte = 0) -> str:
    pubKeyBytes = binascii.unhexlify(pubKey)
    sha256val = hashlib.sha256(pubKeyBytes).digest()
    ripemd160val = hashlib.new('ripemd160', sha256val).digest()
    return bitcoin.bin_to_b58check(ripemd160val, magic_byte)



priv_key = base58.b58decode('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ')

private_key = binascii.hexlify(priv_key)
prKey = private_key[2:-8]
print("Private Key (hex): ", prKey)


public_key = private_key_to_public_key(prKey)
print("Public key (x,y) coordinates: ", public_key)

compressed_public_key = bitcoin.compress(public_key)
print("Public key (hex compressed): ", compressed_public_key)

print()

address = bitcoin.pubkey_to_address(public_key)
print("Address: ", address)

address1 = pubkey_to_address(compressed_public_key)
print("Compressed Bitcoin Address (bas58check): ", address1)

addressDEC = base58.b58decode(address1)
print(addressDEC)
