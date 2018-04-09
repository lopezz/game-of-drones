# game-of-drones
A rock-paper-scissors game written in Django and ReactJS

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [ReactJS](https://reactjs.org/): A JavaScript library for building user interfaces

## Requirements
* Python 3.5+

## Installation
* In order to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python [here](https://www.python.org).
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```bash
        $ python -m pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/lopezz/game-of-drones.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd game-of-drones
        ```
    2. Create and activate your virtual enviroment:
        ```bash
            $ python -m venv venv
            $ source venv/bin/activate
        ```
        If you are on Windows, you can achieve this using.
        ```bash            
            $ venv\Scripts\activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```
    5. Collect static files
        ```bash            
            $ python manage.py collectstatic --noinput
        ```

* #### Run It
    Start the server using this command:
    ```bash
        $ python manage.py runserver
    ```
    You can now access the game in your browser using
    ```
        http://localhost:8000
    ```
