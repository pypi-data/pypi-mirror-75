import json
import copy
from ecdsa.keys import VerifyingKey
from ecdsa.curves import SECP256k1
from typing import Union
from sygna_bridge_util.config import SYGNA_BRIDGE_CENTRAL_PUBKEY
from hashlib import sha256


def verify_data(data: dict, public_key: str = SYGNA_BRIDGE_CENTRAL_PUBKEY) -> bool:
    """ verify data with provided public key or default sygna bridge public key

    Args:
        data: dict
        public_key: str
    Returns:
        bool
    """
    copy_data = copy.deepcopy(data)
    signature = copy_data['signature']
    copy_data['signature'] = ''

    return verify_message(copy_data, signature, public_key)


def verify_message(message: Union[dict, str], signature: str, public_key: str) -> bool:
    """ verify message(utf-8) with signature and public_key"""
    if isinstance(message, dict) is False and isinstance(message, str) is False:
        raise TypeError('message should be dict or str')

    message_str = message if isinstance(message, str) else json.dumps(message, separators=(',', ':'),
                                                                      ensure_ascii=False)
    message_b = message_str.encode('utf-8')
    public_key_b_obj = bytearray.fromhex(public_key)
    signature_b_obj = bytearray.fromhex(signature)
    vk = VerifyingKey.from_string(string=public_key_b_obj, curve=SECP256k1)
    is_valid = vk.verify(signature=signature_b_obj, data=message_b, hashfunc=sha256)

    return is_valid
