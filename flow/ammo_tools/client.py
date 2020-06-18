#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import json
from time import sleep

import requests

from order import prep_limit_orders_put
from . import domain_wrapper_local, domain_mark_local, domain_limit_local, \
    domain_observer_local, currencies, currency_usd_rate

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def client_flow(domain, email):
    client_create(domain, email)
    client_token, client_id = client_login(domain, email)
    if client_token is None:
        return {}

    client_info = {
        "client": email,
        "client_id": client_id,
        "token": client_token,
        "accounts": []
    }

    for currency in currencies:
        for num in range(1):
            account_guid = account_create(domain, client_token, email, currency, num)
            if account_guid is None:
                continue
            deposit_resp = deposit_commit(domain, client_token, client_id, account_guid, currency,
                                          currency_usd_rate[currency])
            if deposit_resp is None:
                continue
            account = {
                "account_guid": account_guid,
                "account_currency": currency
            }
            client_info["accounts"].append(account)

    return client_info


def market_fill_flow(domain, email, client_accounts, contract_symbols):
    # print("\n*******LOGIN CLIENT********\n")
    client_token, client_id = client_login(domain, email)
    if client_token is None:
        return {}

    client_info = {
        "client": email,
        "client_id": client_id,
        "token": client_token,
        "accounts": []
    }

    for account in client_accounts:
        account_guid = account["account_guid"]
        currency = account["account_currency"]

        # print("\n*******PUT ORDERS********\n")
        for contract_symbol in contract_symbols:
            mark_price = get_mark_price(domain, contract_symbol)
            print("Contract Symbol: ", contract_symbol, "Currency: ", currency)
            registred_guids = prep_limit_orders_put(domain, client_token, account_guid, contract_symbol, mark_price, 2)

            account = {
                "account_guid": account_guid,
                "account_currency": currency,
                "contract_symbol": contract_symbol,
                "registred_guids": registred_guids
            }
            client_info["accounts"].append(account)

    return client_info


def client_create(domain, email):
    # Invite
    if domain == "localhost":
        domain = domain_wrapper_local

    url = domain + "/pub/invite"
    payload = {
        "email": email,
        "broker": "HFTB"
    }

    payload = json.dumps(payload, sort_keys=True)
    invite_response = requests.request("PUT", url, data=payload, headers="")

    if not invite_response.ok:
        if invite_response.status_code == 409:
            return
        else:
            print("Unexpected invite_response: ", email, invite_response)
            return

    jj = invite_response.json()
    invite_token = jj.get("debug_info", "")

    # Claim invite
    claim_url = domain + "/pub/client_claim_invite/" + invite_token
    claim_response = requests.request("PUT", claim_url, data="", headers="")

    if not claim_response.ok:
        print("Unexpected invite claim_response: ", email, claim_response)
        return

    jj = claim_response.json()
    claim_access_token = jj.get("user", {}).get("access_token", "")

    sleep(0.1)
    # New password
    new_pass_url = domain + "/user/new_password"
    payload = {
        "password": "123456",
        "repeat_password": "123456"
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + claim_access_token,
    }

    payload = json.dumps(payload, sort_keys=True)
    new_pass_response = requests.request("POST", new_pass_url, data=payload, headers=headers)
    if not new_pass_response.ok:
        print("Unexpected new_pass_response: ", email, new_pass_response)

    return


def client_login(domain, email):
    if domain == "localhost":
        domain = domain_wrapper_local
    login_url = domain + "/pub/client_login"
    payload = {
        "email": email,
        "password": "123456"
    }

    payload = json.dumps(payload, sort_keys=True)

    login_response = requests.request("POST", login_url, data=payload)
    if login_response.ok:
        jj = login_response.json()
        if jj.get("code", "") != 200:
            print(email, jj.get("status", ""), jj.get("code", ""))
            return None, None
        access_token = jj.get("user", {}).get("access_token", "")
        client_id = jj.get("user", {}).get("client", {}).get("id", "")
        print(email, "log in successfully")
        return access_token, client_id
    else:
        print("Unexpected client_login response: {resp}".format(resp=login_response))


def generate_clients_list(amount):
    clients = []
    for i in range(amount):
        clients.insert(i, "n%03d@yandex.ru" % (i + 1))
    return clients


def account_create(domain, token, client, currency, num):
    if domain == "localhost":
        domain = domain_limit_local
    url = domain + "/client/account"

    payload = {
        "name": client + currency + str(num),
        "description": client + " " + currency + " test account",
        "account_currency": currency,
        "account_type": "ACCOUNT_CLIENT"
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
    }

    payload = json.dumps(payload, sort_keys=True)

    try:
        account_create_response = requests.request("PUT", url, data=payload, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
        return None
    if not account_create_response.ok:
        print("Unexpected account_create response for client + currency: {resp}".format(resp=account_create_response))
        return None

    jj = account_create_response.json()
    account = jj.get("account", {})
    print(account.get("name"), "created")
    return account.get("account_guid")


def deposit_commit(domain, token, client_id, account_guid, currency, score):
    if domain == "localhost":
        domain = domain_observer_local
    url = domain + "/oclient/account_wallet_transfer"

    payload = {
        "user_guid": "398858ef-89d3-4ed9-80ef-411be750c1d9",
        "broker": "HFTB",
        "client_id": client_id,
        "account_guid": account_guid,
        "currency_symbol": currency,
        "client_wallet_id": 1,
        "is_account_direction": True,
        "score": score,
        "status": 1
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
    }

    try:
        deposit_commit_response = requests.request("PUT", url, json=payload, headers=headers)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
        return None
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
        return None
    if not deposit_commit_response.ok:
        print("Unexpected deposit_commit response: {resp}".format(resp=deposit_commit_response))
        return None

    print("deposit committed for account_guid", payload["account_guid"])

    return ""


def get_mark_price(domain, contract_symbol):
    if domain == "localhost":
        domain = domain_mark_local
    url = domain + "/pub/index_quote/" + contract_symbol + ".M"

    mark_response = requests.request("GET", url)
    if mark_response.ok:
        jj = mark_response.json()
        print("mark_response", jj.get("status", ""), jj.get("code", ""), jj.get("quote", {}))
        if jj.get("code", "") != 200:
            print("Failed to get mark price. Mark price = 0.3")
            index_quote = 0.3
        else:
            index_quote = jj.get("quote", {}).get("score", "")
        return index_quote
    else:
        print("Unexpected get_mark_price response: {resp}".format(resp=mark_response))
        print("Failed to get mark price. Mark price = 0.3")
        return 0.3


# Write JSON file with all clients necessary info
def write_client_info(clients):
    data = json.dumps(clients, sort_keys=True)
    with io.open('client_info.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))


# Read JSON file with all clients necessary info
def read_clients_info(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        data = json.loads(data)
        data = data["full_info"]
    return data
