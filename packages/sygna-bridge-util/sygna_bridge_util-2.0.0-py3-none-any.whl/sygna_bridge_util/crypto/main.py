from . import ecies, sign as sygna_sign
import json
from typing import Union
from sygna_bridge_util.validator import (
    validate_private_key
)


def sygna_encrypt_private_data(data: Union[dict, str], public_key: str) -> str:
    """ the method would be deprecated next version, use encrypt_private_data instead """
    return encrypt_private_data(data, public_key)


def encrypt_private_data(data: Union[dict, str], public_key: str) -> str:
    """ Encrypt private info data to hex string.
    Args:
        data: dict or str. private info in data format
        public_key: str. recipient public key in hex string

    Returns:
        str. ECIES encoded private message.
    """
    data_str = data
    if isinstance(data, dict):
        data_str = json.dumps(data)
    return ecies.ecies_encrypt(data_str, public_key)


def sygna_decrypt_private_data(private_message: str, private_key: str) -> Union[dict, str]:
    """ the method would be deprecated next version, use decrypt_private_data instead """
    return decrypt_private_data(private_message, private_key)


def decrypt_private_data(private_message: str, private_key: str) -> Union[dict, str]:
    """ Decrypt private info from recipient server."""
    decode_str = ecies.ecies_decrypt(private_message, private_key)
    try:
        return json.loads(decode_str)
    except ValueError as e:
        return decode_str


def sign_data(data: dict, private_key: str) -> dict:
    """ sign data.
    Args:
        data: dict
        private_key: dict

    Returns:
        dict. original object adding a signature field
    """
    data['signature'] = ''
    signature = sygna_sign.sign_message(data, private_key)
    print(f'sign_data signature ={signature}')
    data['signature'] = signature
    return data


def sign_permission_request(data: dict, private_key: str) -> dict:
    """ sign permission request data

    Args:
        data :dict{
            private_info: str,
            transaction: dict{
                originator_vasp: dict{
                    vasp_code: str
                    addrs:dict[]{
                        address: str
                        Optional addr_extra_info: dict[]
                    }
                },
                beneficiary_vasp: dict{
                    vasp_code: str
                    addrs:dict[]{
                        address: str
                        Optional addr_extra_info: dict[]
                    }
                }
                currency_id: str
                amount: str
            }
            data_dt: str
            Optional expire_date: int
            Optional need_validate_addr: bool
        }
        private_key: str

    Returns:
        dict{
            private_info: str
            transaction: dict{
                originator_vasp: dict{
                    vasp_code: str
                    addrs:dict[]{
                        address: str
                        Optional addr_extra_info: dict[]
                    }
                },
                beneficiary_vasp: dict{
                    vasp_code: str
                    addrs:dict[]{
                        address: str
                        Optional addr_extra_info: dict[]
                    }
                }
                currency_id: str
                amount: str
            }
            data_dt: str
            Optional expire_date: int
            Optional need_validate_addr: bool
            signature: str
        }
    """
    validate_private_key(private_key)
    return sign_data(data, private_key)


def sign_callback(data: dict, private_key: str) -> dict:
    """ sign callback data

    Args:
        data: dict{
            callback_url: str
        }
        private_key: str

    Returns:
        dict{
            callback_url: str,
            signature: str
        }
    """
    validate_private_key(private_key)
    return sign_data(data, private_key)


def sign_permission(data: dict, private_key: str) -> dict:
    """ sign permission data

    Args:
        data: dict{
            transfer_id: str,
            permission_status: str (ACCEPTED or REJECTED),
            Optional expire_date: int,
            Optional reject_code: str (BVRC001~007 or BVRC999),
            Optional reject_message: str
        }
        private_key: str

    Returns:
        dict{
            transfer_id: str,
            permission_status: str,
            Optional expire_date: int,
            Optional reject_code: str
            Optional reject_message: str,
            signature: str
        }
    """
    validate_private_key(private_key)
    return sign_data(data, private_key)


def sign_transaction_id(data: dict, private_key: str) -> dict:
    """ sign transaction id data

    Args:
        data: dict{
            transfer_id: str
            txid: str
        }
        private_key: str

    Returns:
        dict{
            transfer_id: str
            txid: str,
            signature: str
        }
    """
    validate_private_key(private_key)
    return sign_data(data, private_key)


def sign_beneficiary_endpoint_url(data: dict, private_key: str) -> dict:
    """ sign sign_beneficiary_endpoint_url data

    Args:
        data: dict{
            vasp_code: str
            Option callback_permission_request_url: str
            Option callback_txid_url: str
            Option callback_validate_ddr_url: str
        }
        private_key: str

    Returns:
        dict{
            vasp_code: str
            Option callback_permission_request_url: str
            Option callback_txid_url: str
            signature: str
        }
    """
    validate_private_key(private_key)
    return sign_data(data, private_key)
