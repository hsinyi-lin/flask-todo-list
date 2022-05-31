from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()])
    password1 = PasswordField('密碼', validators=[DataRequired()])
    password2 = PasswordField('再次輸入密碼', validators=[DataRequired()])
    submit = SubmitField('Submit')