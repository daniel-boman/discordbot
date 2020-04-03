import os

import redis

import local_types

client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

print(client.echo("TESTING 123 123123 "))


def add_role(guild_id, role: local_types.Snowflake) -> int:
    print(f"add: {role.id} | {role.name}")
    try:
        res = client.hset(name=f"guild_roles:{guild_id}", key=role.id, value=role.name)
    except Exception:
        raise
    return res


def remove_role(guild_id, role: local_types.Snowflake) -> int:
    print(f"remove: {role.id} | {role.name}")
    try:
        res = client.hdel(f"guild_roles:{guild_id}", role.id)
    except Exception:
        raise
    return res


def get_roles(guild_id) -> any:
    try:
        res = client.hgetall(name=f"guild_roles:{guild_id}")
    except Exception:
        raise
    return res
