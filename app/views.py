from flask import Flask, request, session, g, redirect, url_for, abort, flash
from flask.json import jsonify
import requests
import json
import os
import string
import random

from app import app


user_data = {'awadyn':['1234',100], 'yna03':['12345',100]}
transfer_requests = {'id1':[222, 'awadyn', 'yna03', 50], 'id2':[333, 'awadyn', 'yna03', 20]}


# generate random passwords
def pass_generator(size=4, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# generate random user_id
def userid_generator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# generate random transfer_id
def transferid_generator(size=4, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# validate user
def valid_user(userid, password):
	for key in user_data:
		if key == userid:
			if user_data[userid][0] == password:
				return True
	return False

# validate transfer destination
def valid_dest(userid):
	for key in user_data:
		if key == userid:
			return True
	return False

# validate transfer
def valid_transfer(transferid, destid):
	for key in transfer_requests:
		if key == transferid:		
			if transfer_requests[key][2] == destid:
				return True
	return False




# view
# show all users
@app.route('/users/')
def show_users():
	return jsonify(user_data)


@app.route('/clear/')
def clear():
	user_data.clear()
	transfer_requests.clear()
	return jsonify(user_data)




# view
# register new user
@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		password = request.form['password']
		if password == None:
			return 'You may register here... Please enter a password...'
		else:	
			userid = userid_generator()
			user_data[userid] = [password, 0]
			return jsonify(user_data)
	else:
		return 'No POST Request'



# view
# check balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
	if request.method == 'POST':
		userid = request.form['userid']
		password = request.form['password']
		if userid == None:
			return 'Balance Page'
		elif password == None:
			return 'Balance Page for ' + userid + '... Please enter password'
		else:
			if valid_user(userid, password):
				return jsonify({'balance':user_data[userid][1]})
			else:
				return 'Incorrect Userid or Password'
	else:
		return 'No POST Request'



# view
# list transfer requests by a user
@app.route('/transfers', methods = ['GET', 'POST'])
def transfers():
	if request.method == 'POST':
		userid = request.form['userid']
		password = request.form['password']
		if userid == None:
			return 'Transfers Page'
		elif password == None:
			return 'Transfers Page for ' + userid + '... Please enter password'
		else:
			transfers = []
			if valid_user(userid, password):
				for key in transfer_requests:
					if transfer_requests[key][2] == userid:
						transfers.append(transfer_requests[key])	
				return jsonify({'transfer_requests':transfers})
			else:
				return 'Incorrect Userid or Password'
	else:
		return 'No POST Request'



# view
# create a transfer request
@app.route('/create_transfer', methods=['GET', 'POST'])
def create_transfer(sourceid=None, password=None, destid=None, amount=None):
	if request.method == 'POST':
		sourceid = request.form['sourceid']
		password = request.form['password']
		destid = request.form['destid']
		amount = request.form['amount']
		if sourceid == None:
			return 'Create Transfer Here'
		elif password == None:
			return sourceid + ', you may create a transfer here... Please enter your password'
		elif destid == None:
			return sourceid + ', you may create a transfer here... Please enter the destination of this transfer'
		elif amount == None:
			return sourceid + ', you may create a transfer here... Please enter the amount to transfer'
		else:
			transferid = None
			if valid_user(sourceid, password):
				if valid_dest(destid):
					if user_data[sourceid][1] >= int(amount):
						transferid = transferid_generator()
						transfer_requests[transferid] = [444, sourceid, destid, int(amount)]
						return transferid
					else:
						return 'Insufficient Balance'
				else:
					return 'Invalid Transfer Destination'
			else:
				return 'Incorrect Userid or Password'
	else:
		return 'No POST Request'



# view
# handle incoming request
@app.route('/handle_incoming_request', methods=['GET', 'POST'])
def handle_incoming_request():
	if request.method == 'POST':
		userid = request.form['userid']
		password = request.form['password']
		transferid = request.form['transferid']
		approve = request.form['approve']
		if userid == None:
			return 'Handle Requests Here'
		elif password == None:
			return 'Handle Requests to ' + userid + '... Please enter password'
		elif transferid == None:
			return 'Handle Requests to ' + userid + '... Please enter transferid'
		elif approve == None:
			return 'Handle Transfer Request ' + transferid + ' to ' + userid + '... Approve?'
		else:
			if valid_user(userid, password):
				if valid_transfer(transferid, userid):
					if int(approve) == 1:
						user_data[transfer_requests[transferid][1]][1] -= transfer_requests[transferid][3]
						user_data[userid][1] += transfer_requests[transferid][3]
						del transfer_requests[transferid]
						return 'Transfer Handled'
					else:
						return 'Transfer ' + transferid + ' Not Approved'
				else:
					return 'Invalid Transfer'
			else:
				return 'Incorrect Username or Password'
	else:
		return 'No POST Request'




