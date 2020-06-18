#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from multiprocessing.pool import ThreadPool
from sys import argv
from time import sleep

from ammo_tools.client import read_clients_info, write_client_info, market_fill_flow


def prepare_market(domain, contract_symbols):
    new_clients_info = {"full_info": []}
    clients_info = read_clients_info("client_info.json")
    pool = ThreadPool(processes=len(clients_info))
    results = []
    for client in clients_info:
        client_email = client["client"]
        client_accounts = client["accounts"]
        sleep(0.1)
        result = pool.apply_async(market_fill_flow, (domain, client_email, client_accounts, contract_symbols))
        results.append(result)

    pool.close()
    pool.join()
    for res in results:
        updated_client_info = res.get()
        new_clients_info["full_info"].append(updated_client_info)

    write_client_info(new_clients_info)
    print("\n\n*************************\n\nMarket is ready for shooting\n")


if __name__ == "__main__":
    # domain = "localhost"
    domain = "https://api.bitboardexchange.com/v1"
    if len(argv) < 2:
        print ("Set up correct contract_symbols to fill market\nCommand example: 'market_fill.py BTCUSD-M0 BTCUSD-H0'")
        exit(1)
    # contract_symbols = ["BTCUSD-M0"]
    contract_symbols = argv[1:]
    prepare_market(domain, contract_symbols)