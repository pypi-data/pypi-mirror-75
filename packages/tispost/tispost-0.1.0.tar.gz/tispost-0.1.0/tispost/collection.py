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

from aiopg import Connection
from psycopg2.extras import Json


class Collection:

    def __init__(self, connection: Connection, collection: str):
        self.connection = connection
        self.table = collection

    async def save(self, value: dict):
        id = value.pop('id', None)
        async with self.connection.cursor() as cursor:
            if id:
                await cursor.execute(f"UPDATE {self.table} SET data=%s WHERE id=%s", (Json(value), id))
            else:
                await cursor.execute(f"INSERT INTO {self.table} (data) VALUES (%s) RETURNING id", (Json(value),))
                id = (await cursor.fetchone())[0]
            cursor.close()
            value.update(id=id)
            return value

    async def delete(self, id: str):
        async with self.connection.cursor() as cursor:
            await cursor.execute(f"DELETE FROM {self.table} WHERE id=%s", (id,))
            cursor.close()

    async def get(self, id: str) -> dict:
        async with self.connection.cursor() as cursor:
            await cursor.execute(f"SELECT data FROM {self.table} WHERE id=%s", (id,))
            result = await cursor.fetchone()
            cursor.close()
            if result:
                result[0].update(id=id)
                return result[0]
            else:
                return None

    async def query(self, filter: dict, offset=0, limit=50):
        async with self.connection.cursor() as cursor:
            result = list()
            query = f"SELECT id, data FROM {self.table} WHERE data@>%s ORDER BY id LIMIT %s OFFSET %s",
            await cursor.execute(query, (Json(filter), limit, offset))
            async for row in cursor:
                item = row[1]
                item.update(id=row[0])
                result.append(item)
            cursor.close()
            return result
