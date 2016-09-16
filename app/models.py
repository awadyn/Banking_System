from app import db

class User(db.Model):
	__tablename__ = 'users'

	userid = db.Column(db.String(22), primary_key=True)
	password = db.Column(db.String(16))
	balance = db.Column(db.Integer)
	temp_balance = db.Column(db.Integer)

#	outgoing_transfers = db.relationship('Transfer', foreign_keys=[Transfer.sourceid], backref='source_user', lazy='dynamic')
#	incoming_transfers = db.relationship('Transfer', foreign_keys=[Transfer.destid], backref='destination_user', lazy='dynamic')
	
	def __repr__(self):
		return '<User %s>' % (self.userid)



class Transfer(db.Model):
	__tablename__ = 'transfers'

	transferid = db.Column(db.String(16), primary_key=True)
	date = db.Column(db.DateTime, index=True)
	sourceid = db.Column(db.String(16), db.ForeignKey('users.userid'))
	destid = db.Column(db.String(16), db.ForeignKey('users.userid'))
	amount = db.Column(db.Integer, index=True)

	source = db.relationship('User', foreign_keys=[sourceid])
	dest = db.relationship('User', foreign_keys=[destid])

	def __repr__(self):
		return '<Transfer %r>' % (self.transferid)
