#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# import os, sys
import requests
import json

from . import domain_wrapper_local, domain_mark_local, crosses


def admin_create(domain, super_admin_token, email):
    # Invite
    if domain == "localhost":
        domain = domain_wrapper_local

    url = "http://" + domain + "/admin/invite"
    payload = {
        "email": email,
        "role": "ADMIN",
        "subrole": "ADMIN_ADMIN"
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer: " + super_admin_token
    }

    payload = json.dumps(payload, sort_keys=True)
    invite_response = requests.request("PUT", url, data=payload, headers=headers)
    jj = invite_response.json()
    print("invite_response", jj)

    invite_token = ""

    if jj:
        invite_token = jj.get("debug_info", "")

    # Claim invitte
    print("invite_token", invite_token)
    claim_url = "http://" + domain + "/pub/stuff_claim_invite/" + invite_token
    claim_response = requests.request("PUT", claim_url, data="", headers="")
    jj = claim_response.json()
    print("invite claim_response", jj)

    claim_access_token = ""

    if jj:
        claim_access_token = jj.get("stuff", {}).get("access_token", "")

    # New password
    new_pass_url = "http://" + domain + "/user/new_password"
    payload = {
        "password": "123456",
        "totp_code": "111111"
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer: " + claim_access_token
    }
    payload = json.dumps(payload, sort_keys=True)
    new_pass_response = requests.request("POST", new_pass_url, data=payload, headers=headers)
    jj = new_pass_response.json()
    print("new_pass_response", jj)
    return


def admin_login(domain, email):
    if domain == "localhost":
        domain = domain_wrapper_local

    url = "http://" + domain + "/pub/stuff_login"

    payload = {
        "password": "123456",
        "email": email,
        "role": "ADMIN",
        "totp_code": "111111"
    }
    headers = {
        'Content-Type': "application/json"
    }

    payload = json.dumps(payload, sort_keys=True)
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    jj = response.json()
    print("admin_login response", email, jj.get("status", ""), jj.get("code", ""))

    access_token = ""

    if jj:
        access_token = jj.get("user", {}).get("access_token", "")
    return access_token


def init_dependencies(domain, admin_token):

    reg_currency(domain, admin_token, "BTC", "Bitcoin", "Bitcoin foundation", False, 0.02)
    reg_currency(domain, admin_token, "ETH", "Ethereum", "Ethereum foundation", False, 0.03)
    reg_currency(domain, admin_token, "LTC", "Litecoin", "Litecoin foundation", False, 0.03)
    reg_currency(domain, admin_token, "XRP", "Ripple", "Ripple foundation", False, 0.03)
    reg_currency(domain, admin_token, "USD", "US dollar", "FRS coins", True, 0.03)

    reg_crosses(domain, admin_token)

    for cross in crosses:
        reg_contract_bulk(domain, admin_token, cross)


def reg_currency(domain, token, symbol, name, description, is_fiat, rate):
    if domain == "localhost":
        domain = domain_wrapper_local

    url = "http://" + domain + "/admin/currency"
    payload = {
        "symbol": symbol,
        "name": name,
        "description": description,
        "is_fiat": is_fiat,
        "rate": rate,
        "is_deleted": False,
        "is_deposit": True,
        "is_withdraw": True,
        "is_cross": True,
        "is_account": True,
        "is_contract": True
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer: " + token
    }
    payload = json.dumps(payload, sort_keys=True)
    response = requests.request("PUT", url, data=payload, headers=headers)
    print("reg_currency_response", symbol, response.json())
    return


def reg_crosses(domain, token):
    if domain == "localhost":
        domain = domain_wrapper_local
    url = "http://" + domain + "/admin/cross"

    payloads = [{
        "symbol": "BTCUSD",
        "description": "BTCUSD cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0,
        "source_exindexes": [{
            "exindex_symbol": "BTCUSD.E.BTMP.P"
        },
            {
            "exindex_symbol": "BTCUSD.E.BTMP.P"
        },
            {
            "exindex_symbol": "BTCUSD.E.BTMP.P"
        },
            {
            "exindex_symbol": "BTCUSD.E.KRKN.P"
        }]
    },
        {
        "symbol": "LTCUSD",
        "description": "LTCUSD cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0,
        "source_exindexes": [{
            "exindex_symbol": "LTCUSD.E.BTMP.P"
        },
            {
            "exindex_symbol": "LTCUSD.E.BTMP.P"
        },
            {
            "exindex_symbol": "LTCUSD.E.BTMP.P"
        },
            {
            "exindex_symbol": "LTCUSD.E.GDAX.P"
        }]
    },
        {
        "symbol": "ETHUSD",
        "description": "ETHUSD cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0,
        "source_exindexes": [{
            "exindex_symbol": "ETHUSD.E.KRKN.P"
        },
            {
            "exindex_symbol": "ETHUSD.E.KRKN.P"
        },
            {
            "exindex_symbol": "ETHUSD.E.KRKN.P"
        },
            {
            "exindex_symbol": "ETHUSD.E.BTMP.P"
        }]
    },
        {
        "symbol": "XRPUSD",
        "description": "XRPUSD cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0,
        "source_exindexes": [{
            "exindex_symbol": "XRPUSD.E.KRKN.P"
        },
            {
            "exindex_symbol": "XRPUSD.E.KRKN.P"
        },
            {
            "exindex_symbol": "XRPUSD.E.KRKN.P"
        },
            {
            "exindex_symbol": "XRPUSD.E.BTMP.P"
        }]
    },
        {
        "symbol": "LTCBTC",
        "description": "LTCBTC cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0
    },
        {
        "symbol": "ETHBTC",
        "description": "ETHBTC cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0
    },
        {
        "symbol": "XRPBTC",
        "description": "XRPBTC cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0
    },
        {
        "symbol": "LTCETH",
        "description": "LTCETH cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0
    },
        {
        "symbol": "XRPETH",
        "description": "XRPETH cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0
    },
        {
        "symbol": "XRPLTC",
        "description": "XRPLTC cross",
        "max_leverage": 100,
        "is_futures": True,
        "is_perpetual": True,
        "is_options": True,
        "default_min_move": 0
    }]
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer: " + token,
    }

    for payload in payloads:
        symbol = payload["symbol"]
        payload = json.dumps(payload, sort_keys=True)
        response = requests.request("PUT", url, data=payload, headers=headers)
        print("reg_cross", symbol, response.json())
    return


def reg_contract_bulk(domain, token, cross):
    if domain == "localhost":
        domain = domain_mark_local

    url = "http://" + domain + "/admin/bulk_contract"

    payload = {
        "cross_symbol": cross,
        "futures": {
            "cross_symbol": cross,
            "days_ahead": 93,
            "base_init_margin": "1.0",
            "base_main_margin": "1.0",
            "min_move": "1.0",
            "is_autodeleverage": False
        },
        "options": {
            "cross_symbol": cross,
            "days_ahead": 73,
            "strike_count": 2,
            "base_init_margin": "1.0",
            "base_main_margin": "1.0",
            "min_move": "1.0",
            "is_autodeleverage": False
        },
        "quick_options": {
            "cross_symbol": cross,
            "days_ahead": 43,
            "strike_count": 1,
            "base_init_margin": "1.0",
            "base_main_margin": "1.0",
            "min_move": "1.0",
            "is_autodeleverage": False
        },
        "perpetual": {
            "cross_symbol": cross,
            "base_init_margin": "1.0",
            "base_main_margin": "1.0",
            "min_move": "1.0",
            "is_autodeleverage": False
        }
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer: " + token,
    }
    payload = json.dumps(payload, sort_keys=True)
    response = requests.request("PUT", url, data=payload, headers=headers)
    print("reg_bulk_contracts for cross", cross, response.json())
