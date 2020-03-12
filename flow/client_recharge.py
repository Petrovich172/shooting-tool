#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from ammo_tools.client import read_clients_info, deposit_commit
from ammo_tools import currency_usd_rate


def recharge_clients(domain):
    clients_info = read_clients_info("client_info.json")
    for client in clients_info:
        client_token = client["token"]
        client_id = client["client_id"]
        for account in client["accounts"]:
            account_id = account["account_id"]
            currency = account["account_currency"]
            deposit_commit(domain, client_token, client_id, account_id, currency, currency_usd_rate[currency])


if __name__ == "__main__":
    domain = "localhost"
    # domain = "api.bitboardexchange.com"
    recharge_clients(domain)
