#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from ammo_tools.admin import admin_login, admin_create, init_dependencies
from ammo_tools.db import clean_postgres_limit, clean_redis, clean_postgres_wrapper, clean_postgres_mark


def clean_all_db(domain):
    clean_postgres_limit(domain)
    clean_postgres_wrapper(domain)
    clean_postgres_mark(domain)
    print("\n\n*************************\n\nLimit, Wrapper & Mark DB are cleaned\n")


def clean_all_redis(domain):
    mark_keys = ["mark:score:*", "mark:last_candle:*"]
    matcher_keys = ["matcher:order:*", "matcher:plan:*", "matcher:glass:*"]
    limit_keys = ["limit:order:*", "limit:account:*", "limit:bundle:*", "limit:portfolio:*", "limit:position:*"]
    keys = limit_keys + matcher_keys + mark_keys
    clean_redis(domain, keys)
    print("\n\n*************************\n\nLimit, Matcher & Mark Redis are cleaned\n")


def prepare_all_essences(domain, admin_email):
    # create admin, all currencies, cross-pairs & contracts for each cross (see flow/admin/reg_contract_bulk)
    super_admin_token = admin_login(domain, 'pete172194177@gmail.com')
    admin_create(domain, super_admin_token, admin_email)
    admin_token = admin_login(domain, admin_email)
    init_dependencies(domain, admin_token)
    print("\n\n*************************\n\nAll essences are ready. Better wait for 2 min\n")
    return admin_token

if __name__ == "__main__":
    domain = "localhost"
    # domain = "api.bitboardexchange.com"
    clean_all_db(domain)
    clean_all_redis(domain)
    prepare_all_essences(domain, "yandex-tank@yandex.ru")