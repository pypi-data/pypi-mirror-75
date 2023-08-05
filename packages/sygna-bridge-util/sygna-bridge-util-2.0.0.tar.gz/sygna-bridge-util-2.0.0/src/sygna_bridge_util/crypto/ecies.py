import ecies
from typing import Union
from .utils import get_shared_secret, aes256_cbc_encrypt, sha512, hmac_sha1, pad, decrypt_and_verify


def ecies_encrypt(msg: str, receiver_pk: Union[str, bytes], ) -> str:
    """
       Sygna Bridge encrypt with receiver's secp256k1 public key

       Parameters
       ----------
       receiver_pk: Union[str, bytes]
           Receiver's public key (hex str or bytes)
       msg: bytes
           Data to encrypt

       Returns
       -------
       hex str
           Pubkey(65B)+MAC key(20B)+Encrypted data(16B)=>private info
       """

    ephemeral = ecies.generate_key()

    if isinstance(receiver_pk, str):
        receiver_pubkey = ecies.hex2pub(receiver_pk)
    elif isinstance(receiver_pk, bytes):
        receiver_pubkey = ecies.PublicKey(receiver_pk)
    else:
        raise TypeError("Invalid public key type")

    shared_secret = get_shared_secret(ephemeral.secret, receiver_pubkey)
    hashed_secret = sha512(shared_secret)
    encryption_key = hashed_secret[0: 32]
    mac_key = hashed_secret[32:len(hashed_secret)]
    msg = pad(msg)
    message_b = bytes(msg, 'utf-8')
    iv = bytearray([0] * 16)  # [0] * 16
    cipher_text = aes256_cbc_encrypt(iv, encryption_key, message_b)
    ephemeral_pub_key = ephemeral.public_key.format(False)
    mac_msg = b''.join([bytes(iv), ephemeral_pub_key, cipher_text])
    tag = hmac_sha1(mac_key, mac_msg)
    result = b''.join([ephemeral_pub_key, tag, cipher_text])

    return result.hex()


def ecies_decrypt(enc_message: str, private_key: str) -> str:

    """Sygna Bridge ECIES Decrypt.
     Args:
        enc_message (str): encode_message whole hex string encrypted by Sygna ECIES
        private_key (str)

     Returns:
        bytes.
     """
    enc_message_b = bytes.fromhex(enc_message)
    ephemeral_pub_key = ecies.PublicKey(enc_message_b[0:65])  # uncompressed pubkey's length is 65 bytes
    received_mac_tag = enc_message_b[65:85]
    ciphered_data = enc_message_b[85:]
    ephemeral = ecies.hex2prv(private_key)
    shared_secret = get_shared_secret(ephemeral.secret, ephemeral_pub_key)
    hashed_secret = sha512(shared_secret)
    enc_key = hashed_secret[0: 32]
    mac_key = hashed_secret[32:len(hashed_secret)]
    iv = bytearray([0] * 16)
    mac_msg = b''.join([bytes(iv), ephemeral_pub_key.format(False), ciphered_data])
    verified_mac_tag = hmac_sha1(mac_key, mac_msg)

    return decrypt_and_verify(iv, enc_key, ciphered_data, received_mac_tag, verified_mac_tag)
