#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import requests
import json

from order import prep_limit_orders_put
from . import domain_wrapper_local, domain_mark_local, domain_limit_local, \
    domain_observer_local, currencies, currency_usd_rate

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def client_flow(domain, email):
    print("\n*******CREATE CLIENT********\n")
    client_create(domain, email)
    print("\n*******LOGIN CLIENT********\n")
    client_token, client_id = client_login(domain, email)

    client_info = {
        "client": email,
        "client_id": client_id,
        "token": client_token,
        "accounts": []
    }

    for currency in currencies:
        print("\n*******CREATE ACCOUNT********\n")
        account_id = account_create(domain, client_token, email, currency)

        print("\n*******PUT DEPOSIT********\n")
        deposit_commit(domain, client_token, client_id, account_id, currency, currency_usd_rate[currency])
        account = {
            "account_id": account_id,
            "account_currency": currency
        }
        client_info["accounts"].append(account)

    return client_info


def market_fill_flow(domain, email, client_accounts, contract_symbols):
    print("\n*******LOGIN CLIENT********\n")
    client_token, client_id = client_login(domain, email)

    client_info = {
        "client": email,
        "client_id": client_id,
        "token": client_token,
        "accounts": []
    }

    for account in client_accounts:
        account_id = account["account_id"]
        currency = account["account_currency"]

        print("\n*******PUT ORDERS********\n")
        for contract_symbol in contract_symbols:
            mark_price = get_mark_price(domain, contract_symbol)
            print("Contract Symbol: ", contract_symbol, "Currency: ", currency)
            registred_guids = prep_limit_orders_put(domain, client_token, account_id, contract_symbol, mark_price, 10)

            account = {
                "account_id": account_id,
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

    url = "http://" + domain + "/pub/invite"
    payload = {
        "email": email,
        "broker": "HFTB"
    }

    payload = json.dumps(payload, sort_keys=True)
    invite_response = requests.request("PUT", url, data=payload, headers="")
    jj = invite_response.json()
    print("client_invite_response", email, jj.get("status", ""), jj.get("code", ""))

    invite_token = ""

    if jj:
        invite_token = jj.get("debug_info", "")

    # Claim invite
    claim_url = "http://" + domain + "/pub/client_claim_invite/" + invite_token
    claim_response = requests.request("PUT", claim_url, data="", headers="")
    jj = claim_response.json()
    print("invite claim_response", email, jj.get("status", ""), jj.get("code", ""))

    claim_access_token = ""

    if jj:
        claim_access_token = jj.get("user", {}).get("access_token", "")

    # New password
    new_pass_url = "http://" + domain + "/user/new_password"
    payload = {
        "password": "123456",
        "totp_code": "111111"
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer: " + claim_access_token,
        'Host': domain
    }

    payload = json.dumps(payload, sort_keys=True)
    new_pass_response = requests.request("POST", new_pass_url, data=payload, headers=headers)
    jj = new_pass_response.json()
    print("new_pass_response", email, jj.get("status", ""), jj.get("code", ""))
    return


def client_login(domain, email):
    if domain == "localhost":
        domain = domain_wrapper_local
    login_url = "http://" + domain + "/pub/client_login"
    payload = {
        "email": email,
        "password": "123456"
    }
    headers = {
        'Content-Type': "application/json",
        'Host': domain
    }

    payload = json.dumps(payload, sort_keys=True)

    login_response = requests.request("POST", login_url, data=payload, headers=headers)
    jj = login_response.json()
    print("login_response", email, jj.get("status", ""), jj.get("code", ""))
    if jj:
        access_token = jj.get("user", {}).get("access_token", "")
        client_id = jj.get("user", {}).get("client", {}).get("id", "")
    return access_token, client_id


def generate_clients_list(amount):
    clients = []
    for i in range(amount):
        clients.insert(i, "tank-n{i}@yandex.ru".format(i=i + 1))
    return clients


def account_create(domain, token, client, currency):
    if domain == "localhost":
        domain = domain_limit_local
    url = "http://" + domain + "/client/account"

    payload = {
        "name": client + currency,
        "description": client + " " + currency + " test account",
        "account_currency": currency,
        "account_type": 1
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token,
    }

    payload = json.dumps(payload, sort_keys=True)

    account_create_response = requests.request("PUT", url, data=payload, headers=headers)
    jj = account_create_response.json()
    print("account_create_response", jj.get("status", ""), jj.get("code", ""), jj.get("account", {}))
    if jj:
        account = jj.get("account", {})
    return account.get("account_id")


def deposit_commit(domain, token, client_id, account_id, currency, score):
    if domain == "localhost":
        domain = domain_observer_local
    url = "http://" + domain + "/oclient/account_wallet_transfer"

    payload = {
        "user_guid": "398858ef-89d3-4ed9-80ef-411be750c1d9",
        "broker": "HFTB",
        "client_id": client_id,
        "account_id": account_id,
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

    payload = json.dumps(payload, sort_keys=True)

    deposit_commit_response = requests.request("PUT", url, data=payload, headers=headers)
    jj = deposit_commit_response.json()
    print("deposit_commit_response", jj.get("status", ""), jj.get("code", ""), jj.get("transfer", {}))

    return


def get_mark_price(domain, contract_symbol):
    if domain == "localhost":
        domain = domain_mark_local
    url = "http://" + domain + "/pub/index_quote/" + contract_symbol + ".M"

    mark_response = requests.request("GET", url)
    jj = mark_response.json()
    print("mark_response", jj.get("status", ""), jj.get("code", ""), jj.get("quote", {}))
    if jj.get("code", "") != 200:
        print("Failed to get mark price. Mark price = 0.3")
        index_quote = 0.3
    else:
        index_quote = jj.get("quote", {}).get("score", "")
    return index_quote


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

