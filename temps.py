	def handle_incoming_request(self, userid=None, password=None, transferid=None, approve=None):
		tester = app.test_client(self)
		return tester.post('/handle_incoming_request', data=dict(userid=userid, password=password, transferid=transferid, approve=approve))
	def test_handle_incoming_request(self):
		response_3 = self.handle_incoming_request('awadyn', '1234', 'bvox', '1')
		self.assertEqual(response_3.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=awadyn, password=1234, transferid=bvox, approve=1}: ' + response_3.data)
		response_4 = self.handle_incoming_request('awadyn', '1234', 'bvox', '1')
		self.assertEqual(response_4.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=awadyn, password=1234, transferid=bvox, approve=1}: ' + response_4.data)
		response_5 = self.handle_incoming_request('awadyn', '1234', '8nt3', '1')
		self.assertEqual(response_5.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=yna03, password=12345, transferid=id7, approve=1}: ' + response_5.data)
		response_6 = self.handle_incoming_request('yna03', '12345', 'id2', '0')
		self.assertEqual(response_6.status_code, 200)
		print('Unittest: /handle_incoming_request, {userid=yna03, password=12345, transferid=id2, approve=0}: ' + response_6.data)
		

	def create_transfer(self, sourceid=None, password=None, destid=None, amount=None):
		tester = app.test_client(self)
		return tester.post('/create_transfer', data=dict(sourceid=sourceid, password=password, destid=destid, amount=amount))
	def test_create_transfer(self):
		response_3 = self.create_transfer('yna03', '12345', 'awadyn', '60')
		self.assertEqual(response_3.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=yna03, password=12345, destid=awadyn, amount=60}: ' + response_3.data)
		response_4 = self.create_transfer('yna03', '12345', 'awadyn', '150')
		self.assertEqual(response_4.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=yna03, password=12345, destid=awadyn, amount=150}: ' + response_4.data)
		response_5 = self.create_transfer('bla', '12345', 'awadyn', '150')
		self.assertEqual(response_5.status_code, 200)
		print('Unittest: /create_transfer, {sourceid=bla, password=12345, destid=awadyn, amount=150}: ' + response_5.data)
		

	def transfers(self, userid=None, password=None):
		tester = app.test_client(self)
		return tester.post('/transfers', data=dict(userid=userid, password=password), follow_redirects=True)
	def test_transfers(self):
		response_3 = self.transfers('yna03', '1234')
		self.assertEqual(response_3.status_code, 200)
		print('Unittest: /transfers, {userid=yna03, password=1234}: ' + response_3.data)
		response_4 = self.transfers('awadyn', '1234')
		self.assertEqual(response_4.status_code, 200)
		print('Unittest: /transfers, {userid=awadyn, password=1234}: ' + response_4.data)
		response_5 = self.transfers('yna03', '12345')
		self.assertEqual(response_5.status_code, 200)
		print('Unittest: /transfers, {userid=yna03, password=12345}: ' + response_5.data)
		

	def register(self, password=None):
		tester = app.test_client(self)

