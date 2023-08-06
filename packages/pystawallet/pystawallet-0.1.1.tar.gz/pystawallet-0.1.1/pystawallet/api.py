import logging
from logging import Logger
from uuid import uuid4

import requests

from pystawallet.const import URL_SANDBOX, URL_MAINNET
from pystawallet.exceptions import StawalletHttpException, StawalletUnknownException

INVOICES_URL = "invoices"
DEPOSITS_URL = "deposits"
WITHDRAWS_URL = "withdraws"
QUOTES_URL = "quotes"


class StawalletApiClient:
    def __init__(
            self,
            api_key,
            api_secret,
            is_sandbox=False,
            logger: Logger = None,
            requests_extra_kwargs: dict = None,
            authorization_token=None,
            base_url=None
    ):
        self.server_url = base_url or (URL_SANDBOX if is_sandbox is True else URL_MAINNET)
        self.logger = logger or logging.getLogger('pystawallet')
        self.requests_extra_kwargs = requests_extra_kwargs or {}
        self.api_key = api_key
        self.api_secret = api_secret

    @classmethod
    def _generate_track_id(cls):
        return uuid4().__str__()

    def _generate_authorization_header(self):
        return {
            'X-Api-Key': f'Bearer {self.api_key}',
            'X-Api-Secret': f'Bearer {self.api_secret}'
        }

    def _execute(self, method, url, query_string: dict = None, body: dict = None, headers=None):
        url = '/'.join([self.server_url, url])

        headers = headers or dict()
        self.logger.debug(f"Requesting {method} over {url} with query: {query_string} with body: {body}")

        headers = {**headers, **self._generate_authorization_header()}

        try:
            response = requests.request(
                params=query_string,
                method=method,
                url=url,
                data=body,
                headers=headers,
                **self.requests_extra_kwargs
            )

            print(response.url)
            print(response.text)
            if response.status_code == 200:
                return response.json()

            raise StawalletHttpException(self.logger, response.status_code, response.text)

        except Exception as e:
            raise StawalletUnknownException(self.logger, f"Request error: {str(e)}")

    def get_wallets(self):
        url = ''
        return self._execute('get', url)

    def get_invoice(self, wallet_id, invoice_id):
        url = f'{wallet_id}/{INVOICES_URL}/{invoice_id}'
        return self._execute('get', url)

    def get_invoices(self, wallet_id, user_id):
        url = f'{wallet_id}/{INVOICES_URL}'
        query_string = {'user': user_id}
        return self._execute('get', url, query_string=query_string)

    def post_invoice(self, wallet_id, user_id, force=False):
        url = f'{wallet_id}/{INVOICES_URL}'
        query_string = {'force': force}
        body = {'user': user_id}
        return self._execute('post', url, query_string=query_string, body=body)

    def get_deposits(self, wallet_id, user_id, page=0, asc=None, after=None):
        url = f'{wallet_id}/{DEPOSITS_URL}'
        query_string = {'user': user_id, 'page': page}
        if asc is not None:
            query_string['asc'] = asc
        if after is not None:
            query_string['after'] = after
        return self._execute('get', url, query_string=query_string)

    def get_deposit(self, wallet_id, deposit_id):
        url = f'{wallet_id}/{DEPOSITS_URL}/{deposit_id}'
        return self._execute('get', url)

    def get_withdraws(self, wallet_id, user_id, page=0, after=None):
        url = f'{wallet_id}/{WITHDRAWS_URL}'
        query_string = {'user': user_id, 'page': page}
        if after is not None:
            query_string['after'] = after
        return self._execute('get', url, query_string=query_string)

    def get_withdraw(self, wallet_id, withdraw_id):
        url = f'{wallet_id}/{WITHDRAWS_URL}/{withdraw_id}'
        # query_string = {'user': user_id}
        query_string = {}
        return self._execute('get', url, query_string=query_string)

    def schedule_withdraw(
            self,
            wallet_id,
            user_id,
            business_uid,
            is_manual: bool,
            destination_address,
            destination_tag,
            amount_to_be_withdrawed,
            amount_to_be_withdrawed_plus_fee,
            estimated_network_fee,
            is_decharge=False
    ):
        url = f'{wallet_id}/{WITHDRAWS_URL}'
        body = {
            'user': user_id,
            'businessUid': business_uid,
            'isManual': is_manual,
            'target': destination_address,
            'netAmount': amount_to_be_withdrawed,
            'grossAmount': amount_to_be_withdrawed_plus_fee,
            'estimatedNetworkFee': estimated_network_fee,
            'type': "decharge" if is_decharge else "withdraw",
        }
        if destination_tag is not None:
            body['targetTag'] = destination_tag
        return self._execute('post', url, body=body)

    def edit_withdraw(self, wallet_id, withdraw_id, is_manual: bool):
        url = f'{wallet_id}/{WITHDRAWS_URL}/{withdraw_id}'
        body = {'isManual': is_manual}
        return self._execute('put', url, body=body)

    def resolve_withdraw(self, wallet_id, withdraw_id, final_network_fee, transaction_hash: str):
        url = f'{wallet_id}/{WITHDRAWS_URL}/{withdraw_id}'
        body = {'finalNetworkFee': final_network_fee, 'txid': transaction_hash}
        return self._execute('put', url, body=body)

    def quote_withdraw(self,
                       wallet_id,
                       user_id,
                       business_uid,
                       destination_address,
                       destination_tag,
                       amount,
                       ):
        url = f'{wallet_id}/{QUOTES_URL}/{WITHDRAWS_URL}'
        query_string = {
            'user': user_id,
            'businessUid': business_uid,
            'target': destination_address,
            'amount': amount,
        }
        if destination_tag is not None:
            query_string['targetTag'] = destination_tag
        return self._execute('get', url, query_string=query_string)
