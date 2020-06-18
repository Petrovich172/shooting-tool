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
        * Custom amount of market orders (quantity in range 10 — 20 (you can set it up manualy at flow/ammo_tools_ammo.py:orders_wrap))
        * Custom amount of limit orders (quantity in range 10 — 20 (you can set it up manualy at flow/ammo_tools_ammo.py:orders_wrap))
        * Custom amount of post only limit orders (quantity in range 10 — 20 (you can set it up manualy at flow/ammo_tools_ammo.py:orders_wrap))
            * Orders better than market price
            * Orders worse than market price
        * Cancel 20% of existing limit orders

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
    * flow/ammo_preparation.py
    * `docker ps`, search for custom_tank #CONTAINER ID
    * `docker cp flow/ammo.txt %your_container_id%:/`
    * Gun recharged!