from src.db.postgres import database

async def insert_friendship(user_id: str, friend_id: str):
    query = """
        INSERT INTO friendships (user_id, friend_id)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING;
    """
    async with database.pool.acquire() as connection:
        await connection.execute(query, user_id, friend_id)

async def list_friendships(user_id: str):
    query = "SELECT friend_id FROM friendships WHERE user_id = $1"
    async with database.pool.acquire() as connection:
        return await connection.fetch(query, user_id)

async def get_user_by_uid(uid: str):
    query = "SELECT uid, email FROM users WHERE uid = $1"
    async with database.pool.acquire() as connection:
        return await connection.fetchrow(query, uid)
