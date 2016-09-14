from flask import Flask, request, session, g, redirect, url_for, abort, flash
from flask.json import jsonify
import requests
import json
import os
import string
import random
import datetime

from app import app, db, models




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
	user = models.User.query.filter_by(userid=userid, password=password).first()
	if user == None:
		return False
	else:
		return True

# validate transfer destination
def valid_dest(userid):
	user = models.User.query.filter_by(userid=userid).first()
	if user == None:
		return False
	else:
		return True

# validate transfer
def valid_transfer(transferid, destid):
	transfer = models.Transfer.query.filter_by(transferid=transferid, destid=destid).first()
	if transfer == None:
		return False
	else:
		return True




# view
# show all users
@app.route('/users/')
def show_users():
	users = models.User.query.all()
	print(users)
	return "done\n"



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
			return "You may register here... Please enter a password...\n"
		else:	
			userid = userid_generator()
			new_user = models.User(userid=userid, password=password, balance=0)
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('show_users'))
	else:
		return "No POST Request\n"



# view
# check balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
	if request.method == 'POST':
		userid = request.form['userid']
		password = request.form['password']
		if userid == None:
			return "Balance Page\n"
		elif password == None:
			return "Balance Page for " + userid + "... Please enter password\n"
		else:
			if valid_user(userid, password):
				this_user = models.User.query.filter_by(userid=userid, password=password).first()
				print(this_user.balance)
				return "done\n"
			else:
				return "Incorrect Userid or Password\n"
	else:
		return "No POST Request\n"



# view
# list transfer requests to a user
@app.route('/transfers', methods = ['GET', 'POST'])
def transfers():
	if request.method == 'POST':
		userid = request.form['userid']
		password = request.form['password']
		if userid == None:
			return "Transfers Page\n"
		elif password == None:
			return "Transfers Page for " + userid + "... Please enter password\n"
		else:
			if valid_user(userid, password):
				transfers = models.Transfer.query.filter_by(destid=userid).all()
				print(transfers)
				return "done\n"
			else:
				return "Incorrect Userid or Password\n"
	else:
		return "No POST Request\n"



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
			return "Create Transfer Here\n"
		elif password == None:
			return sourceid + ", you may create a transfer here... Please enter your password\n"
		elif destid == None:
			return sourceid + ", you may create a transfer here... Please enter the destination of this transfer\n"
		elif amount == None:
			return sourceid + ", you may create a transfer here... Please enter the amount to transfer\n"
		else:
			transferid = None
			if valid_user(sourceid, password):
				if valid_dest(destid):
					user_balance = models.User.query.filter_by(userid=sourceid, password=password).first().balance
					if user_balance >= int(amount):
						transferid = transferid_generator()
						transfer = models.Transfer(transferid=transferid, date=datetime.date.today(), sourceid=sourceid, destid=destid, amount=amount)
						db.session.add(transfer)
						db.session.commit()
						print(transfer)
						return "done\n"
					else:
						return "Insufficient Balance\n"
				else:
					return "Invalid Transfer Destination\n"
			else:
				return "Incorrect Userid or Password\n"
	else:
		return "No POST Request\n"



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
			return "Handle Requests Here\n"
		elif password == None:
			return "Handle Requests to " + userid + "... Please enter password\n"
		elif transferid == None:
			return "Handle Requests to " + userid + "... Please enter transferid\n"
		elif approve == None:
			return "Handle Transfer Request " + transferid + " to " + userid + "... Approve?\n"
		else:
			if valid_user(userid, password):
				if valid_transfer(transferid, userid):
					if int(approve) == 1:
						dest_user = models.User.query.filter_by(userid=userid).first()
						transfer = models.Transfer.query.filter_by(transferid=transferid).first()
						source_user = models.User.query.filter_by(userid=transfer.sourceid).first()
						dest_user.balance += transfer.amount
						source_user.balance -= transfer.amount
						db.session.delete(transfer)
						db.session.commit()
						return "Transfer Handled\n"
					else:
						return "Transfer " + transferid + " Not Approved\n"
				else:
					return "Invalid Transfer\n"
			else:
				return "Incorrect Username or Password\n"
	else:
		return "No POST Request\n"




