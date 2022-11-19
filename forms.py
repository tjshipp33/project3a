"""Form class declaration."""
import json;
import csv;

from datapackage import Package

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length



class StockForm(FlaskForm):
    """Generate Your Graph."""
    
    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS

    #f = open('nyse_listed.json')
    #data = json.load(f)
    #f.close()
    #print(tuple(data.items()))

    #lst=list(tuple(line) for line in csv.reader(open('nyse_listed.csv'))) 
    #print(lst)

    #For some reason, I could never get Python to recognize any files. I have tried both relative and absolute path.

    package = Package('https://datahub.io/core/nyse-other-listings/datapackage.json')
    print(package.resource_names)
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            print(resource.read())

    symbol = SelectField("Choose Stock Symbol",[DataRequired()],
        choices=[

            (package, package),
            ("IBM", "IBM"),
            ("GOOGL", "GOOGL"),
            #("lst", "lst"),
        ],      
    )

    chart_type = SelectField("Select Chart Type",[DataRequired()],
        choices=[
            ("1", "1. Bar"),
            ("2", "2. Line"),
        ],
    )

    time_series = SelectField("Select Time Series",[DataRequired()],
        choices=[
            ("1", "1. Intraday"),
            ("2", "2. Daily"),
            ("3", "3. Weekly"),
            ("4", "4. Monthly"),
        ],
    )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")



