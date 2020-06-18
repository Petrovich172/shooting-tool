#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading
import os
import random

from ammo_tools.ammo import write_to_file, ping_request_prepare
from multiprocessing.pool import ThreadPool


def make_ammo(domain):
    # microservices = ["mark", "wrapper", "exmarket", "limit"]
    microservices = ["limit"]
    if os.path.exists("simple_ammo.txt"):
        os.remove("simple_ammo.txt")
    for microservice in microservices:
        for i in range(500):
            req = ping_request_prepare(domain, microservice)
            write_to_file(req, "simple_ammo.txt", "a+")


if __name__ == "__main__":
    # domain = "localhost"
    domain = "https://api.bitboardexchange.com/v1"
    make_ammo(domain)
