from app import app, db, models

db.session.remove()
db.drop_all()
