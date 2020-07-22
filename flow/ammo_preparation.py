#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading
import os
import random

from sys import argv
from time import sleep
from ammo_tools.ammo import limit_buy_orders_ammo, limit_sell_orders_ammo, market_orders_ammo, cancel_orders_ammo, write_to_file
from ammo_tools.client import read_clients_info, get_mark_price, client_login
from multiprocessing.pool import ThreadPool


def make_ammo(domain):
    clients_info = read_clients_info("client_info.json")
    pool = ThreadPool(processes=10)
    results = []
    if os.path.exists("ammo.txt"):
        os.remove("ammo.txt")
    for client in clients_info:
        sleep(0.1)
        result = pool.apply_async(ammo_flow, (domain, client))
        results.append(result)

    pool.close()
    pool.join()
    flat_results = []
    _ = [flat_results.extend(item) if isinstance(item, list) else flat_results.append(item) for item in results if item]
    for res in flat_results:
        req = res.get()
        write_to_file(req, "ammo.txt", "a+")


def ammo_flow(domain, client):
    client_name = client["client"]
    client_token, client_id = client_login(domain, client_name)
    reqs = []
    accounts = client["accounts"]
    random.shuffle(accounts)
    for account in accounts:
        account_guid = account["account_guid"]
        contract_symbol = account["contract_symbol"]

        registred_guids = account["registred_guids"]
        cancel_len = int(round(len(registred_guids) / 5))
        cancel_guids = random.sample(registred_guids, cancel_len)

        mark_price = get_mark_price(domain, contract_symbol)

        req = limit_buy_orders_ammo(domain, client_token, account_guid, contract_symbol, mark_price, int(argv[1]))
        # req = limit_buy_orders_ammo(domain, client_token, account_guid, contract_symbol, mark_price, 10)
        reqs.append(req)
        req = limit_sell_orders_ammo(domain, client_token, account_guid, contract_symbol, mark_price, int(argv[2]))
        # req = limit_sell_orders_ammo(domain, client_token, account_guid, contract_symbol, mark_price, 10)
        reqs.append(req)
        # req = post_orders_ammo(domain, client_token, account_guid, contract_symbol, mark_price, 10)
        # reqs.append(req)
        req = market_orders_ammo(domain, client_token, account_guid, contract_symbol, int(argv[3]))
        # req = market_orders_ammo(domain, client_token, account_guid, contract_symbol, 10)
        reqs.append(req)
        # req = cancel_orders_ammo(domain, client_token, account_guid, contract_symbol, cancel_guids)
        # reqs.append(req)
    return reqs


if __name__ == "__main__":
    # domain = "localhost"
    domain = "https://api.bitboardexchange.com/v1"
    if len(argv) < 4:
        print("Set up correct number of limit_buy, limit_sell & market orders\nExample: ")
        exit(1)
    make_ammo(domain)
