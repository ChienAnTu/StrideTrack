from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(max=50)
    ])
    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(max=50)
    ])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    submit = SubmitField("Login")
