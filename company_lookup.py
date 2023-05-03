from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, SelectMultipleField, SelectField, RadioField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError

companyNames = []

with open('static/data/listing_status.csv', 'r') as file:
    for line in file:
        if line.strip():
            l = line.rstrip().split(",")
            list = []
            list.append(l[0])
            list.append(l[1])
            myTuple = tuple(list)
            companyNames.append(myTuple)


class Lookup(FlaskForm):
    name = SelectField("Pick a company", choices=companyNames)
    purpose = RadioField(u'Pick what information you want displayed',
                         choices=[('General Overview', 'General Overview'),
                                #   ('Divident Income', 'Divident Income'),
                                  ('Stock History', 'Stock History')],
                         validators=[InputRequired(message="You Have To Pick An Option")])
    submit = SubmitField("Submit")


class SignUp(FlaskForm):
    name = StringField("Name", validators=[
                       InputRequired(message="You have to enter your name")])

    email = StringField("Email", validators=[
                        InputRequired(message="You have to enter your email")])

    bank = StringField("Bank", validators=[
                       InputRequired(message="You have to enter bank name")])

    address = StringField("Address", validators=[
                          InputRequired(message="You have to enter your address")])

    state = StringField("State", validators=[
                        InputRequired(message="You have to enter your state")])
    
    password = StringField("Password", validators=[
                        InputRequired(message="You have to enter your password")])
    
    confirmPassword = StringField("Confirm Password", validators=[
                        InputRequired(message="You have to enter your password")])

    submit = SubmitField("Submit")
    
class Login(FlaskForm):
    email = StringField("Email")
    
    password = StringField("Password")
    
    submit = SubmitField("Submit")
    
    signup = SubmitField("Sign Up")


class BankTransfer(FlaskForm):
    amount = FloatField("Amount", validators=
                        [InputRequired(message="You have to enter amount of money you want to transfer")])
    
    submit = SubmitField("Submit")
    
class BuyShares(FlaskForm):
    name = SelectField("Pick a company", choices=companyNames)

    submit = SubmitField("Submit")

    # investmentAmount = IntegerField("Investment Amount", validators=
                        # [InputRequired(message="You have to enter amount of money you would like to invest in the company")])

    numberOfShares = IntegerField("Number of Shares", validators=
                        [InputRequired(message="You have to enter a valid amount of share you would like to purchase")])

# class AddToHoldings(FlaskForm):
#     purchaseAmount = IntegerField("Amount", validators=
#                         [InputRequired(message="You have to enter amount of money you want to invest in the company")])

#     Submit = SubmitField("Submit")
