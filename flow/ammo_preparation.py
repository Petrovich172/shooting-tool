#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading
import random
import os

from ammo_tools.client import read_clients_info, get_mark_price, client_login
from ammo_tools.ammo import limit_orders_ammo, market_orders_ammo, cancel_orders_ammo


def ammo_flow(domain):
    clients = read_clients_info("client_info.json")
    if os.path.exists("ammo.txt"):
        os.remove("ammo.txt")
    for client in clients:
        client_name = client["client"]
        client_token, client_id = client_login(domain, client_name)
        for account in client["accounts"]:
            account_id = account["account_id"]
            contract_symbol = account["contract_symbol"]

            registred_guids = account["registred_guids"]
            cancel_len = int(round(len(registred_guids) / 5))
            cancel_guids = random.sample(registred_guids, cancel_len)

            mark_price = get_mark_price(domain, contract_symbol)
            limit_orders_ammo(domain, client_token, account_id, contract_symbol, mark_price, 5)

            market_orders_ammo(domain, client_token, account_id, contract_symbol, 4)

            cancel_orders_ammo(domain, client_token, account_id, contract_symbol, cancel_guids)


if __name__ == "__main__":
    domain = "localhost"
    # domain = "api.bitboardexchange.com"
    ammo_flow(domain)
