from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, validators


class RegistrationForm(FlaskForm):
    """Registration form for new users"""

    username = StringField('Username', [validators.Length(min=1, max=20)])
    password = PasswordField('Password', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1, max=20)])
    password = PasswordField('Password', [validators.DataRequired()])


class FeedbackForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    content = TextField('Content', [validators.DataRequired()])


# email - a not-nullable column that is unique and no longer than 50 characters.
# first_name - a not-nullable column that is no longer than 30 characters.
# last_name - a not-nullable column that is no longer than 30 characters.
