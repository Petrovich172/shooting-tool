#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from ammo_tools.admin import admin_login, admin_create, init_dependencies


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
    # domain = "https://api.bitboardexchange.com/v1"
    prepare_all_essences(domain, "yandex-tank@yandex.ru")
