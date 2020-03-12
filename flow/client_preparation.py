#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading

from ammo_tools.client import generate_clients_list, client_flow, write_client_info


def prepare_clients(domain, amount):
    # create clients with 5 accounts each, make deposit
    clients = {"full_info": []}
    for client in generate_clients_list(amount):
        client_info = client_flow(domain, client)
        clients["full_info"].append(client_info)

    write_client_info(clients)


if __name__ == "__main__":
    domain = "localhost"
    # domain = "api.bitboardexchange.com"
    prepare_clients(domain, 9)
