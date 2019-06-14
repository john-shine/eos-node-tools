import sqlite3
import asyncio
from time import time
from eos_rpc.client import Client
from settings.servers import servers
from settings.database import db_name
from models.height_statistics import HeightStatistics


class HeightCheck:

    def __init__(self):
        pass

    async def task(self, server):
        print('server: %s' % server)
        client = Client(server)
        info = None
        try:
            info = await client.get_info()
        except Exception as e:
            print(e)

        height = info.get('head_block_num', 0) if info else 0
        return server, height

    async def run(self):
        db_conn = sqlite3.connect(db_name)
        db_conn.set_trace_callback(print)

        hs = HeightStatistics(db_conn)
        insert_id = hs.get_last_id() + 1
        timestamp = time()

        tasks = []
        for server in servers:
            task = self.task(server)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        for response in responses:
            server, height = response
            hs.insert_or_update_height(insert_id, server, height, timestamp)
            print(response)

        print('cycle: %s height check finished.' % insert_id)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(HeightCheck().run())
    loop.close()
