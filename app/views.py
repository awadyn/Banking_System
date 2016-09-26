from flask import Flask, request, redirect, url_for, flash, render_template
from flask.json import jsonify
import requests
import json
import os
import string
import random
import datetime
import uuid
import sys
import validators
from time import mktime

from app import app, db, models
from .forms import RegisterForm, BalanceForm, TransfersForm, CreateTransferForm, HandleIncomingRequestForm

# allow datetime to be json serializable
# currently not doing the job -.-
class MyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return int(mktime(obj.timetuple()))
		else:
			return json.JSONEncoder.default(self, obj)


######################
##### Generators #####
######################

# compress UUID
# UUID to more compact form (string of 22 characters)
def uuid2compact(uuid):
	return uuid.bytes.encode('base64'.rstrip('=\n').replace('/','_'))

# decompress UUID
# from string of 22 characters to UUID
def compact2uuid(uuid_compact):
	return str(uuid.UUID(bytes=(uuid_compact + '==').replace('_','/').decode('base64')))

# generate unique userid's using python's uuid module
# uuid4(): generates unique uuid from random number
# returns unique userid as str
def userid_generator():
	return str(uuid.uuid4())
#	return uuid2compact(uuid.uuid4())

# generate unique transferid's using python's uuid module
# uuid4(): generates unique uuid from random number
# returns unique userid as str
def transferid_generator():
	return str(uuid.uuid4())
	return uuid2compact(uuid.uuid4())


#####################
##### Verifiers #####
#####################

# verify user
def verified_user(userid, password):
	user = models.User.query.filter_by(userid=userid, password=password).first()
	if user == None:
		return False
	else:
		return True

# verify transfer destination
def verified_dest(userid):
	user = models.User.query.filter_by(userid=userid).first()
	if user == None:
		return False
	else:
		return True

# verify transfer
def verified_transfer(transferid, destid):
	transfer = models.Transfer.query.filter_by(transferid=transferid, destid=destid).first()
	if transfer == None:
		return False
	else:
		return True


######################		
##### Validators #####
######################

# validate id
def valid_id(userid, id_repr):
	error = ''
	if userid == None:
		error += "---- " + id_repr + " Required ----\n"
	elif not isinstance(userid, basestring):
		error += "---- " + id_repr + " Must be Instance of String ----\n"
	elif not validators.uuid(userid):
		error += "---- Invalid " + id_repr + " ----\n"
	return error

# validate passwords
def valid_password(password, password_repr):
	error = ''
	if password == None:
		error += "---- " + password_repr + " Required ----\n"
	elif not isinstance(password, basestring):
		error += "---- " + password_repr + " Must be Instance of String ----\n"
	elif not validators.between(len(password), min=8, max=16):
		error += "---- " + password_repr + " Length Must Be Between 8 and 16 Characters Long ----\n"
	return error

# validate amounts
def valid_amount(amount, amount_repr):
	error = ''
	if amount == None:
		error += "---- " + amount_repr + " Required ----\n"
	elif type(amount) != int:
		error += "---- " + amount_repr + " Must be Integer ----\n"
	elif not validators.between(amount, min=0, max=sys.maxint):
		error += "---- Invalid " + amount_repr + " ----"
	return error

# validate registration
def valid_register_request(password, confirm_password):
	error = ''
	error += valid_password(password, "Password")
	error += valid_password(confirm_password, "Password Confirmation")
	if password != confirm_password:
		error += "---- Passwords Don't Match ----\n"
	return error

# validate user credentials
def valid_user_credentials(userid, password):
	error = ''
	error += valid_id(userid, "UserID")
	error += valid_password(password, "Password")
	return error

# validate balance check request
def valid_balance_request(userid, password):
	return valid_user_credentials(userid, password)

# validate transfers check request
def valid_transfers_request(userid, password):
	return valid_user_credentials(userid, password)

# validate create transfer request
def valid_create_transfer_request(sourceid, password, destid, amount):
	error = ''
	error += valid_id(sourceid, "SourceID")
	error += valid_password(password, "Password")
	error += valid_id(destid, "DestinationID")
	error += valid_amount(amount, "Amount")
	return error
	
# validate handle transfer request
def valid_handle_transfer_request(userid, password, transferid, approve):
	error = ''
	error += valid_id(userid, "UserID")
	error += valid_password(password, "Password")
	error += valid_id(transferid, "TransferID")
	if approve == None:
		error += "---- Approval Required ----\n"
	elif type(approve) != bool:
		error += "---- Approve Must be Boolean ----\n"
	return error


#################
##### Views #####
#################

# view
# index page (temporary)
@app.route('/index')
def index():
	return render_template('index.html', title='Home')



# view
# register new user
@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		request_content = request.json
		password = request_content.get('password')
		confirm_password = request_content.get('confirm_password')
		error = valid_register_request(password, confirm_password)
		if error == '':
			userid = userid_generator()
			new_user = models.User(userid=userid, password=password, balance=0)
			db.session.add(new_user)
			db.session.commit()
			return jsonify({'New User':str(new_user)})
		else:
			return error
	else:
		return "---- No POST Request ----\n"



# view
# check balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
	if request.method == 'POST':
		request_content = request.json
		userid = request_content.get('userid')
		password = request_content.get('password')
		error = valid_balance_request(userid, password)
		if error == '':
			if verified_user(userid, password):
				this_user = models.User.query.filter_by(userid=userid, password=password).first()
				balance = this_user.balance
				return jsonify({'User':userid, 'Balance':balance})
			else:
				return "---- User Not Found ----\n"
		else:
			return error
	else:
		return "---- No POST Request ----\n"



# view
# list transfer requests to a user
@app.route('/transfers', methods = ['GET', 'POST'])
def transfers():
	if request.method == 'POST':
		request_content = request.json
		userid = request_content.get('userid')
		password = request_content.get('password')
		error = valid_transfers_request(userid, password)
		if error == '':
			if verified_user(userid, password):
				transfers = models.Transfer.query.filter_by(destid=userid).all()
				return jsonify({'Transfers':str(transfers)})
			else:
				return "---- User Not Found ----\n"
		else:
			return error
	else:
		return "---- No POST Request ----\n"




# view
# create a transfer request
@app.route('/create_transfer', methods=['GET', 'POST'])
def create_transfer():
	if request.method == 'POST':
		request_content = request.json
		sourceid = request_content.get('sourceid')
		password = request_content.get('password')
		destid = request_content.get('destid')
		amount = request_content.get('amount')
		message = request_content.get('message')
		error = valid_create_transfer_request(sourceid, password, destid, amount)
		if error == '':
			if verified_user(sourceid, password):
				if verified_dest(destid):
					transferid = transferid_generator()
					transfer = models.Transfer(transferid=transferid, date=datetime.date.today(), sourceid=sourceid, destid=destid, amount=amount, message=message)
					db.session.add(transfer)
					db.session.commit()
					return jsonify({'New Transfer':str(transfer), 'Message':transfer.message})
				else:
					return "---- Destination Not Found ----\n"
			else:
				return "---- User Not Found ----\n"
		else:
			return error
	else:
		return "---- No POST Request ----\n"




# view
# handle incoming request
@app.route('/handle_incoming_request', methods=['GET', 'POST'])
def handle_incoming_request():
	if request.method == 'POST':
		request_content = request.json
		userid = request_content.get('userid')
		password = request_content.get('password')
		transferid = request_content.get('transferid')
		approve = request_content.get('approve')
		error = valid_handle_transfer_request(userid, password, transferid, approve)
		if error == '':
			if verified_user(userid, password):
				if verified_transfer(transferid, userid):
					if approve == True:
						dest_user = models.User.query.filter_by(userid=userid).first()
						transfer = models.Transfer.query.filter_by(transferid=transferid).first()
						source_user = models.User.query.filter_by(userid=transfer.sourceid).first()
						dest_user.balance += transfer.amount
						source_user.balance -= transfer.amount
						db.session.delete(transfer)
						db.session.commit()
						return jsonify({'Transfer':transfer.transferid, 'Status':'Approved', 'New Balance':dest_user.balance})
					else:
						return jsonify({'Transfer':transfer.transferid, 'Status':'Not Approved'})
				else:
					return "---- Transfer Not Found ----\n"
			else:
				return "---- User Not Found ----\n"
		else:
			return error
	else:
		return "No POST Request\n"




