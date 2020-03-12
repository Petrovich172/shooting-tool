#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import random

from . import domain_limit_local


def cancel_orders(domain, token, account_id, contract_symbol, guids):
    if domain == "localhost":
        domain = domain_limit_local

    url = "http://" + domain + "/client/multi_order"

    querystring = {
        "account_id": account_id,
        "contract_symbol": contract_symbol,
        "order_guids": guids
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
    }

    cancel_response = requests.request(
        "DELETE", url, headers=headers, params=querystring)

    jj = cancel_response.json()
    print(
        "cancel_response", jj.get("status", ""), jj.get("code", ""),
        jj.get("orders", {}), jj.get("error", {}).get("detail"))


def prep_market_orders_put(domain, token, account_id, contract_symbol, amount):

    buy_orders = prep_orders_wrap(amount, account_id, contract_symbol, 0, "SIDE_BUY", "ORDER_MARKET", 1)
    sell_orders = prep_orders_wrap(amount, account_id, contract_symbol, 0, "SIDE_SELL", "ORDER_MARKET", 1)

    payload = {
        "account_id": account_id,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)
    registred = orders_put(domain, token, payload)
    guids = []
    for reg in registred:
        guid = reg.get("order_guid", "")
        guids.append(guid)

    return guids


def prep_limit_orders_put(domain, token, account_id, contract_symbol, mark_price, amount):

    buy_orders = prep_orders_wrap(amount, account_id, contract_symbol, mark_price, "SIDE_BUY", "ORDER_LIMIT", 2)
    sell_orders = prep_orders_wrap(amount, account_id, contract_symbol, mark_price, "SIDE_SELL", "ORDER_LIMIT", 2)

    payload = {
        "account_id": account_id,
        "contract_symbol": contract_symbol,
        "orders": buy_orders + sell_orders
    }
    payload = json.dumps(payload, sort_keys=True)
    registred = orders_put(domain, token, payload)
    guids = []
    for reg in registred:
        guid = reg.get("order_guid", "")
        guids.append(guid)

    return guids


def prep_orders_wrap(amount, account_id, contract_symbol, mark_price, side, order_type, exec_inst):
    orders = []
    for _ in range(amount):
        quantity = random.randint(10, 1000)
        price = randomize_price(mark_price, side)
        price = round(price, 2)
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


def orders_put(domain, token, payload):
    if domain == "localhost":
        domain = domain_limit_local

    url = "http://" + domain + "/client/multi_order"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "localhost:8085",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "179",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    order_put_response = requests.request("PUT", url, data=payload, headers=headers)
    jj = order_put_response.json()
    print(
        "order_put_response", jj.get("status", ""), jj.get("code", ""),
        jj.get("orders", {}), jj.get("error", {}).get("detail"))
    registred = jj.get("orders", {})
    return registred


def randomize_price(mark_price, side):
    diff = random.uniform(0, 0.03)
    mark_price = mark_price * (1 + 0.015 - diff)
    price = random.uniform(100, 500)

    if side == "SIDE_BUY":
        min_buy_price = mark_price - mark_price * 0.1
        max_buy_price = mark_price + mark_price * 0.05
        if min_buy_price > 1000:
            rnd_int = random.randint(0, 150)
            price = mark_price + 50 - rnd_int
        else:
            price = random.uniform(min_buy_price, max_buy_price)
        return price
    elif side == "SIDE_SELL":
        min_sell_price = mark_price - mark_price * 0.05
        max_sell_price = mark_price + mark_price * 0.1
        if min_sell_price > 1000:
            rnd_int = random.randint(0, 150)
            price = mark_price - 50 + rnd_int
        else:
            price = random.uniform(min_sell_price, max_sell_price)
        return price
