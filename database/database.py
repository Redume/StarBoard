import json

import asyncpg
import yaml

config = yaml.safe_load(open("config.yaml", "r"))

async def pg_con():
    try:
        con = await asyncpg.connect(
            user=config['database']["user"],
            password=config['database']["password"],
            database=config['database']["database"],
            host=config['database']["host"],
            port=5432
        )

        await con.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )

        return con
    except Exception as e:
        print(e)