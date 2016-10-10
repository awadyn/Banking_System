from app import db

class User(db.Model):
	__tablename__ = 'users'

	userid = db.Column(db.String(22), primary_key=True)
	password = db.Column(db.String(16))
	balance = db.Column(db.Integer)

	def __init__(self, userid, password, balance):
		self.userid = userid
		self.password = password
		self.balance = balance
	
	def __repr__(self):
		return '<User: %s>' % (self.userid)


class Transfer(db.Model):
	__tablename__ = 'transfers'

	transferid = db.Column(db.String(16), primary_key=True)
	date = db.Column(db.DateTime, index=True)
	sourceid = db.Column(db.String(16), db.ForeignKey('users.userid'))
	destid = db.Column(db.String(16), db.ForeignKey('users.userid'))
	amount = db.Column(db.Integer, index=True)
	message = db.Column(db.String(30))

	source = db.relationship('User', foreign_keys=[sourceid])
	dest = db.relationship('User', foreign_keys=[destid])

	def __init__(self, transferid, date, sourceid, destid, amount, message):
		self.transferid = transferid
		self.date = date
		self.sourceid = sourceid
		self.destid = destid
		self.amount = amount
		self.message = message

	def __repr__(self):
		return '<Transfer: %s, Transfer Message: %s>' % (self.transferid, self.message)
