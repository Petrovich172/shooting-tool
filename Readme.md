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
    * Sends post limit orders (custom amount)
    * Price is randomized around mark price (see method `randomize_price`)
    * Quantity is 500 (see method `prep_orders_wrap`)

* 1.4 flow/client_recharge.py
    * Remakes deposit $1M (or equivalent) for each account

* Sample of market preparation flow:
    * Create admin, currencies, cross-pairs, contracts & indexes
        * `python field_preparation.py`
    * Create 100 clients with accounts & deposits
        * `python client_preparation.py 100`
    * Create 4 post limit orders (will create 2 buy & 2 sell orders)
        * `python market_fill.py 4 BTCUSD-M0`

### 	2. Ammo preparation instrument:
* flow/ammo_preparation.py
    * Prepares shooting ammo in flow/ammo.txt
        * Custom amount of market orders (quantity in range 10 — 20 (you can set it up manualy at flow/ammo_tools_ammo.py:orders_wrap))
        * Custom amount of limit orders (quantity in range 10 — 20 (you can set it up manualy at flow/ammo_tools_ammo.py:orders_wrap))
        * Custom amount of post only limit orders (quantity in range 10 — 20 (you can set it up manualy at flow/ammo_tools_ammo.py:orders_wrap))
            * Orders better than market price
            * Orders worse than market price
        * Cancel 20% of existing limit orders

* Sample of ammo preparation use:
    * Create ammo.txt with 20 buy limit, 20 sell limit & 20 market (10 buy & 10 sell) orders in one shot
        * `python ammo_preparation.py 20 20 20`

### 	3. Load testing:
* 3.1 Set up all necessary config
    * Pandora as load generator
        * Shooting config in pandora_config.yaml
        * Pay attention to target option!
        * You can change it manually later, inside container 
    * Yandex-tank config in load.yaml
    * Token from token.txt for http://overload.yandex.net/ connection
    * flow/ammo.txt will be used as ammo file
        
* 3.2. docker build -t custom_tank .
    * Builds docker image with all necessary yandex-tank environment

* 3.3 docker run -it custom_tank
    * Starts load testing with given config options

* 3.4 docker run -it custom_tank bash
    * You can change config inside container
    * yandex-tank -c load.yaml (starts load testing)

* 3.5 You can update ammo.txt file and move it inside container
    * `docker ps`, search for custom_tank #CONTAINER ID
    * `docker cp flow/ammo.txt %your_container_id%:/`
    * Gun recharged!