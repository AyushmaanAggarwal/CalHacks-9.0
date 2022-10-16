from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class OrganizeProtest(FlaskForm):
    title = StringField('Name your protest', validators=[DataRequired()])
    description = TextAreaField('Describe your protest. What and why are you protesting? Why should people care? What '
                                'should protestors bring? ', validators=[DataRequired(), Length(max=1000)])
    location = StringField('Where is your protest happening? Be specific.', validators=[DataRequired()])
    date = DateTimeField('When is your protest happening?', validators=[DataRequired()], format='%Y-%m-%d %H:%M', display_format='%Y-%m-%d %H:%M')
    submit = SubmitField('Create a new protest')


class UpdateProtest(FlaskForm):
    title = StringField('Re-Name your protest')
    description = TextAreaField('Describe your protest. What and why are you protesting? Why should people care? What '
                                'should protestors bring? ', validators=[Length(max=1000)])
    location = StringField('Change the location: ')
    date = DateTimeField('Change the date: ', format='%Y-%m-%d %H:%M', display_format='%Y-%m-%d %H:%M')
    submit = SubmitField('Update protest')

