from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from portfo.models import User
from portfo import db

class RegisterForm(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired(), Length(max=20, min=4)])
  email = EmailField(label='Email', validators=[DataRequired(), Email()])
  password = PasswordField(label='Password', validators=[DataRequired()])
  confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField(label='Register')

  def validate_username(self, username):
    user = db.session.scalar(db.select(User).where(User.username==username.data))
    if user:
      raise ValidationError('That username is taken. Please choose different one!')
    
  def validate_email(self, email):
    user = db.session.scalar(db.select(User).where(User.email==email.data))
    if user:
      raise ValidationError('That email is taken. Please choose different one!')
    
class LoginForm(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=20)])
  password = PasswordField(label='Password', validators=[DataRequired()])
  remember = BooleanField(label='Remember Me')

  submit = SubmitField(label='Login')

class UpdateAccountForm(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=20)],
                         render_kw={'readonly':'readonly'})
  email = EmailField(label='Email', validators=[DataRequired(), Email()], render_kw={'readonly':'readonly'})
  fullname = StringField(label='Fullname')
  avatar = FileField(label='Update Profile Avatar', validators=[FileAllowed(['jpg', 'png', 'gif', 'jfif'])])

  submit = SubmitField(label='Update Account')

class TaskForm(FlaskForm):
  task = StringField(label='Task', validators=[DataRequired(), Length(min=4, max=50)], 
                     render_kw={'placeholder': 'Enter your Task'})
  
  submit = SubmitField(label='Add New Task')

class FriendProfileForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    avatar = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
