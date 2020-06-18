#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

import requests

from . import domain_limit_local


def cancel_orders_ammo(domain, token, account_guid, contract_symbol, guids):
    if domain == "localhost":
        domain = domain_limit_local

    url = domain + "/client/multi_order"

    querystring = {
        "account_guid": account_guid,
        "contract_symbol": contract_symbol,
        "order_guids": guids
    }
    headers = {
        'Authorization': "Bearer " + token
    }
    payload = json.dumps({}, sort_keys=True)

    req = requests.Request("DELETE", url, headers=headers, params=querystring)
    req_prepared = req.prepare()
    prepare_ammo_request(req_prepared, payload, "a+")


def market_orders_ammo(domain, token, account_guid, contract_symbol, amount):
    buy_orders = orders_wrap(int(amount/2), account_guid, contract_symbol, 0, "SIDE_BUY", "ORDER_MARKET", "EXECINST_NONE")
    sell_orders = orders_wrap(int(amount/2), account_guid, contract_symbol, 0, "SIDE_SELL", "ORDER_MARKET", "EXECINST_NONE")

    payload = {
        "account_guid": account_guid,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)
    req_prepared = orders_put_request_prepare(domain, token, payload)
    return prepare_ammo_request(req_prepared, payload, "a+")


def limit_orders_ammo(domain, token, account_guid, contract_symbol, mark_price, amount):
    # diff = random.uniform(0, 0.03)
    # mark_price = mark_price * (1 + 0.015 - diff)
    min_buy_price = mark_price - mark_price * 0.02
    max_buy_price = mark_price + mark_price * 0.06
    min_sell_price = mark_price - mark_price * 0.06
    max_sell_price = mark_price + mark_price * 0.02

    buy_price = random.uniform(min_buy_price, max_buy_price)
    buy_orders = orders_wrap(amount, account_guid, contract_symbol, round(buy_price), "SIDE_BUY", "ORDER_LIMIT",
                             "EXECINST_NONE")

    sell_price = random.uniform(min_sell_price, max_sell_price)
    sell_orders = orders_wrap(amount, account_guid, contract_symbol, round(sell_price), "SIDE_SELL", "ORDER_LIMIT",
                              "EXECINST_NONE")

    payload = {
        "account_guid": account_guid,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)

    req_prepared = orders_put_request_prepare(domain, token, payload)

    return prepare_ammo_request(req_prepared, payload, "a+")


def limit_sell_orders_ammo(domain, token, account_guid, contract_symbol, mark_price, amount):
    # diff = random.uniform(0, 0.03)
    # mark_price = mark_price * (1 + 0.015 - diff)
    min_sell_price = mark_price - mark_price * 0.001
    max_sell_price = mark_price + mark_price * 0.002

    sell_price = random.uniform(min_sell_price, max_sell_price)
    sell_orders = orders_wrap(amount, account_guid, contract_symbol, round(sell_price), "SIDE_SELL", "ORDER_LIMIT",
                              "EXECINST_NONE")

    payload = {
        "account_guid": account_guid,
        "contract_symbol": contract_symbol,
        "orders": sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)

    req_prepared = orders_put_request_prepare(domain, token, payload)

    return prepare_ammo_request(req_prepared, payload, "a+")


def limit_buy_orders_ammo(domain, token, account_guid, contract_symbol, mark_price, amount):
    # diff = random.uniform(0, 0.03)
    # mark_price = mark_price * (1 + 0.015 - diff)
    min_buy_price = mark_price - mark_price * 0.002
    max_buy_price = mark_price + mark_price * 0.001

    buy_price = random.uniform(min_buy_price, max_buy_price)
    buy_orders = orders_wrap(amount, account_guid, contract_symbol, round(buy_price), "SIDE_BUY", "ORDER_LIMIT",
                             "EXECINST_NONE")

    payload = {
        "account_guid": account_guid,
        "contract_symbol": contract_symbol,
        "orders": buy_orders
    }
    payload = json.dumps(payload, sort_keys=True)

    req_prepared = orders_put_request_prepare(domain, token, payload)

    return prepare_ammo_request(req_prepared, payload, "a+")


def post_orders_ammo(domain, token, account_guid, contract_symbol, mark_price, amount):
    diff = random.uniform(0, 0.03)
    mark_price = mark_price * (1 + 0.015 - diff)
    min_buy_price = mark_price - mark_price * 0.1
    max_buy_price = mark_price + mark_price * 0.05
    min_sell_price = mark_price - mark_price * 0.05
    max_sell_price = mark_price + mark_price * 0.1

    buy_price = random.uniform(min_buy_price, max_buy_price)
    buy_orders = orders_wrap(amount, account_guid, contract_symbol, round(buy_price), "SIDE_BUY", "ORDER_LIMIT",
                             "EXECINST_POST")

    sell_price = random.uniform(min_sell_price, max_sell_price)
    sell_orders = orders_wrap(amount, account_guid, contract_symbol, round(sell_price), "SIDE_SELL", "ORDER_LIMIT",
                              "EXECINST_POST")

    payload = {
        "account_guid": account_guid,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)

    req_prepared = orders_put_request_prepare(domain, token, payload)

    prepare_ammo_request(req_prepared, payload, "a+")


def orders_wrap(amount, account_guid, contract_symbol, price, side, order_type, exec_inst):
    orders = []
    for _ in range(amount):
        quantity = random.randint(1, 5)
        if order_type == "ORDER_MARKET":
            quantity = random.randint(8, 15)
        order = {
            "account_guid": account_guid,
            "contract_symbol": contract_symbol,
            "price": price,
            "side": side,
            "quantity": quantity,
            "order_type": order_type,
            "exec_inst": exec_inst,
            "time_in_force": "ORDERTTL_GTC"
        }
        orders.append(order)
    return orders


def ping_request_prepare(domain, microservice):
    url = domain + "/pub/ping/" + microservice
    headers = {
        'Host': domain.replace("http://", "").replace("https://", "").replace("/v1", ""),
    }
    req = requests.Request(method="GET", url=url, headers=headers)
    req_prepared = req.prepare()
    req = {
        "method": req_prepared.method,
        "path_url": req_prepared.path_url,
        "headers": dict_dump(req_prepared.headers, True)
    }
    req_dump = "{method} {path_url} HTTP/1.1\r\n{headers}\r\n".format(**req)

    return "{req_size}\n{req}\r\n".format(req_size=len(req_dump), req=req_dump)
    # return print_request_and_write_ammo_fille(req_prepared, '', "a+")


def orders_put_request_prepare(domain, token, payload):
    if domain == "localhost":
        domain = domain_limit_local

    url = domain + "/client/multi_order"
    headers = {
        'Authorization': "Bearer " + token,
        'Host': domain.replace("http://", "").replace("https://", "").replace("/v1", ""),
    }
    req = requests.Request("PUT", url, data=payload, headers=headers)

    return req.prepare()


def write_to_file(request, filename, write_type):
    f = open('./' + filename, write_type)
    for index in request:
        f.write(index)
    f.close


def prepare_ammo_request(request, payload, write_type):
    req = {
        "method": request.method,
        "path_url": request.path_url,
        "headers": dict_dump(request.headers, True),
        "body": json.dumps(eval(payload), sort_keys=True)
    }

    print(request.body)

    req_dump = "{method} {path_url} HTTP/1.1\r\n{headers}\r\n{body}".format(**req)

    # write_to_file("{req_size}\n{req}\r\n".format(req_size=len(req_dump), req=req_dump), write_type)
    return "{req_size}\n{req}\r\n".format(req_size=len(req_dump), req=req_dump)


def dict_dump(d, with_newline):
    comma = "\r\n" if with_newline else ""
    dump = ["{0}: {1}{2}".format(k, d[k], comma) for k in sorted(d.keys())]
    return "".join(dump)
