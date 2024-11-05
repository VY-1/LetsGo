from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class Flight(FlaskForm):
    flight_number = StringField("Flight Number")
    flight_capacity = IntegerField("Flight Capacity")
    flight_origin = StringField("Origin")
    flight_destination = StringField("Destination")
    submit = SubmitField("Add Flight")