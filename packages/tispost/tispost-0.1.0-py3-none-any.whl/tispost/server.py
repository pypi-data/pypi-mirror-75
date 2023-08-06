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

from tispost.session import Session
from aiopg import Pool
import aiopg


class Server:

    pool: Pool = None
    dns: str = None

    def __init__(self, **kwargs):
        self.dsn = ' '.join(['{}={}'.format(k, v) for k, v in kwargs.items()])

    async def connect(self):
        self.pool = await aiopg.create_pool(self.dsn)

    async def close(self):
        if self.pool:
            self.pool.close()

    async def session(self) -> Session:
        return Session(self.pool)
