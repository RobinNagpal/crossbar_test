# Crossbar test

Requirements:

- Python >= 3.6

## Run

Create a dev db:

Install Pip. Dependency manager.

`(root)$ sudo easy_install pip`

Install virtual environement.

`(root)$ sudo pip install virtualenv`

Create environement.

`(auth)$ virtualenv -p python3 p-env`

`(auth)$ pip3 install --upgrade virtualenv`

Install dependencies.

`(auth)$ pip3 install -r requirements.txt`

Activate virtual enironment.

`(auth)$ source p-env/bin/activate`



Goals
- Have a way for user can authenticate 
- Allow server to route messages to specific client

Good to have
- Use existing JWT token mechanism 
- Try to use Python and angular 5
