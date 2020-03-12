#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import requests

from . import domain_limit_local


def cancel_orders_ammo(domain, token, account_id, contract_symbol, guids):
    if domain == "localhost":
        domain = domain_limit_local

    url = "http://" + domain + "/client/multi_order"

    querystring = {
        "account_id": account_id,
        "contract_symbol": contract_symbol,
        "order_guids": guids
    }
    headers = {
        'Authorization': "Bearer " + token,
        'Host': domain
    }
    payload = json.dumps({}, sort_keys=True)

    req = requests.Request("DELETE", url, headers=headers, params=querystring)
    req_prepared = req.prepare()
    print_request_and_write_ammo_fille(req_prepared, payload, "a+")


def market_orders_ammo(domain, token, account_id, contract_symbol, amount):
    buy_orders = orders_wrap(amount, account_id, contract_symbol, 0, "SIDE_BUY", "ORDER_MARKET", 1)
    sell_orders = orders_wrap(amount, account_id, contract_symbol, 0, "SIDE_SELL", "ORDER_MARKET", 1)

    payload = {
        "account_id": account_id,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)
    req_prepared = orders_put_request_prepare(domain, token)
    print_request_and_write_ammo_fille(req_prepared, payload, "a+")


def limit_orders_ammo(domain, token, account_id, contract_symbol, mark_price, amount):
    diff = random.uniform(0, 0.03)
    mark_price = mark_price * (1 + 0.015 - diff)
    min_buy_price = mark_price - mark_price * 0.1
    max_buy_price = mark_price + mark_price * 0.05
    min_sell_price = mark_price - mark_price * 0.05
    max_sell_price = mark_price + mark_price * 0.1

    buy_price = random.uniform(min_buy_price, max_buy_price)
    buy_orders = orders_wrap(amount, account_id, contract_symbol, round(buy_price), "SIDE_BUY", "ORDER_LIMIT", 2)

    sell_price = random.uniform(min_sell_price, max_sell_price)
    sell_orders = orders_wrap(amount, account_id, contract_symbol, round(sell_price), "SIDE_SELL", "ORDER_LIMIT", 2)

    payload = {
        "account_id": account_id,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)

    req_prepared = orders_put_request_prepare(domain, token)

    print_request_and_write_ammo_fille(req_prepared, payload, "a+")


def orders_wrap(amount, account_id, contract_symbol, price, side, order_type, exec_inst):
    orders = []
    for _ in range(amount):
        quantity = random.randint(10, 1000)
        order = {
            "account_id": account_id,
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


def orders_put_request_prepare(domain, token):
    if domain == "localhost":
        domain = domain_limit_local

    url = "http://" + domain + "/client/multi_order"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': domain,
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "179",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    req = requests.Request("PUT", url, headers=headers)

    return req.prepare()


def write_to_file(request, write_type):
    f = open('./ammo.txt', write_type)
    for index in request:
        f.write(index)
    f.close


def print_request_and_write_ammo_fille(request, payload, write_type):
    req = {
        "method": request.method,
        "path_url": request.path_url,
        "headers": dict_dump(request.headers, True),
        "body": json.dumps(eval(payload), sort_keys=True)
    }

    print(request.body)

    req_dump = "{method} {path_url} HTTP/1.1\r\n{headers}\r\n{body}".format(**req)

    write_to_file("{req_size}\n{req}\r\n".format(req_size=len(req_dump), req=req_dump), write_type)
    return "{req_size}\n{req}\r\n".format(req_size=len(req_dump), req=req_dump)


def dict_dump(d, with_newline):
    comma = "\r\n" if with_newline else ""
    dump = ["{0}: {1}{2}".format(k, d[k], comma) for k in sorted(d.keys())]
    return "".join(dump)
