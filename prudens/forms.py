from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField ,SubmitField,BooleanField
from wtforms.validators import DataRequired ,Length,Email ,Regexp ,EqualTo,ValidationError
from email_validator import validate_email, EmailNotValidError

class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=25)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField('User Name', validators=[DataRequired(), Length(min=2, max=25)])
    field_of_study=StringField('Field of Study',validators=[DataRequired(), Length(min=5, max=50)])
    # Custom email validator to ensure it ends with ".edu"
    def edu_email(form, field):
        if not field.data.lower().endswith('.edu.eg'):
            raise ValidationError('Email must end with .edu.eg')

    email = StringField('Email', validators=[DataRequired(), Email(), edu_email])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_])[A-Za-z\\d@$!%*?&_]{8,32}$")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    linkedin_account = StringField('LinkedIn Account',validators=[DataRequired()])
    google_scholar_account = StringField('Google Scholar Account',validators=[DataRequired()])
    
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField( "Password",validators=[DataRequired() ])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")