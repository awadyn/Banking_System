from config import basedir
from app import app, db, models

import os
import json
import unittest
import tempfile
import requests
import datetime
import uuid


class FlaskTestCase(unittest.TestCase):

	test_url = 'http://127.0.0.1:5000'
	uid_1 = str(uuid.uuid4())
	uid_2 = str(uuid.uuid4())
	tid_1 = str(uuid.uuid4())
	tid_2 = str(uuid.uuid4()) 
	tid_3 = str(uuid.uuid4())
 

	
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		db.create_all()
		user_1 = models.User(userid=self.uid_1, password='1111111111', balance=0)
		user_2 = models.User(userid=self.uid_2, password='2222222222', balance=0)
		transfer_1 = models.Transfer(transferid=self.tid_1, sourceid=self.uid_1, destid=self.uid_2, amount=50, date=datetime.date.today(), message='first transfer')
		transfer_2 = models.Transfer(transferid=self.tid_2, sourceid=self.uid_2, destid=self.uid_1, amount=150, date=datetime.date.today(), message='second transfer')
		transfer_3 = models.Transfer(transferid=self.tid_3, sourceid=self.uid_1, destid=self.uid_2, amount=50, date=datetime.date.today(), message='third transfer')
		db.session.add(user_1)
		db.session.add(user_2)
		db.session.add(transfer_1)
		db.session.add(transfer_2)
		db.session.add(transfer_3)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def register(self, password, confirm_password):
		data = dict(password=password, confirm_password=confirm_password)
		return requests.post(self.test_url + '/register', json=data)
	def test_register(self):
		response = self.register('3333333333', '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register(None, '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333', '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register(123, '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', None)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333222222')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)

	def balance(self, userid, password):
		data = dict(userid=userid, password=password)
		return requests.post(self.test_url + '/balance', json=data)
	def test_balance(self):
		response = self.balance(self.uid_1, '1111111111')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(None, '1111111111')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance('invalid_userid', '1111111111')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(123, '1111111111')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(self.uid_1, None)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(self.uid_1, '1234')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(self.uid_1, 1234)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)

	def transfers(self, userid, password):
		data = dict(userid=userid, password=password)
		return requests.post(self.test_url + '/transfers', json=data)
	def test_transfers(self):
		response = self.transfers(self.uid_2, '2222222222')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /transfers')
		print(response.text)

	def create_transfer(self, sourceid, password, destid, amount, message):
		data = dict(sourceid=sourceid, password=password, destid=destid, amount=amount, message=message)
		return requests.post(self.test_url + '/create_transfer', json=data)
	def test_create_transfer(self):
		response = self.create_transfer(self.uid_1, '1111111111', self.uid_2, 10, 'transfer message')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(self.uid_1, '1111111111', None, 10, 'transfer message')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(self.uid_1, '1111111111', 'invalid_destid', 10, 'transfer message')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(self.uid_1, '1111111111', self.uid_2, None, 'transfer message')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(self.uid_1, '1111111111', self.uid_2, 'invalid_amount', 'transfer message')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(self.uid_1, '1111111111', self.uid_2, -1, 'transfer message')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)

	def handle_incoming_request(self, userid, password, transferid, approve):
		data = dict(userid=userid, password=password, transferid=transferid, approve=approve)
		return requests.post(self.test_url + '/handle_incoming_request', json=data)
	def test_handle_incoming_request(self):
		response = self.handle_incoming_request(self.uid_2, '2222222222', self.tid_1, True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(self.uid_2, '2222222222', self.tid_1, False)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(self.uid_2, '2222222222', None, True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(self.uid_2, '2222222222', 'invalid_transferid', True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(self.uid_2, '2222222222', 123, True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(self.uid_2, '2222222222', self.tid_1, 123)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)




if __name__ == '__main__':
	unittest.main()
