from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class RegisterForm(Form):
	password = StringField('password', validators = [DataRequired()])

