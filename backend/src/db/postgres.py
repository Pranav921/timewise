import asyncpg

DATABASE_URL = "postgresql://postgres@localhost/testdb"

class Postgres:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        await self.pool.close()

    async def create_tables(self):
        async with database.pool.acquire() as connection:
            await connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    uid TEXT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    username TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS plans (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    owner_uid TEXT REFERENCES users(uid),
                    semester VARCHAR(15) NOT NULL,
                    name TEXT NOT NULL,
                    date DATE NOT NULL DEFAULT CURRENT_DATE
                );

                CREATE TABLE IF NOT EXISTS schedules (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    owner_uid TEXT REFERENCES users(uid),
                    semester VARCHAR(15) NOT NULL,
                    name TEXT NOT NULL,
                    date DATE NOT NULL DEFAULT CURRENT_DATE
                );
            ''')

database = Postgres(DATABASE_URL)