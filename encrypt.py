import os
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode, b64encode
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad


# En / De cryption Key
key = b'0123456789012345'

# Random Initialization Vector
# iv = Random.get_random_bytes(16)
iv = key

def readFileAsString(file_path='compressed.txt'):
    file = open(file_path,"r",encoding='utf-8')
    data = file.read()
    return data

def convertStrToBytes(cipher):
    if(type(cipher) == str):
        return bytes(cipher,encoding="utf-8")
    else:
        return cipher


def encrypt(string_to_encrypt):
    cipher_to_encrypt = convertStrToBytes(string_to_encrypt)

    cipher = AES.new(key,AES.MODE_CBC,iv)        
    ciphertext = cipher.encrypt(pad(cipher_to_encrypt,16))

    return ciphertext

def decrypt(string_to_decrypt):
    cipher_to_decrypt = convertStrToBytes(string_to_decrypt)


    cipher = AES.new(key,AES.MODE_CBC,iv)        
    decrypted = cipher.decrypt(cipher_to_decrypt)

    return unpad(decrypted,16)

def encryptFourierData(compressed_data):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    ciphertext = cipher.encrypt(pad(convertStrToBytes(compressed_data),16))

    encrypted = b64encode(ciphertext)
    return encrypted

if __name__ == "__main__":
    
    string_to_encrypt = readFileAsString()

    encrypted = encrypt(string_to_encrypt)

    encrypted_encoded = b64encode(encrypted)

    file = open("encrypted_1.txt","w")
    file.write(str(encrypted_encoded))
    file.close()

    print(f" Original Encrypted File Size {os.path.getsize('compressed.txt') / 1e6} vs {os.path.getsize('encrypted_1.txt')/1e6}")

    file = open("decrypted.txt","a+")
    decrypted_decoded = b64decode(encrypted_encoded)

    # file.write("\n\n")

    # file.write(str(decrypted_decoded))
    file.write("\n")

    decrypted = decrypt(decrypted_decoded)
    file.write(str(decrypted))
    file.close()

    print(decrypted)

