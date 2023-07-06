import base64
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import os
from ytscraper100 import *

#wielkosc_tablicy_bajtow = 100
poprzedni_wynik = int(time.time() * 1000)

def toBase64(string):
    return base64.b64encode(string).decode('utf-8')

def generate_bytes(wielkosc_tablicy_bajtow):
    random_bytes = generuj_wyniki(wielkosc_tablicy_bajtow)
    return random_bytes

def generate_keys():
    modulus_length = 256 * 4
    private_key = RSA.generate(modulus_length, Random.new().read) #randfunc=generate_bytes)
    #private_key = RSA.generate(modulus_length, randfunc=generate_bytes)
    public_key = private_key.publickey()
    return public_key, private_key

def encrypt_message(public_key, message):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return encrypted_message

def decrypt_message(private_key, encrypted_message):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message



current_directory = os.path.dirname(os.path.abspath(__file__))

dirs = os.listdir(current_directory)

file_name1 = "input.txt"
file_name2 = "output.txt"


file_path1 = os.path.join(current_directory, file_name1)
file_path2 = os.path.join(current_directory, file_name2)

if not os.path.isfile(file_path1):
    print(f"File '{file_name1}' not found.")
    exit()

if not os.path.isfile(file_path2):
    print(f"File '{file_name2}' not found.")
    exit()

with open(file_path1, "rb") as file1:
    message = file1.read()

generated_public_key, generated_private_key = generate_keys()

encrypted_message = encrypt_message(generated_public_key, message)

with open(file_path2, "wb") as encrypted_file:
    encrypted_file.write(encrypted_message)

with open(file_path2, "rb") as file2:
    encrypted_message_to_decrypt = file2.read()

decrypted_message = decrypt_message(generated_private_key, encrypted_message_to_decrypt)

if message == decrypted_message:
    print("Decryption successful. The original message matches the decrypted message.")
else:
    print("Decryption failed. The original message does not match the decrypted message.")
