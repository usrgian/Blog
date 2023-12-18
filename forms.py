
from flask_wtf import FlaskForm
from wtforms import  StringField, TextAreaField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField()
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password (Confirm)', validators=[DataRequired()])
    about_me = TextAreaField('Tell me about yourself (Optional)')
    submit = SubmitField('Register')

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    about_me = TextAreaField('About')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) #allowed files
    submit = SubmitField('Submit')
    
    
    