import os
import logging
from Cryptodome import Random
import binascii
import Cryptodome.Cipher.AES as AES
from app.library.aes_ctr import CTRCipher
from app.models.api_keys import ApiKeyResponse


def is_dev_mode():
    return True if str(os.environ.get("DEV_MODE")).lower() == "true" else False


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
            logging.debug("api_key={0} secret_key(decrypted)={1} is_default={2}".format(
                item.api_key, secret_key, item.is_default))
            item.secret_key = mask_text(secret_key)
            apiKeyList.append(item)
    return apiKeyList


def get_default_api_keys(api_keys, ctr_key, app_name, username):
    for k in api_keys:
        if k.app_name == app_name:
            item = ApiKeyResponse.from_orm(k)
            if item.is_default:
                secret_key = aes_decrypt(item.secret_key, ctr_key)
                return item.api_key, secret_key
    logging.warn("no default api key found for app {0}, user {1}".format(
        app_name, username))
    return None, None


def mask_text(text):
    n = len(text)
    if n > 4:
        text = "{0}{1}{2}".format(
            text[0:2], "*" * 3, text[-2:])
    else:
        text = "*" * n
    return text
