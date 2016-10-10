from app import db, models


#####################
##### Verifiers #####
#####################

# verify user
def verified_user(userid, password):
	user = models.User.query.filter_by(userid=userid, password=password).first()
	if user == None:
		return False
	else:
		return True

# verify transfer destination
def verified_dest(userid):
	user = models.User.query.filter_by(userid=userid).first()
	if user == None:
		return False
	else:
		return True

# verify transfer
def verified_transfer(transferid, destid):
	transfer = models.Transfer.query.filter_by(transferid=transferid, destid=destid).first()
	if transfer == None:
		return False
	else:
		return True

