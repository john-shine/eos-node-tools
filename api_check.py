import asyncio
import sqlite3
import inspect
from time import time
from settings.database import db_name
from eos_rpc.client import Client
from settings.servers import servers
from models.health_statistics import HealthStatistics


class APICheck:

    async def run(self, server):
        print('server: ', server)
        self.client = Client(server)

        db_conn = sqlite3.connect(db_name)
        db_conn.set_trace_callback(print)

        health_statistics = HealthStatistics(db_conn)

        attrs = inspect.getmembers(self, predicate=inspect.ismethod)
        for attr in attrs:
            fname, fmethod = attr
            if 'check_' in fname:
                before = time()
                result = await fmethod()
                after = time()
                consumed = int((after - before) * 1000)
                if result:
                    print(fname + ' check result: True')
                    health_statistics.insert_health(server, fname, consumed, 1)
                else:
                    print(fname + ' check result: False')
                    health_statistics.insert_health(server, fname, consumed, 0)
                
                print('time consumed: ' + str(consumed))

    async def check_get_account(self):
        account = await self.client.get_account('fepxecwzm41t')
        try:
            assert account['account_name'] == 'fepxecwzm41t'
        except Exception as e:
            return False

        return True

    async def check_get_block(self):
        try:
            block = await self.client.get_block(63240199)
            assert block['previous'] == \
                '03c4f8065ac064a9ad3dd83c77e06cab17eb153701c91b03992b9463422df35c'
        except Exception as e:
            return False

        return True

    async def check_get_info(self):
        try:
            info = await self.client.get_info()
            assert info['server_version'] != ''
        except Exception as e:
            return False

        return True

    async def check_get_abi(self):
        try:
            abi = await self.client.get_abi('fepxecwzm41t')
            assert abi['account_name'] == 'fepxecwzm41t'
        except Exception as e:
            return False

        return True

    async def check_get_accounts(self):
        try:
            accounts = await self.client.get_accounts('EOS6TA4GyfDF51A4Qz4F6TZMd2Z78hLXp6p2PnyH2kY98ZyTh2vnt')
            assert 'fepxecwzm41t' in accounts['account_names']
        except Exception as e:
            return False

        return True

    async def check_get_transaction(self):
        try:
            transaction = await self.client.get_transaction('c3d986a334164a2c71355169b7ebbbd70869a5645e902b1a5d75eec309d40a73')
            assert transaction['id'] == 'c3d986a334164a2c71355169b7ebbbd70869a5645e902b1a5d75eec309d40a73'
        except Exception as e:
            return False

        return True


if __name__ == '__main__':

    async def main():
        health_check = APICheck()
        for server in servers:
            await health_check.run(server)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())

    loop.close()
