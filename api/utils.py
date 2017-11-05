import requests
import json

base_url = 'https://3hkaob4gkc.execute-api.us-east-1.amazonaws.com/prod/au-hackathon/'

# get all account id
# account_id: int
# customer_id: int
def get_all_accounts():
	option = 'accounts'
	info = requests.post(base_url + option)
	return info

# get all customer ids and their belonged account id
# account_id: int
# customer_id: int
def get_all_customers():
	option = 'customers'
	info = requests.post(base_url + option)
	return info
 
# -----below are five read APIs-----

''' get account info (ex: account_id = 100700000)
if all missing, return all account ids

request{
account_id: int
card_type: str
team_name: str}

response{
account_id: int
primary_user: int (id)
primary_user_card_number: str
authorized_users: [{customer_id, credit_card_number},...]
credit_limit: int
balance: int
card_type: str
card_number: str
total_rewards_earned: int
total_rewards_used: int}
'''
def get_account_info(account_id=None, card_type=None, team_name=None):
	option = 'accounts'
	body = {}
	if account_id:
		account_id = int(account_id)
		body["account_id"] = account_id
	if card_type:
		card_type = str(card_type)
		body["card_type"] = card_type
	if team_name:
		team_name = str(team_name)
		body["team_name"] = team_name
	info = requests.post(base_url + option, data=json.dumps(body))
	return info

''' get customer info (ex: customer_id = 100720000)
if all missing, return all customer ids and account ids

request{
gender: str (Male or Female)
customer_zipcode: str
customer_id: int
card_number: str
is_married: bool}

response{
account_id: int
customers: [
{customer_id: int
first_name: str
last_name: str
dob: str (format mm/dd/yyyy)
gender: str (Male or Female)
country: str
zipcode: str
credit_card_number: str
is_primary: bool
is_married: bool
email: str}, ... ]}
'''
def get_customer_info(gender=None, customer_zipcode=None,
	customer_id=None, card_number=None, is_married=None):
	option = 'customers'
	body = {}
	if gender:
		gender = str(gender)
		body["gender"] = gender
	if customer_zipcode:
		customer_zipcode = str(customer_zipcode)
		body["customer_zipcode"] = customer_zipcode
	if customer_id:
		customer_id = int(customer_id)
		body["customer_id"] = customer_id
	if card_number:
		card_number = str(card_number)
		body["card_number"] = card_number
	if is_married:
		is_married = bool(is_married)
		body["is_married"] = is_married
	info = requests.post(base_url + option, data=json.dumps(body))
	return info

''' get transaction info (ex: account_id = 100700000)
must have at least one of account_id, customer_id, transaction_id, card_number

request{
date_from: str (format mm/dd/yyyy)
date_to: str (format mm/dd/yyyy)
min_amount: int
max_amount: int
card_number :str
account_id: int
customer_id: int
merchant_name: str
card_type: str
transaction_zipcode: str
transaction_id: int}

response{ check github for details
account_id: integer
customers: [
	{
		customer_id: int
		transactions: [
			{
				transaction_row_id: 1, (index)
				zipcode: str,
				month: str,
				rewards_earned: float,
				amount: float,
				year: int,
				country: str,
				day: int,
				transaction_id: int,
				merchant_name: str
			},
			...
		]
	},
	...
]}
'''
def get_transaction_info(date_from=None, date_to=None, 
	min_amount=None, max_amount=None, card_number=None,
	account_id=None, customer_id=None, merchant_name=None,
	card_type=None, transaction_zipcode=None, transaction_id=None):
	option = 'transactions'
	body = {}
	if date_from:
		date_from = str(date_from)
		body["date_from"] = date_from
	if date_to:
		date_to = str(date_to)
		body["date_to"] = date_to
	if min_amount:
		min_amount = int(min_amount)
		body["min_amount"] = min_amount
	if max_amount:
		max_amount = int(max_amount)
		body["max_amount"] = max_amount
	if card_number:
		card_number = str(card_number)
		body["card_number"] = card_number
	if account_id:
		account_id = int(account_id)
		body["account_id"] = account_id
	if customer_id:
		customer_id = int(customer_id)
		body["customer_id"] = customer_id
	if merchant_name:
		merchant_name = str(merchant_name)
		body["merchant_name"] = merchant_name
	if card_type:
		card_type = str(card_type)
		body["card_type"] = card_type
	if transaction_zipcode:
		transaction_zipcode = str(transaction_zipcode)
		body["transaction_zipcode"] = transaction_zipcode
	if transaction_id:
		transaction_id = int(transaction_id)
		body["transaction_id"] = transaction_id
	info = requests.post(base_url + option, data=json.dumps(body))
	return info

''' get rewards info (ex: account_id = 100700000)
must have account_id

request{
account_id: int,
date_from: str (format mm/yyyy)
date_to: str (format mm/yyyy)
card_type: str}

response{
account_id: int,
card_type: str
rewards: [
		{
			month: str,
			total_rewards_earned: float,
			total_rewards_used: int,
			rewards_remaining: float,
			year: int
		},
		...
	]
}
'''
def get_rewards_info(account_id, date_from=None, date_to=None, card_type=None):
	option = 'rewards'
	body = {}
	account_id = int(account_id)
	body["account_id"] = account_id
	if date_from:
		date_from = str(date_from)
		body["date_from"] = date_from
	if date_to:
		date_to = str(date_to)
		body["date_to"] = date_to
	if card_type:
		card_type = str(card_type)
		body["card_type"] = card_type
	info = requests.post(base_url + option, data=json.dumps(body))
	return info

''' get payment info (ex: account_id = 100700000)
must have account_id

request{
account_id: int,
date_from: str (format mm/yyyy)
date_to: str (format mm/yyyy)}

response{
card_type: str,
account_id: int,
payment: [
	{
		total_monthly_balance: float,
		year: int,
		total_balance_remaining: float,
		total_balance_paid: float,
		month: str
	},
	...
	]
}
'''
def get_payment_info(account_id, date_from=None, date_to=None):
	option = 'payments'
	body = {}
	account_id = int(account_id)
	body["account_id"] = account_id
	if date_from:
		date_from = str(date_from)
		body["date_from"] = date_from
	if date_to:
		date_to = str(date_to)
		body["date_to"] = date_to
	info = requests.post(base_url + option, data=json.dumps(body))
	return info

# -----below are three write APIs-----

''' add new account
must have team_name

request{
team_name: str}

response{
account_id: int
status: str}
'''
def add_new_account(team_name):
	option = 'add-account'
	team_name = str(team_name)
	body = {"team_name": team_name}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info

''' add new authorized user
team_name and account_id are both required

request{
team_name: str
account_id: int}

response{
account_id: int
customer_id: int
status: str}
'''
def add_new_au(team_name, account_id):
	option = 'accounts'
	team_name = str(team_name)
	account_id = int(account_id)
	body = {"team_name": team_name,
	"account_id": account_id}
	info = requests.post(base_url + option, data=json.dumps(body))
	return info


''' update customer
team_name and customer_id are both required

request{
team_name: str
customer_id: int
first_name: str
last_name: str
address: str
city: str
state: str
zipcode: str
is_married: bool
phone_number: str
email: str}

response{
customer_id: int
status: str}
'''
def update_customer(team_name, customer_id, 
first_name=None, last_name=None, address=None, city=None, state=None,
zipcode=None, is_married=None, phone_number=None, email=None):
	option = 'update-customer'
	body = {}
	team_name = str(team_name)
	body["team_name"] = team_name
	customer_id = int(customer_id)
	body["customer_id"] = customer_id
	if first_name:
		first_name = str(first_name)
		body["first_name"] = first_name
	if last_name:
		last_name = str(last_name)
		body["last_name"] = last_name
	if address:
		address = str(address)
		body["address"] = address
	if city:
		city = str(city)
		body["city"] = city
	if state:
		state = str(state)
		body["state"] = state
	if zipcode:
		zipcode = str(zipcode)
		body["zipcode"] = zipcode
	if is_married:
		is_married = bool(is_married)
		body["is_married"] = is_married
	if phone_number:
		phone_number = str(phone_number)
		body["phone_number"] = phone_number
	if email:
		email = str(email)
		body["email"] = email
	info = requests.post(base_url+option, data=json.dumps(body))
	return info

# used for debug
# info = get_customer_info()
# print(info.json())