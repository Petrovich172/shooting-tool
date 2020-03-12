#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from ammo_tools.client import read_clients_info, write_client_info, market_fill_flow


def prepare_market(domain, contract_symbols):
    new_clients_info = {"full_info": []}
    clients_info = read_clients_info("client_info.json")
    for client in clients_info:
        client_email = client["client"]
        client_accounts = client["accounts"]
        updated_client_info = market_fill_flow(domain, client_email, client_accounts, contract_symbols)
        new_clients_info["full_info"].append(updated_client_info)

    write_client_info(new_clients_info)
    print("\n\n*************************\n\nMarket is ready for shooting\n")


if __name__ == "__main__":
    domain = "localhost"
    # domain = "api.bitboardexchange.com"
    contract_symbols = ["BTCUSD-H0"]
    prepare_market(domain, contract_symbols)
