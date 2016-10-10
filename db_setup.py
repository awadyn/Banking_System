from app import app, db, models

import uuid
import datetime


uid_1 = str(uuid.uuid4())
uid_2 = str(uuid.uuid4())
tid_1 = str(uuid.uuid4())
tid_2 = str(uuid.uuid4())
tid_3 = str(uuid.uuid4())

print uid_1
print uid_2
print tid_1
print tid_2
print tid_3

db.create_all()

user_1 = models.User(userid=uid_1, password='1111111111', balance=0)
user_2 = models.User(userid=uid_2, password='2222222222', balance=0)

transfer_1 = models.Transfer(transferid=tid_1, sourceid=uid_1, destid=uid_2, amount=50, date=datetime.date.today(), message='first transfer')
transfer_2 = models.Transfer(transferid=tid_2, sourceid=uid_2, destid=uid_1, amount=150, date=datetime.date.today(), message='second transfer')
transfer_3 = models.Transfer(transferid=tid_3, sourceid=uid_1, destid=uid_2, amount=50, date=datetime.date.today(), message='third transfer')
		
db.session.add(user_1)
db.session.add(user_2)
db.session.add(transfer_1)
db.session.add(transfer_2)
db.session.add(transfer_3)
db.session.commit()


