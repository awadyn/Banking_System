from flask import Flask, request, session, g, redirect, url_for, abort, flash, render_template
from flask.json import jsonify
import requests
import json
import os
import string
import random
import datetime
import uuid


from app import app, db, models
from .forms import RegisterForm, BalanceForm, TransfersForm, CreateTransferForm, HandleIncomingRequestForm


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
# index page (temporary)
@app.route('/index')
def index():
	return render_template('index.html', title='Home')



# view
# register new user
@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()
	if request.method == 'POST' and form.validate_on_submit():
		userid = userid_generator()
		new_user = models.User(userid=userid, password=form.password.data, balance=form.balance.data, temp_balance=form.balance.data)
		db.session.add(new_user)
		db.session.commit()
		# for debugging
		flash('Registration Validated for User = "%s", Password = "%s", Balance = %d' % (userid, form.password.data, form.balance.data))
		return redirect('/index')
	else:
		return render_template('register.html', title='Register', form=form)



# view
# check balance
@app.route('/balance', methods=['GET', 'POST'])
def balance():
	form = BalanceForm()
	if request.method == 'POST' and form.validate_on_submit():
		userid = form.userid.data
		password = form.password.data
		if valid_user(userid, password):
			this_user = models.User.query.filter_by(userid=userid, password=password).first()
			balance = this_user.balance
			# for debugging
			flash('Balance Check Validated for User = "%s", Password = "%s": Balance = %d' % (userid, password, balance))
			return redirect('/index')
		else:
			flash('Incorrect UserID or Password', 'error')
			return render_template('balance.html', title='Balance', form=form)
	else:
		return render_template('balance.html', title='Balance', form=form)



# view
# list transfer requests to a user
@app.route('/transfers', methods = ['GET', 'POST'])
def transfers():
	form = TransfersForm()
	if request.method == 'POST' and form.validate_on_submit():
		userid = form.userid.data
		password = form.password.data
		if valid_user(userid, password):
			transfers = models.Transfer.query.filter_by(destid=userid).all()
			# for debugging
			flash('Check Transfers Validated for User = "%s", Password = "%s": Transfers = %s' % (userid, password, str(transfers)))
			return redirect('/index')
		else:
			flash('Incorrect UserID or Password', 'error')
			return render_template('transfers.html', title='Transfers', form=form)
	else:
		return render_template('transfers.html', title='Transfers', form=form)



# view
# create a transfer request
@app.route('/create_transfer', methods=['GET', 'POST'])
def create_transfer(sourceid=None, password=None, destid=None, amount=None):
	form = CreateTransferForm()
	if request.method == 'POST' and form.validate_on_submit():
		sourceid = form.sourceid.data
		password = form.password.data
		destid = form.destid.data
		amount = form.amount.data
		if valid_user(sourceid, password):
			if valid_dest(destid):
				user_balance = models.User.query.filter_by(userid=sourceid, password=password).first().balance
				user_temp_balance = models.User.query.filter_by(userid=sourceid, password=password).first().temp_balance
				if user_balance >= int(amount):
					if user_temp_balance >= int(amount):
						transferid = transferid_generator()
						transfer = models.Transfer(transferid=transferid, date=datetime.date.today(), sourceid=sourceid, destid=destid, amount=amount)
						models.User.query.filter_by(userid=sourceid, password=password).first().temp_balance -= int(amount)
						db.session.add(transfer)
						db.session.commit()
						# for debugging
						flash('Create Transfer Validated for User = "%s", Password = "%s", Destination = "%s", Amount= %d: TransferID = "%s"' % (sourceid, password, destid, amount, transferid))
						return redirect('/index')
					else:
						flash('Cannot make this transfer... Try handling incoming requests first', 'error')
						return render_template('create_transfer.html', title='Create Transfer', form=form)
				else:
					flash('Cannot make this transfer... Insufficient Balance', 'error')
					return render_template('create_transfer.html', title='Create Transfer', form=form)
			else:
				flash('Invalid Transfer Destination', 'error')
				return render_template('create_transfer.html', title='Create Transfer', form=form)
		else:
			flash('Incorrect Userid or Password', 'error')				
			return render_template('create_transfer.html', title='Create Transfer', form=form)
	else:
		return render_template('create_transfer.html', title='Create Transfer', form=form)



# view
# handle incoming request
@app.route('/handle_incoming_request', methods=['GET', 'POST'])
def handle_incoming_request():
	form = HandleIncomingRequestForm()
	if request.method == 'POST' and form.validate_on_submit():
		userid = form.userid.data
		password = form.password.data
		transferid = form.transferid.data
		approve = form.approve.data
		if valid_user(userid, password):
			if valid_transfer(transferid, userid):
				if int(approve) == 1:
					dest_user = models.User.query.filter_by(userid=userid).first()
					transfer = models.Transfer.query.filter_by(transferid=transferid).first()
					source_user = models.User.query.filter_by(userid=transfer.sourceid).first()
					dest_user.balance += transfer.amount
					dest_user.temp_balance += transfer.amount
					source_user.balance -= transfer.amount
					db.session.delete(transfer)
					db.session.commit()
					# for debugging
					flash('Handle Transfer Validated for User = "%s", Password = "%s", Transfer = "%s", Approve= %d: New Balance = %d' % (userid, password, transferid, int(approve), dest_user.balance))
					return redirect('/index')
				else:
					flash('Transfer Not Approved', 'error')
					return render_template('handle_incoming_request.html', title='Handle Incoming Request', form=form)
			else:
				flash('Invalid Transfer', 'error')
				return render_template('handle_incoming_request.html', title='Handle Incoming Request', form=form)
		else:
			flash('Incorrect Username or Password', 'error')
			return render_template('handle_incoming_request.html', title='Handle Incoming Request', form=form)
	else:
		return render_template('handle_incoming_request.html', title='Handle Incoming Request', form=form)




