import requests
from sygna_bridge_util.config import (
    SYGNA_BRIDGE_CENTRAL_PUBKEY,
    HTTP_TIMEOUT,
    SYGNA_BRIDGE_CENTRAL_PUBKEY_TEST
)
import sygna_bridge_util.crypto.verify
import json


class API:
    def __init__(self, api_key: str, sygna_bridge_domain: str):
        self.api_key = api_key
        self.domain = sygna_bridge_domain

    def get_sb(self, url: str) -> dict:
        """HTTP GET request to Sygna Bridge

        Args:
            url: str

        Returns:
            dict
        """
        headers = {'x-api-key': self.api_key}
        response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        return response.json()

    def post_sb(self, url: str, body: dict) -> dict:
        """HTTP Post request to Sygna Bridge

        Args:
            url: str
            body: dict

        Returns:
            dict
        """
        headers = {'Content-Type': 'application/json',
                   'x-api-key': self.api_key}
        response = requests.post(
            url,
            data=json.dumps(body),
            headers=headers,
            timeout=HTTP_TIMEOUT)
        return response.json()

    def get_vasp_list(self, validate: bool = True, is_prod: bool = False) -> [dict]:
        """get list of registered VASP associated with public key

         Args:
            validate: bool. decide whether to validate returned vasp list data.
            is_prod: bool. decide which public key to use

         Returns:
            dict{
                vasp_name: str
                vasp_code: str
                vasp_pubkey: str
            }[]

         Raises:
            Exception('Request VASPs failed')
            Exception('get VASP info error: invalid signature')
         """
        url = self.domain + 'v2/bridge/vasp'
        result = self.get_sb(url)
        if 'vasp_data' not in result:
            raise ValueError(
                'Request VASPs failed: {0}'.format(result['message']))

        if not validate:
            return result['vasp_data']

        pubkey = SYGNA_BRIDGE_CENTRAL_PUBKEY if is_prod is True else SYGNA_BRIDGE_CENTRAL_PUBKEY_TEST

        valid = sygna_bridge_util.crypto.verify.verify_data(result, pubkey)

        if not valid:
            raise ValueError('get VASP info error: invalid signature.')

        return result['vasp_data']

    def get_vasp_public_key(self, vasp_code: str, validate: bool = True, is_prod: bool = False) -> str:
        """A Wrapper function of get_vasp_list to return specific VASP's public key.

         Args:
            vasp_code: str
            validate: bool. decide whether to validate returned vasp list data.
            is_prod: bool. decide which public key to use

         Returns:
            str. uncompressed public key

         Raises:
            Exception('Invalid vasp_code')
         """
        vasps = self.get_vasp_list(validate, is_prod)
        target_vasp = None
        for _, item in enumerate(vasps):
            if item['vasp_code'] == vasp_code:
                target_vasp = item
                break

        if target_vasp is None:
            raise ValueError('Invalid vasp_code')

        return target_vasp['vasp_pubkey']

    def get_status(self, transfer_id: str) -> dict:
        """get detail of particular transaction premission request

         Args:
            transfer_id: str

         Returns:
            dict{
                transferData:dict{
                    transfer_id: str
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
                    permission_request_data_signature: str
                    permission_status: str. ACCEPTED or REJECTED
                    permission_signature: str
                    txid: str
                    txid_signature: str
                    created_at: str
                    transfer_to_originator_time: str
                }
                signature: str
            }
         Raises: ValueError
         """
        url = self.domain + 'v2/bridge/transaction/status?transfer_id=' + transfer_id
        return self.get_sb(url)

    def post_permission(self, data: dict) -> dict:
        """Notify Sygna Bridge that you have confirmed specific permission Request from other VASP.
        Should be called by Beneficiary Server

         Args:
            data (dict): {
                transfer_id:str,
                permission_status:str,
                Optional expire_date(int)
                Optional reject_code(str) : BVRC001~7 or BVRC999
                Optional reject_message(str),
                signature:str
            }

         Returns:
            dict{
                status: str
            }
         """
        url = self.domain + 'v2/bridge/transaction/permission'
        return self.post_sb(url, data)

    def post_permission_request(self, data: dict) -> dict:
        """Should be called by Originator.

         Args:
             data: dict{
                data: dict{
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
                callback: dict{
                    callback_url: str
                    signature: str
                }
             }

         Returns:
            dict{
                transfer_id: str
            }
         """
        url = self.domain + 'v2/bridge/transaction/permission-request'
        return self.post_sb(url, data)

    def post_transaction_id(self, data: dict) -> dict:
        """Send broadcasted transaction id to Sygna Bridge for purpose of storage.

         Args:
            data: dict{
                transfer_id: str
                txid: str
                signature: str
            }

         Returns:
            dict{
                status: str
            }
         """
        url = self.domain + 'v2/bridge/transaction/txid'
        return self.post_sb(url, data)

    def post_beneficiary_endpoint_url(self, data: dict) -> dict:
        """This allows VASP to update the Beneficiary's callback URL programmatically.

         Args:
            data: dict{
                vasp_code: str
                Option callback_permission_request_url: str
                Option callback_txid_url: str
                Option callback_validate_addr_url: str
                signature: str
            }

         Returns:
            dict{
                status: str
            }
         """
        url = self.domain + 'v2/bridge/vasp/beneficiary-endpoint-url'
        return self.post_sb(url, data)

    def post_retry(self, data: dict) -> dict:
        """retrieve the lost transfer requests

         Args:
            data: dict{
                vasp_code: str
            }

         Returns:
            dict{
                retryItems: number
            }
         """
        url = self.domain + 'v2/bridge/transaction/retry'
        return self.post_sb(url, data)

    def get_currencies(self, data: dict = {}) -> dict:
        """get supported currencies

         Args:
            data: dict{
                Option currency_id: str
                Option currency_symbol: str
                Option currency_name: str
            }

         Returns:
            dict{
                supported_coins: dict{
                    currency_id: str
                    currency_name: str
                    currency_symbol: str
                    is_active: bool
                    addr_extra_info: str[]
                }[]
            }
         """
        url = self.domain + 'v2/bridge/transaction/currencies'
        query_string = '&'.join([f'{k}={v}' for k, v in data.items()])

        if query_string:
            url = url + '?' + query_string

        return self.get_sb(url)
