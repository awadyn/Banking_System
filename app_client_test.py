from app import app

import os
import json
import unittest
import tempfile
import requests
import uuid

class FlaskTestCase(unittest.TestCase):

	test_url = 'http://127.0.0.1:5000'
	
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
	
	def tearDown(self):
		pass

	def register(self, password, confirm_password, balance):
		data = dict(password=password, confirm_password=confirm_password, balance=balance)
		return requests.post(self.test_url + '/register', json=data)
	def test_register(self):
		response = self.register('3333333333', '3333333333', 200)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register(None, '3333333333', 200)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333', '3333333333', 200)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', None, 200)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333', 200)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333222222', 200)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333333333', None)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333333333', -1)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)
		response = self.register('3333333333', '3333333333', 'invalid_balance')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register')
		print(response.text)

	def balance(self, userid, password):
		data = dict(userid=userid, password=password)
		return requests.post(self.test_url + '/balance', json=data)
	def test_balance(self):
		userid = str(uuid.uuid4())
		response = self.balance(userid, '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(None, '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance('invalid_userid', '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(123, '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(userid, None)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(userid, '3333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)
		response = self.balance(userid, 123)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance')
		print(response.text)

	def transfers(self, userid, password):
		data = dict(userid=userid, password=password)
		return requests.post(self.test_url + '/transfers', json=data)
	def test_transfers(self):
		userid = str(uuid.uuid4())
		response = self.transfers(userid, '3333333333')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /transfers')
		print(response.text)

	def create_transfer(self, sourceid, password, destid, amount):
		data = dict(sourceid=sourceid, password=password, destid=destid, amount=amount)
		return requests.post(self.test_url + '/create_transfer', json=data)
	def test_transfers(self):
		sourceid = str(uuid.uuid4())
		destid = str(uuid.uuid4())
		response = self.create_transfer(sourceid, '3333333333', destid, 10)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(sourceid, '3333333333', None, 10)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(sourceid, '3333333333', 'invalid_destid', 10)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(sourceid, '3333333333', destid, None)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(sourceid, '3333333333', destid, 'invalid_amount')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)
		response = self.create_transfer(sourceid, '3333333333', destid, -1)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /create_transfer')
		print(response.text)

	def handle_incoming_request(self, userid, password, transferid, approve):
		data = dict(userid=userid, password=password, transferid=transferid, approve=approve)
		return requests.post(self.test_url + '/handle_incoming_request', json=data)
	def test_handle_incoming_request(self):
		userid = str(uuid.uuid4())
		transferid = str(uuid.uuid4())
		response = self.handle_incoming_request(userid, '3333333333', transferid, True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(userid, '3333333333', transferid, False)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(userid, '3333333333', None, True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(userid, '3333333333', 'invalid_transferid', True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(userid, '3333333333', 123, True)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)
		response = self.handle_incoming_request(userid, '3333333333', transferid, 123)
		self.assertEqual(response.status_code, 200)
		print('Unittest: /handle_incoming_request')
		print(response.text)




if __name__ == '__main__':
	unittest.main()
