#!/usr/bin/python
# -*- coding: latin-1 -*-

import psycopg2
import redis
from clickhouse_driver import Client


def clean_clickhouse(domain, database):
    client = Client(host=domain)
    tables = client.execute("SELECT name FROM system.tables WHERE database = %(db)s",
                            {"db": database}
                            )
    for table in tables:
        table_name = table[0].encode("utf-8")
        if table_name == "schema_migrations":
            continue
        else:
            table_name = database + "." + table_name
            client.execute("TRUNCATE TABLE {table_name}".format(table_name=table_name))


def clean_redis(domain, prefixes):
    r = redis.Redis(host=domain, port=6379, db=0)
    pipe = r.pipeline()

    for prefix in prefixes:
        mid_results = []
        cursor, results = r.scan(0, prefix, 1000)
        mid_results += results
        while cursor != 0:
            cursor, results = r.scan(cursor, prefix, 1000)
            mid_results += results

        for order in mid_results:
            pipe.delete(order)

    pipe.execute()


def clean_postgres_limit(domain):
    conn = psycopg2.connect(dbname="limit", user="limit", password="limit", host=domain)
    cursor = conn.cursor()
    cursor.execute(
        "truncate public.order, public.account, public.portfolio, public.account_action, public.wtransfer cascade;")
    conn.commit()
    conn.close()


def clean_accounts_for_client(domain, client_id):
    client = Client(host=domain)
    client.execute(
        "ALTER TABLE limit.account DELETE WHERE user_id = toUInt64(%(client_id)s)", {"client_id": client_id})


def clean_postgres_mark(domain):
    conn = psycopg2.connect(dbname="mark", user="mark", password="mark", host=domain)
    cursor = conn.cursor()
    cursor.execute("truncate public.contract, public.index cascade;")
    conn.commit()
    conn.close()


def clean_postgres_wrapper(domain):
    conn = psycopg2.connect(dbname="wrapper", user="wrapper", password="wrapper", host=domain)
    cursor = conn.cursor()
    cursor.execute(
        "truncate public.cross_pair, public.currency, public.client cascade;"
    )
    conn.commit()
    conn.close()
