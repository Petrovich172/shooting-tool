## Prepares market for test and generates ammos for yandex tank
### 	1. Market preparation instruments:
* 1.1 flow/field_preparation.py
   * Creates admin
   * Creates 5 currencies
   * Creates 10 cross-pairs
   * Creates contracts (future, option, perpetual) for each cross-pair
    
* 1.2 flow/client_preparation.py
    * Creates clients (custom amount)
    * Creates 5 accounts (1 currency => 1 account) for each client
    * Makes deposit $1M (or equivalent) for each account
    * Writes all necessary info at flow/client_info.json

* 1.3 flow/market_fill.py
    * Sends 20 (10 buy & 10 sell) Limit orders for each contract with random prices (around mark price). Quantity in range 10 — 1000

* 1.4 flow/client_recharge.py
    * Remakes deposit $1M (or equivalent) for each account

### 	2. Ammo preparation instrument:
* flow/ammo_preparation.py
    * Prepares shooting ammo in flow/ammo.txt
        * Custom amount of market orders (quantity in range 10 — 1000)
        * Custom amount of limit orders (quantity in range 10 — 1000)
            * Orders better than market price
            * Orders worse than market price
        * Cancel 20% of existing limit orders

### 	3. Load testing:
* 3.1. docker build -t custom_tank .
    * Builds docker image with all necessary yandex-tank environment
    * flow/ammo.txt will be used as ammo file
    * Pandora as load generator
    * Shooting config in pandora_config.yaml
    * Yandex-tank config in load.yaml
    * Token from token.txt for http://overload.yandex.net/ connection

* 3.2 docker run -it custom_tank
    * Starts load testing with given config options

* 3.2 docker run -it custom_tank bash
    * You can change config inside container
    * yandex-tank -c load.yaml (starts load testing)
