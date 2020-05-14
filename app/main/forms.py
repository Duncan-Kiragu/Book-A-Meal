from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SelectField,SubmitField
from wtforms.validators import Required,email

class AddOrder(FlaskForm):
    order_name = StringField('Blog title ', validators=[Required()])
    submit = SubmitField('Make Order')

class SubscriberForm(FlaskForm):
    username = StringField(validators=[Required()], render_kw={"placeholder": "Enter your name.."})
    email = StringField(validators=[Required()],render_kw={"placeholder":"Enter your email.."})
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself', validators=[Required()])
    submit = SubmitField('Submit')

class AddMenu(FlaskForm):
    title = StringField('Title')
    description =TextAreaField('Description')
    price =StringField('Price')
    submit = SubmitField('Submit')

