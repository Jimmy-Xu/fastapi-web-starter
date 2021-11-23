import Cryptodome.Cipher.AES as AES
import operator
from binascii import a2b_hex
from Cryptodome import Random

'''
pip install pycryptodomex
'''


def xor_block(left, right):
    return map(operator.xor, left, right)


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


class CTRCipher(object):
    def __init__(self, key):
        self._cipher = AES.new(key, AES.MODE_ECB)
        self.block_size = AES.block_size

    def encrypt(self, plainText, count):
        count = bytes(count)
        counters = self._get_timers(count, len(plainText))
        blocks = xor_block(self._cipher.encrypt(counters), plainText)
        ciphertext = bytes(blocks)
        return count + ciphertext[:len(plainText)]

    def decrypt(self, cipherText):
        blockSZ = self.block_size
        pt = self.encrypt(cipherText[blockSZ:], cipherText[:blockSZ])
        return pt[blockSZ:]

    def _get_timers(self, iv, plaintext_len):
        # iv: 计时器初值
        # plaintext_len: 密文长度(明文)
        blockSZ = self.block_size
        blocks = int((plaintext_len + blockSZ - 1) // blockSZ)
        timer = int_from_bytes(iv)
        timers = iv
        for i in range(1, blocks):
            timer += 1
            timers += int_to_bytes(timer)
        return timers


if __name__ == '__main__':
    iv = Random.new().read(AES.block_size)
    print("iv:", int_from_bytes(iv))
    ctr_key = "2e101c7211144bb08bb03e1597e3139c"
    decryptor = CTRCipher(a2b_hex(ctr_key))

    words = b"helloworld"
    a = decryptor.encrypt(words, iv)
    ciphertext = int_from_bytes(a)
    print("CTR ciphertext：", ciphertext)
    print("CTR plaintext", decryptor.decrypt(int_to_bytes(ciphertext)))
