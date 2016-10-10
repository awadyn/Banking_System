import sys
import string
import uuid
import validators

######################		
##### Validators #####
######################

# validate id
def valid_id(userid, id_repr):
	error = ''
	if userid == None:
		error += id_repr + " Required"
	elif not isinstance(userid, basestring):
		error += id_repr + " Must be Instance of String"
	elif not validators.uuid(userid):
		error += "Invalid " + id_repr
	return error

# validate passwords
def valid_password(password, password_repr):
	error = ''
	if password == None:
		error += password_repr + " Required"
	elif not isinstance(password, basestring):
		error += password_repr + " Must be Instance of String"
	elif not validators.between(len(password), min=8, max=16):
		error += password_repr + " Length Must Be Between 8 and 16 Characters Long"
	return error

# validate amounts
def valid_amount(amount, amount_repr):
	error = ''
	if amount == None:
		error += amount_repr + " Required"
	elif type(amount) != int:
		error += amount_repr + " Must be Integer"
	elif not validators.between(amount, min=0, max=sys.maxint):
		error += "Invalid " + amount_repr
	return error

# validate registration
def valid_register_request(password, confirm_password):
	error = ''
	error += valid_password(password, "Password")
	if password != confirm_password:
		error += "Passwords Don't Match"
	return error

# validate user credentials
def valid_user_credentials(userid, password):
	error = ''
	error += valid_id(userid, "UserID")
	error += valid_password(password, "Password")
	return error

# validate balance check request
def valid_balance_request(userid, password):
	return valid_user_credentials(userid, password)

# validate transfers check request
def valid_transfers_request(userid, password):
	return valid_user_credentials(userid, password)

# validate create transfer request
def valid_create_transfer_request(sourceid, password, destid, amount):
	error = ''
	error += valid_id(sourceid, "SourceID")
	error += valid_password(password, "Password")
	error += valid_id(destid, "DestinationID")
	error += valid_amount(amount, "Amount")
	return error
	
# validate handle transfer request
def valid_handle_transfer_request(userid, password, transferid, approve):
	error = ''
	error += valid_id(userid, "UserID")
	error += valid_password(password, "Password")
	error += valid_id(transferid, "TransferID")
	if approve == None:
		error += "Approval Required"
	elif type(approve) != bool:
		error += "Approve Must be Boolean"
	return error

