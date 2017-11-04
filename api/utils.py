import requests
import json

base_url = 'https://3hkaob4gkc.execute-api.us-east-1.amazonaws.com/prod/au-hackathon/'

# get all accounts ids
# account_id: int
def get_all_accounts():
	option = 'accounts'
	info = requests.post(base_url + option)
	return info.json()

# get all customer ids
# customer_id: int
def get_all_ids():
	option = 'accounts'
	info = requests.post(base_url + option)
	return info.json()

# -----below are five read APIs-----

# get account info (ex: account_id = 100700000)
# account_id: int
def get_account_info(account_id):
    option = 'accounts'
    body = {"account_id": account_id}
    info = requests.post(base_url + option, data=json.dumps(body))
    return info.json()

def get_account_info(account_id):
    print("working")
    print(account_id)
    option = 'accounts'
    body = {"account_id": account_id}
    info = requests.post(base_url + option, data=json.dumps(body))
    print(info)
    return info.json()

# get customer info (ex: customer_id = 100720000)
# customer_id: int
def get_customer_info(customer_id):
	option = 'customers'
	body = {"customer_id": customer_id}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info.json()

# get transaction info (ex: account_id = 100700000)
# account_id: int
def get_transaction_info(account_id):
    option = 'transactions'
    body = {"account_id": account_id}
    info = requests.post(base_url + option, data=json.dumps(body))
    return info.json()

# get rewards info (ex: account_id = 100700000)
# account_id: int
def get_rewards_info(account_id):
	option = 'rewards'
	body = {"account_id": account_id}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info.json()

# get payment info (ex: account_id = 100700000)
# account_id: int
def get_payment_info(account_id):
	option = 'payments'
	body = {"account_id": account_id}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info.json()

# -----below are three write APIs-----

# add new account
# team_name: str
def add_new_account(team_name):
	option = 'add-account'
	body = {"team_name": team_name}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info.json()

# add new authorized user
# team_name: str
# account_id: int
def add_new_au(team_name, account_id):
	option = 'add-au'
	body = {"team_name": team_name,
	"account_id": account_id}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info.json()

# update customer
# team_name: str
# customer_id: int
# first_name: str
# last_name: str
# address: str
# city: str
# state: str
# zipcode: str
# is_married: bool
# phone_number: str
# email: str
def update_customer(team_name, customer_id, 
first_name=None, last_name=None, address=None, city=None, state=None,
zipcode=None, is_married=None, phone_number=None, email=None):
	option = 'update-customer'
	body = {"team_name" : team_name,
	"customer_id" : customer_id,
	"first_name" : first_name,
	"last_name" : last_name,
	"address" : address,
	"city" : city,
	"state" : state,
	"zipcode" : zipcode,
	"is_married" : is_married,
	"phone_number" : phone_number,
	"email" : email}
	info = requests.post(base_url+option, data=json.dumps(body))
	return info.json()