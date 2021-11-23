import logging
import os.path
from Cryptodome import Random
import markdown

import os
import binascii

import Cryptodome.Cipher.AES as AES
from app.library.aes_ctr import CTRCipher, int_from_bytes, int_to_bytes

from app.models.api_keys import ApiKeyResponse


def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data


def aes_encrypt(plaintext, ctr_key):
    iv = Random.new().read(AES.block_size)
    decryptor = CTRCipher(binascii.a2b_hex(ctr_key))

    # str -> byte
    buf = decryptor.encrypt(plaintext.encode(), iv)

    # byte -> int -> str
    #ciphertext = int_from_bytes(buf)
    # return str(ciphertext)

    # byte -> hexstr
    ciphertext = bytes2hexstr(buf)
    return ciphertext


def aes_decrypt(ciphertext, ctr_key):
    decryptor = CTRCipher(binascii.a2b_hex(ctr_key))

    # str -> int -> byte -> str
    # return bytes.decode(decryptor.decrypt(int_to_bytes(int(ciphertext))))

    # hexstr -> byte -> str
    return bytes.decode(decryptor.decrypt(hexstr2bytes(ciphertext)))


def bytes2hexstr(bs):
    return ''.join(['%02x' % b for b in bs])


def hexstr2bytes(str):
    return bytes.fromhex(str)


def mask_api_keys(api_keys, ctr_key, app_name):
    apiKeyList = []
    for k in api_keys:
        if k.app_name == app_name:
            item = ApiKeyResponse.from_orm(k)
            secret_key = aes_decrypt(item.secret_key, ctr_key)
            #logging.debug("api_key={0} secret_key(decrypted)={1}".format(item.api_key, secret_key))
            item.secret_key = mask_text(secret_key)
            apiKeyList.append(item)
    return apiKeyList


def mask_text(text):
    n = len(text)
    if n > 4:
        text = "{0}{1}{2}".format(
            text[0:2], "*"*(n-4), text[-2:])
    else:
        text = "*" * n
    return text
