# API Vending Machine

<p align="center">
<img src="https://i.ytimg.com/vi/s4_2odXcjUc/hqdefault.jpg" align="right"
     alt="Among us Vending Machine" width="120" height="178">
</p>
API Vending Machine looks to use a functional tested beverage vending machine
for the entire human population.


## How It Works
The behavior is defined by a simple contract that you can check:

1) Insert a coin in the vending machine, returning the amount of accepted coins.
2) Get all the coins back from the vending machine
3) Get the list of the remaining items and their corresponding quantities.
4) Get the remaining quantity in stock for a certain item
5) Buy a certain item from the vending machine returning the amount of coins that
weren’t used and the amount of remaining items of that :id remaining in the
inventory

    a) If there’s no stock for that item the purchase fails and returns the amount of
    coins that have been entered
    
    b) If the funds are insufficient for purchasing an item the purchase fails and
    returns the amount of coins that have been entered 

## Usage

| VERB   | URL            | REQUEST BODY | RESPONSE CODE | RESPONSE HEADERS                                     | RESPONSE BODY         | STATUS      |
|--------|----------------|--------------|---------------|------------------------------------------------------|-----------------------|-------------|
| PUT    | /              | {'coin':1}   | 204           | X-Coins: $accepted                                   |                       | In progress |
| DELETE | /              |              | 204           | X-Coins : $returned                                  |                       | In progress |
| GET    | /inventory     |              | 200           |                                                      | Array of items        | In progress |
| PUT    | /inventory/:id |              | 200           | X-Coins: $remaining X-Inventory-Remaining: $quantity | {'quantity': $vended} | In progress |


### Required Software Installations

Aside from Python, you’ll need:

-The Chrome web browser

-The Git version control system

-A virtualenv with Python 3, Django 2.1, and Selenium 3 in it


1. Install Your Virtualenv:

    ```sh
    # on Windows
    pip install virtualenvwrapper
    # on macOS / Linux
    pip install --user virtualenvwrapper
    # then make Bash load virtualenvwrapper automatically
    echo "source virtualenvwrapper.sh" >> ~/.bashrc
    source ~/.bashrc
    ```

2. Create your virtualenv:

    ```diff
    # on macOS/Linux:
    mkvirtualenv --python=python3.6 vendingmachine
    # on Windows
    mkvirtualenv --python=`py -3.6 -c"import sys; print(sys.executable)"` vendingmachine
    # (a little hack to make sure we get a python 3.6 virtualenv)
    ```
3. Activating and Deactivating your Virtualenv
    Is active if you see: 
    ```sh
        (vendingmachine) $ 
    ```
    if is not, activate it by: 
    ``` sh
     $  workon vendingmachine 
    ```
    to disable it just:
    ```sh
     (vendingmachine) $ deactivate 
    ```
4. Install requirements
        ```sh
            (vendingmachine) $ pip install -r requirements.txt 
         ```
    
### Deployment

manage.py loaddata 