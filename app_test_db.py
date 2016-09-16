import os
import json
import unittest
import tempfile
import datetime

from config import basedir
from app import app, db
from app import models


class FlaskTestCase(unittest.TestCase):
	
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()
		user_1 = models.User(userid='awadyn', password='1234', balance=100, temp_balance=100)
		user_2 = models.User(userid='yna03', password='12345', balance=200, temp_balance=200)
		transfer_1 = models.Transfer(transferid='id1', date=datetime.date.today(), sourceid='awadyn', destid='yna03', amount=50)
		transfer_2 = models.Transfer(transferid='id2', date=datetime.date.today(), sourceid='yna03', destid='awadyn', amount=20)
		transfer_3 = models.Transfer(transferid='id3', date=datetime.date.today(), sourceid='awadyn', destid='yna03', amount=150)
		db.session.add(user_1)
		db.session.add(user_2)
		db.session.add(transfer_1)
		db.session.add(transfer_2)
		db.session.add(transfer_3)
		db.session.commit()


	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_users(self):
		response = self.app.get('/users/', content_type = 'application/json')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /show_users/: ' + response.data)


	def register(self, password=None):
		return self.app.post('/register', data=dict(password=password), follow_redirects=True)			
	def test_register(self):
		response = self.register('1234567')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /register, {password=1234567}: ' + response.data)


	def balance(self, userid=None, password=None):
		return self.app.post('/balance', data=dict(userid=userid, password=password), follow_redirects=True)
	def test_balance(self):
		response = self.balance('yna03', '1234')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /balance, {userid=yna03, password=1234}: ' + response.data)
		response_0 = self.balance('yna03', '12345')
		self.assertEqual(response_0.status_code, 200)
		print('Unittest: /balance, {userid=yna03, password=12345}: ' + response_0.data)
		response_1 = self.balance('awadyn', '1234')
		self.assertEqual(response_1.status_code, 200)
		print('Unittest: /balance, {userid=awadyn, password=1234}: ' + response_1.data)


	def transfers(self, userid=None, password=None):
		return self.app.post('/transfers', data=dict(userid=userid, password=password), follow_redirects=True)
	def test_transfers(self):
		response = self.transfers('yna03', '12345')
		self.assertEqual(response.status_code, 200)
		print('Unittest: /transfers, {userid=yna03, password=1234}: ' + response.data)
		response_0 = self.transfers('awadyn', '1234')
		self.assertEqual(response_0.status_code, 200)
		print('Unittest: /transfers, {userid=awadyn, password=1234}: ' + response_0.data)
		response_1 = self.transfers('yna03', 'not_this_password')
		self.assertEqual(response_1.status_code, 200)
		print('Unittest: /transfers, {userid=yna03, password=not_this_password}: ' + response_1.data)


	def create_transfer(self, sourceid=None, password=None, destid=None, amount=None):
		return self.app.post('/create_transfer', data=dict(sourceid=sourceid, password=password, destid=destid, amount=amount))
	def test_create_transfer(self):
		response_2 = self.create_transfer('yna03', '12345', 'awadyn', '150')
		self.assertEqual(response_2.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=yna03, password=12345, destid=awadyn, amount=150}: ' + response_2.data)
		response_3 = self.create_transfer('yna03', '12345', 'awadyn', '60')
		self.assertEqual(response_3.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=yna03, password=12345, destid=awadyn, amount=60}: ' + response_3.data)
		response_4 = self.create_transfer('yna03', '12345', 'awadyn', '300')
		self.assertEqual(response_4.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=yna03, password=12345, destid=awadyn, amount=300}: ' + response_4.data)
		response_5 = self.create_transfer('awadyn', '1234', 'yna03', '10')
		self.assertEqual(response_5.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=awadyn, password=1234, destid=yna03, amount=10}: ' + response_5.data)
		response_6 = self.create_transfer('yna03', '12345', 'not_this_destination', '60')
		self.assertEqual(response_6.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=yna03, password=12345, destid=not_this_destination, amount=60}: ' + response_6.data)
		

	def handle_incoming_request(self, userid=None, password=None, transferid=None, approve=None):
		return self.app.post('/handle_incoming_request', data=dict(userid=userid, password=password, transferid=transferid, approve=approve))
	def test_handle_incoming_request(self):
		response_3 = self.handle_incoming_request('awadyn', '1234', 'id2', '1')
		self.assertEqual(response_3.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=awadyn, password=1234, transferid=id2, approve=1}: ' + response_3.data)
		response_4 = self.handle_incoming_request('awadyn', '1234', 'not_this_transfer', '1')
		self.assertEqual(response_4.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=awadyn, password=1234, transferid=not_this_transfer, approve=1}: ' + response_4.data)
		response_5 = self.handle_incoming_request('yna03', '12345', 'id1', '1')
		self.assertEqual(response_5.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=yna03, password=12345, transferid=id1, approve=1}: ' + response_5.data)
		response_6 = self.handle_incoming_request('yna03', '12345', 'id3', '0')
		self.assertEqual(response_6.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=yna03, password=12345, transferid=id3, approve=0}: ' + response_6.data)
	

	

if __name__ == '__main__':
	unittest.main()
