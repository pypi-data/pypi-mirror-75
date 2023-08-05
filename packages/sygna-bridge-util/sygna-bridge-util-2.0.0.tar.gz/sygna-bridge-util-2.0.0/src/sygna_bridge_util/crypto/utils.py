from Crypto.Cipher import AES
import hashlib
import hmac

__all__ = [
    "get_shared_secret",
    "aes256_cbc_encrypt",
    "sha512",
    "hmac_sha1",
    "pad",
    "verify",
    "decrypt_and_verify",
    "aes256_cbc_decrypt"
]


def get_shared_secret(ephemeral_key: object, receiver_pubkey: bytes) -> bytes:
    return receiver_pubkey.multiply(ephemeral_key).format(True)[1:]


def aes256_cbc_encrypt(iv, key, plain_text):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(plain_text)


def aes256_cbc_decrypt(iv, key, cipher_text):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(cipher_text)


def sha512(message: str) -> str:
    return hashlib.sha512(message).digest()


def hmac_sha1(key: str, message: str) -> bytes:
    digester = hmac.new(key, message, hashlib.sha1).digest()
    mac = digester
    print(mac)
    return mac


def pad(plain_text):

    # block_size = AES.block_size  # Size of a data block (in bytes) =16
    # number_of_bytes_to_pad = block_size - len(plain_text) % block_size
    # ascii_string = chr(number_of_bytes_to_pad)
    # padding_str = number_of_bytes_to_pad * ascii_string
    # padded_plain_text = plain_text + padding_str
    # return padded_plain_text
    """
    padding to blocksize according to PKCS #5
    calculates the number of missing chars to BLOCK_SIZE and pads with
    ord(number of missing chars)
    @see: http://www.di-mgt.com.au/cryptopad.html
    @param plain_text: string to pad
    @type plain_text: string
    @rtype: string
    """
    return plain_text + (AES.block_size - len(plain_text) % AES.block_size) * chr(AES.block_size - len(plain_text) % AES.block_size)


def unpadding(message):
    """
    unpadding according to PKCS #5
          @param message: string to unpad
          @type message: string
          @rtype: string
    """

    return message[0:-ord(message[-1])]


def decrypt_and_verify(iv, enc_key, ciphered_data, received_mac_tag, _mac_tag):
    aes = AES.new(enc_key, AES.MODE_CBC, iv)
    plaintext = aes.decrypt(ciphered_data)
    plaintext = str(plaintext, "utf-8")
    verify(received_mac_tag, _mac_tag)

    return unpadding(plaintext)


def verify(received_mac_tag, mac_tag) -> bool:

    if received_mac_tag != mac_tag:
        raise ValueError("MAC check failed")

    return True
