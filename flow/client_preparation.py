#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
from time import sleep
from multiprocessing.pool import ThreadPool
from ammo_tools.client import generate_clients_list, client_flow, write_client_info


def prepare_clients(domain, amount):
    clients = {"full_info": []}
    pool = ThreadPool(processes=10)
    results = []
    for client in generate_clients_list(amount):
        sleep(0.01)
        result = pool.apply_async(client_flow, (domain, client))
        results.append(result)

    pool.close()
    pool.join()
    for res in results:
        client_info = res.get()
        if len(client_info) == 0:
            continue
        clients["full_info"].append(client_info)
        write_client_info(clients)

    print("success")


if __name__ == "__main__":
    # domain = "localhost"
    domain = "https://api.bitboardexchange.com/v1"
    if len(argv) != 2:
        print("Set up correct number of clients\nCommand example: 'python client_preparation.py 5'")
        exit(1)
    prepare_clients(domain, int(argv[1]))
    # prepare_clients(domain, 1)
