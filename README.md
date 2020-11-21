# API Vending Machine

<p align="center">
<img src="https://i.ytimg.com/vi/s4_2odXcjUc/hqdefault.jpg" align="right"
     alt="Among us Vending Machine" width="120" height="178">
</p>

API Vending Machines  is (Application Programming Interface) for 3rd-party development and integration of new functionalities, customization and any other applications and use cases for virtually unlimited scalability and expandability. API is commited to keep Code Quality Aspects, Reliability, Maintainability, Testability, Portability, Reusability
You can see it working on http://jacuna.pythonanywhere.com/

<p align="left">
     Its fully developed in Python
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/1200px-Python.svg.png" align="right"
     alt="python logo" width="50" height="50">
</p> 

<p align="left">
     Using Django web framework used for rapid development
<img src="https://cosasdedevs.com/media/sections/images/django_rh1DU90.png" align="right"
     alt="django logo" width="50" height="50">
</p>

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
6) Refill: fills the inventory of the vending machine with 3 beverage producuts, 5 units each
## Usage

| VERB   | URL            | REQUEST BODY | RESPONSE CODE | RESPONSE HEADERS                                     | RESPONSE BODY         | STATUS      |
|--------|----------------|--------------|---------------|------------------------------------------------------|-----------------------|-------------|
| GET    | /              |              | 200           |                                                      | Main page html        | :heavy_check_mark: |
| PUT    | /              | {'coin':1}   | 204           | X-Coins: $accepted                                   |                       | :heavy_check_mark: |
| DELETE | /              |              | 204           | X-Coins : $returned                                  |                       | :heavy_check_mark: |
| POST   | /refill        |              | 200           |                                                      |                       | :heavy_check_mark: |
| GET    | /inventory     |              | 200           |                                                      | Array of items        | :heavy_check_mark: |
| PUT    | /inventory/:id |              | 200           | X-Coins: $remaining X-Inventory-Remaining: $quantity | {'quantity': $vended} | :heavy_check_mark: |


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
  ```sh
     git clone  https://github.com/JoaquinAcuna97/vending-machine-.git
     cd vending-machine-
     python manage.py makemigrations
     python manage.py migrate
     python manage.py loaddata
     python manage.py runserver 
```
### Assumptions
There will exist only one global vending machine for the entire human population,
this means that if one user or session, has put 3 coins into a machine, and other
session makes the purchase in the middle, the user will loose their money. 
But, this is similar to real world...

I prefer to put all the test in the tests/ directory, that lives in the project directory to separate them from the code. 

I’ll be using SQLite, a portable database that stores data in a single file by default (www.sqlite.org/index.html).
This is convenient, compared to more complex database systems, because i can start from scratch by deleting the
file if something goes wrong.

### Design
With a focus on optimized software architecture and design,
i think about optimizations in object creation, code structure,
 and interaction between objects at the architecture or design level.
This makes sure that the cost of software maintenance is low, and code can be easily
reused and is adaptable to change.

I try to use the open/close principle, in a case where you have to
create a class implementation, doit by extending the abstract base class to implement the
required behavior instead of changing the abstract class.

I use Singleton design pattern—one of the simplest
and well-known Creational design patterns used in application development,
to be shure that it will be only one instance of vending machines.

For the different kind of machines that can exist, i use a   
Simple Factory pattern: This allows interfaces to create objects without
exposing the object creation logic.


<p align="center">
<img src="https://user-images.githubusercontent.com/61162180/99867321-60432000-2b97-11eb-8cc9-17e252628350.png" align="center"
     alt="models diagram" width="500" height="500">
</p>
