from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, UUID, ValidationError
import sys


# validation 'factory'
# balance must be greater than zero
def valid_amount(min=0, max=-1):
	message = 'Balance must be a positive integer'
	def _valid_amount(form, field):
		amount = field.data
		if amount < min or max != -1 and amount > max:
			raise ValidationError(message)
	return _valid_amount
		


class RegisterForm(Form):
	password = PasswordField('password', validators = [InputRequired(), EqualTo('confirm_password', message='Passwords Must Match'), Length(min=8, max=16, message='Password length must be between 8 and 16 characters long.')])
	confirm_password = PasswordField('confirm_password', validators = [InputRequired()])


class BalanceForm(Form):
	userid = StringField('userid', validators = [InputRequired(), UUID(message='Invalid UUID')], default='User ID')
	password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=16, message='Password length must be between 8 and 16 characters long.')])


class TransfersForm(Form):
	userid = StringField('userid', validators = [InputRequired(), UUID(message='Invalid UUID')], default='User ID')
	password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=16, message='Password length must be between 8 and 16 characters long.')])


class CreateTransferForm(Form):
	sourceid = StringField('sourceid', validators = [InputRequired(), UUID(message='Invalid UUID')], default='User ID')
	password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=16, message='Password length must be between 8 and 16 characters long.')])
	destid = StringField('destid', validators = [InputRequired(), UUID(message='Invalid UUID')], default='Destination ID')
	amount = IntegerField('amount', validators = [InputRequired(), valid_amount(max=sys.maxint)], default=None)
	message = StringField('message', validators = [Length(max=30)], default='transfer message')

class HandleIncomingRequestForm(Form):
	userid = StringField('userid', validators = [InputRequired(), UUID(message='Invalid UUID')], default='User ID')
	password = PasswordField('password', validators = [InputRequired(), Length(min=8, max=16, message='Password length must be between 8 and 16 characters long.')])
	transferid = StringField('transferid', validators = [InputRequired(), UUID(message='Invalid UUID')], default='Transfer ID')
	approve = BooleanField('approve', validators = [InputRequired()], default=False)
