from wtforms import Form, StringField, PasswordField, validators,FileField

#form used on Register page
class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4,max=25)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

#form used on the Verification page
class VerificationForm(Form):
    diplome =FileField('Diplome')

#form used on the create Diplome page
class CreatediplomeForm(Form):
    matricule = StringField('Matricule', [validators.Length(min=1,max=50)])
    mention = StringField('Mention', [validators.Length(min=1,max=50)])


#form used to add student 

class AddstudentForm(Form):
    familyname = StringField('Family Name', [validators.Length(min=1,max=50)])
    lastname = StringField('Last Name', [validators.Length(min=1,max=50)])
    matricule = StringField('Matricule', [validators.Length(min=1,max=50)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    date = StringField('Date', [validators.Length(min=6,max=50)])
    place = StringField('Place Of Birth', [validators.Length(min=4,max=25)])
    major = StringField('Major', [validators.Length(min=4,max=25)])
    
    