#
#    Copyright 2020 Alessio Pinna <alessio.pinna@aiselis.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from tispost.collection import Collection
from aiopg import Pool, Connection


class Session:

    pool: Pool = None
    connection: Connection = None

    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_connection(self):
        if not self.connection:
            self.connection = await self.pool.acquire()
        return self.connection

    async def collection(self, table: str) -> Collection:
        return Collection(await self.get_connection(), table)

    async def create(self, collection: str):
        q = "CREATE TABLE IF NOT EXISTS {}(id UUID NOT NULL DEFAULT uuid_generate_v4(), data JSON, PRIMARY KEY (id))"
        async with (await self.get_connection()).cursor() as cursor:
            await cursor.execute(q.format(collection))
            cursor.close()

    async def delete(self, collection: str):
        q = "DROP TABLE IF EXISTS {}"
        async with (await self.get_connection()).cursor() as cursor:
            await cursor.execute(q.format(collection))
            cursor.close()

    async def close(self):
        if self.connection:
            await self.pool.release(self.connection)
