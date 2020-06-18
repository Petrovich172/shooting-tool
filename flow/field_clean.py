#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from ammo_tools.db import clean_postgres_limit, clean_redis, clean_postgres_wrapper, \
    clean_postgres_mark, clean_clickhouse


def clean_all_db(domain):
    clean_postgres_limit(domain)
    clean_postgres_wrapper(domain)
    clean_postgres_mark(domain)
    print("\n\n*************************\n\nLimit, Wrapper & Mark DB are cleaned\n")


def clean_all_clickhouse(domain):
    databases = ["mark", "limit"]
    for database in databases:
        clean_clickhouse(domain, database)
    print("\n\n*************************\n\nLimit & Mark ClickHouse are cleaned\n")


def clean_all_redis(domain):
    mark_keys = ["mark:score:*", "mark:last_candle:*"]
    matcher_keys = ["matcher:*"]
    limit_keys = ["limit:*"]
    keys = limit_keys + matcher_keys + mark_keys
    clean_redis(domain, keys)
    print("\n\n*************************\n\nLimit, Matcher & Mark Redis are cleaned\n")


if __name__ == "__main__":
    domain = "localhost"
    clean_all_db(domain)
    clean_all_redis(domain)
    clean_all_clickhouse(domain)
