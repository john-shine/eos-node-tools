import ast
import json
import requests
import traceback


class Client:

    def __init__(self, rpc_host):
        self.rpc_host = rpc_host

    async def post(self, url, data=None):
        r = requests.post(self.rpc_host + url, data=json.dumps(data), timeout=60)
        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print('unexpected response data: %s' % r.text)

            return False
        except Exception as e:
            traceback.print_exc()

            return False

    async def get_info(self):
        return await self.post('/chain/get_info', {})

    async def get_block(self, block_num_or_id):
        return await self.post('/chain/get_block', {'block_num_or_id': block_num_or_id})

    async def get_block_header_state(self, block_num_or_id):
        return await self.post('/chain/get_block_header_state', {'block_num_or_id': block_num_or_id})

    async def get_account(self, account_name):
        return await self.post('/chain/get_account', {'account_name': account_name})

    async def get_code(self, account_name):
        code = await self.post('/chain/get_code', {'account_name': account_name})
        return code

    async def get_currency_stats(self, code='eosio.token', symbol='EOS'):
        return await self.post('/chain/get_currency_stats', {'code': code, 'symbol': symbol})

    async def get_table_rows(self, scope, code='eosio.token', table='accounts', is_json=True):
        data = {'scope': scope, 'code': code, 'table': table, 'json': is_json}
        return await self.post('/chain/get_table_rows', data)

    async def get_abi(self, account_name):
        return await self.post('/chain/get_abi', {'account_name': account_name})

    async def abi_json_to_bin(self, abi_json, code='eosio.token', action='transfer'):
        abi_json = ast.literal_eval(abi_json)
        data = {'code': code, 'action': action, 'args': abi_json}
        return await self.post('/chain/abi_json_to_bin', data)

    async def abi_bin_to_json(self, binargs, code='eosio.token', action='transfer'):
        data = {'code': code, 'action': action, 'binargs': binargs}
        return await self.post('/chain/abi_bin_to_json', data)

    async def get_raw_abi(self, code):
        return await self.post('/chain/get_raw_abi', {'code': code})

    async def get_required_keys(self, tx):
        return await self.post('/chain/get_required_keys', tx)

    async def get_producers(self, lower_bound, json_, limit):
        data = {
            'lower_bound': lower_bound,
            'json': json_,
            'limit': limit
        }
        return await self.post('/chain/get_producers', data)

    async def get_raw_code_and_abi(self, account_name):
        return await self.post('/chain/get_raw_code_and_abi', {'account_name': account_name})

    async def get_table_by_scope(
            self,
            code,
            table,
            lower_bound=None,
            upper_bound=None,
            limit=10
    ):
        data = {
            'code': code,
            'table': table,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'limit': limit
        }
        return await self.post('/chain/get_table_by_scope', data)

    async def push_transaction(self, packed_context, packed_trx, signatures):
        data = {
            'compression': 'none',
            'packed_context_free_data': packed_context,
            'packed_trx': packed_trx,
            'signatures': signatures
        }
        return await self.post('/chain/push_transaction', data)

    async def get_accounts(self, public_key):
        return await self.post('/history/get_key_accounts', {'public_key': public_key})

    async def get_transaction(self, tx_id):
        data = {
            'id': tx_id
        }
        return await self.post('/history/get_transaction', data)

    async def get_actions(self, account_name, begin=0, limit=10):
        data = {
            'pos': begin,
            'offset': limit - 1,
            'account_name': account_name
        }

        return await self.post('/history/get_actions', data)
