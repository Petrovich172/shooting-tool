#!/usr/bin/python
# -*- coding: utf-8 -*-

domain_wrapper_local = "localhost:8081"
domain_mark_local = "localhost:8083"
domain_limit_local = "localhost:8085"
domain_observer_local = "localhost:8090"

currencies = ["BTC", "ETH", "LTC", "XRP", "USD"]
currency_usd_rate = {
    "BTC": 139.196,
    "ETH": 6796,
    "LTC": 21527,
    "XRP": 4550898,
    "USD": 1000000
}

crosses = ["BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "ETHBTC", "LTCBTC", "XRPBTC", "LTCETH",
           "XRPETH", "XRPLTC"]

# contract_suffixes = ["K0", "M0", "N0", "Q0", "U0", "V0", "X0", "Z0", "F1", "G1", "H1",
# "K1", "M1", "N1", "Q1", "U1", "V1", "X1", "Z1", "F2", "G2", "H2", "K2", "M2", "N2",
# "Q2", "U2", "V2", "X2", "Z2", "F3", "G3", "H3"]

# contract_suffixes = ["K0", "M0", "N0", "Q0", "U0", "V0", "X0", "Z0"]