from flask import Flask, request, redirect, url_for, flash, render_template
from flask.json import jsonify
import requests
import string
import datetime


from app import app, db, models


import generators
import verifiers
import custom_validators


#################
##### Views #####
#################


# view
# register new user
@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		request_content = request.json
		password = request_content.get('password')
		confirm_password = request_content.get('confirm_password')
		input_error = custom_validators.valid_register_request(password, confirm_password)
		new_user = ''
		if input_error == '':
			userid = generators.id_generator()
			new_user = models.User(userid=userid, password=password, balance=0)	
			db.session.add(new_user)
			db.session.commit()
		return jsonify({'New User':str(new_user), 'Error':input_error})
	else:
		return render_template('register_elm.html', title='Register')


# view
# check balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
	if request.method == 'POST':
		request_content = request.json
		userid = request_content.get('userid')
		password = request_content.get('password')
		input_error = custom_validators.valid_balance_request(userid, password)
		request_error = ''
		balance = ''
		if input_error == '':
			if verifiers.verified_user(userid, password):
				this_user = models.User.query.filter_by(userid=userid, password=password).first()
				balance = this_user.balance
			else:
				request_error += 'User Not Found'
		else:
			request_error += 'User Not Valid'
		return jsonify({'Balance':str(balance), 'Error':request_error})
	else:
		return render_template('balance_elm.html', title='Balance')


# view
# list transfer requests to a user
@app.route('/transfers', methods = ['GET', 'POST'])
def transfers():
	if request.method == 'POST':
		request_content = request.json
		userid = request_content.get('userid')
		password = request_content.get('password')
		input_error = custom_validators.valid_transfers_request(userid, password)
		request_error = ''
		transfers = ''
		if input_error == '':
			if verifiers.verified_user(userid, password):
				transfers = models.Transfer.query.filter_by(destid=userid).all()
			else:
				request_error += 'User Not Found'
		else:
			request_error += 'User Not Valid'
		return jsonify({'Transfers':str(transfers), 'Error':request_error})
	else:
		return render_template('transfers_elm.html', title='Transfers')


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
		message = request_content.get('transfer_message')
		input_error = custom_validators.valid_create_transfer_request(sourceid, password, destid, amount)
		request_error = ''
		new_transfer = ''
		if input_error == '':
			if verifiers.verified_user(sourceid, password):
				if verifiers.verified_dest(destid):
					if sourceid == destid:
						request_error += 'Cannot Make Transfer from Source to Source'
					else:
						transferid = generators.id_generator()
						new_transfer = models.Transfer(transferid=transferid, date=datetime.date.today(), sourceid=sourceid, destid=destid, amount=amount, message=message)
						db.session.add(new_transfer)
						db.session.commit()
				else:
					request_error += 'Destination Not Found'
			else:
				request_error += 'User Not Found'
		else:
			request_error += 'Transaction Not Valid'
		return jsonify({'New Transfer':str(new_transfer), 'Error':request_error})
	else:
		return render_template('create_transfer_elm.html', title='Create Transfer')


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
		input_error = custom_validators.valid_handle_transfer_request(userid, password, transferid, approve)
		request_error = ''
		request_status = ''
		current_balance = ''
		if input_error == '':
			if verifiers.verified_user(userid, password):
				if verifiers.verified_transfer(transferid, userid):
					dest_user = models.User.query.filter_by(userid=userid).first()
					transfer = models.Transfer.query.filter_by(transferid=transferid).first()
					source_user = models.User.query.filter_by(userid=transfer.sourceid).first()
					if approve == True:
						dest_user.balance += transfer.amount
						source_user.balance -= transfer.amount
						db.session.delete(transfer)
						db.session.commit()
						request_status = 'Request Approved'
					else:
						request_status = 'Request Not Approved'
					current_balance = dest_user.balance
				else:
					request_error += 'Transfer Not Found'
			else:
				request_error += 'User Not Found'
		else:
			request_error += 'User Not Valid'
		return jsonify({'Request Status':request_status, 'Current Balance': str(current_balance), 'Error':request_error})
	else:
		return render_template('handle_incoming_request_elm.html', title='Handle Incoming Request')




