"""`main` is the top level module for your Flask application."""

# Visualization Byte Version 1
# 
# Copyright 1/2016 Jennifer Mankoff
#
# Licensed under GPL v3 (http://www.gnu.org/licenses/gpl.html)
#

# standard imports (same as other bytes)
# Imports -- similar to explore byte
import os
import jinja2
import webapp2
import logging
import json
import urllib
from datetime import datetime
#from googleapiclient.discovery import build

#import MySQLdb
#import math
#import httplib2
from apiclient.discovery import build
#import numpy
#from django.utils import simplejson

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyCL67cC-KjGfKvejisBrvyi1Yd-WjOVmT0'

# This is the table id for the fusion table
TABLE_ID = '1vtO2Jnos9vLO3mp740L1XP1DIPyy2yV4OEuNtAMb'

# This API key is provided by google as described in the tutorial
#API_KEY = 'AIzaSyCpZ1iLD_Id7epHtnkEgAYTXsk2uBUtGkk'

# This is the table id for the fusion table
#TABLE_ID = '1ymz3EtGdi4qKGMl5AxEFXtTlgk3tKi8iCpjTzvM'


# This uses discovery to create an object that can talk to the 
# fusion tables API using the developer key
service = build('fusiontables', 'v1', developerKey=API_KEY)

# This is the default columns for the query
query_cols = []
query_animals = ['DOG']

# Import the Flask Framework
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    data = get_all_data()
    columns = data['columns']
    #logging.info(columns)
    rows = data['rows']
    
    # specify the ages we will search for
    age_mapping = {u'Infant - Younger than 6 months':'<6mo',
                   u'Youth - Younger than 1 year':'6mo-1yr',
                   u'Older than 1 year':'1yr-6yr',
                   u'Older than 7 years':'>7yr',
                   u'':'Unspecified',}
    # create an 'empty' array storing the number of dogs in each outcome
    
    # specify the outcomes we will search for 
    outcomes = ['Adopted', 'Euthanized', 'Foster', 'Returned to Owner', 'Transferred to Rescue Group', 'Other' ]
    ages = ['<6mo', '6mo-1yr', '1yr-6yr', '>7yr', 'Unspecified']
    #count = {}
    # total_by_age = {}
    # age_by_outcome = {}
    # logging.info(age_by_outcome)
    
	
    # for age in ages:
        # outcome_vals = {'Age':age}
		# #logging.error(outcome_vals)
        # #count = {'total': count} 
        # #count[age] = 0
        # #total_by_age[age] = count
        # #logging.error(total_by_age)
        # for outcome in outcomes:
            # outcome_vals[outcome]= 0
            # #logging.error(outcome_vals)
        # age_by_outcome[age] = outcome_vals
        # #count[age] = 0
        # logging.error(age_by_outcome)
        # #logging.error(count)
	# #logging.info(age_by_outcome)   
    
    duration_by_age = {}
    
    for age in ages:
        inner_dict = {'Age': age}
        inner_dict['count']=0
        inner_dict['duration']=0
        duration_by_age[age] = inner_dict
        #duration_by_age[age]=dict1
	logging.error(duration_by_age)
		
    query = "SELECT DISTINCT Zip_Where_Found FROM TABLE_ID"
    logging.error(query)
	
    # find the column id for ages
    ageid = columns.index(u'Estimated_Age')
    
    # find the column id for outcomes
    outcomeid = columns.index(u'OutcomeType')
    
	# find column id for indates and outdates
    intakeid = columns.index(u'Intake_Date')
    outid = columns.index(u'OutcomeDate')
	
    date_format = "%m/%d/%Y"
    duration = []
    total_duration_by_age = 0
	
     
        #logging.info(duration)
        
        #logging.info(duration)
    duration_sum = {}
    number_by_age = {}    
    
    #num_days = {'count':0}
	
	#duration_by_age = {'Age': age{}
    
    
    
            
    for row in rows :
        age = age_mapping[row[ageid]]
        InDate = row[intakeid]
        a = datetime.strptime(InDate, date_format)
        OutDate = row[outid]
        b= datetime.strptime(OutDate, date_format)
        delta = b - a
        duration = delta.days
        duration_by_age[age]['count'] += 1
        duration_by_age[age]['duration'] += duration
    logging.error(duration_by_age[age]['count'])
    logging.error(duration_by_age[age]['duration'])
    logging.error(duration_by_age)
    
    #zipped = zip(InDate, OutDate)
    #logging.info(zipped)
    	#date_for_duration[InDate][OutDate] += 1
        #data.append(date_for_duration[row])
	#logging.info(test)
    # loop through each row
    #total[] = 0
	
	
    # for row in rows: 
        # # get the age of the dog in that row
        # age = age_mapping[row[ageid]]
        # #logging.warning(age_mapping[row[ageid]])
        # # get the outcome for the dog in that row
        # outcome = row[outcomeid]
		
        # if age not in ages: age = 'Unspecified'
        # if outcome not in outcomes: outcome = 'Other'
		
        # age_by_outcome[age][outcome] += 1
        #count[age] +=1
		
        #logging.error(count)
        #logging.warning(age_by_outcome[age])
        #logging.info(age_by_outcome[age][outcome])
	

    		
        
        # average_duration_by_age = total_duration_by_age/count
    
    data = duration_by_age
    logging.info(data)
    # for age in ages:
        # logging.info("appending " + age)
        # #logging.info(age_by_outcome[age])
        # #data.append(age_by_outcome[age])
        # #data.append(count[age])
        # #logging.info(count[age])
    # logging.warning(data)
    
    # add it to the context being passed to jinja
    variables = {'data':data}
    
    # and render the response
    template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    return template.render(variables)

@app.route('/about')
def about():
    template = JINJA_ENVIRONMENT.get_template('templates/about.html')
    return template.render()


@app.route('/quality')
def quality():
    template = JINJA_ENVIRONMENT.get_template('templates/quality.html')
    return template.render()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

# collect the data from google fusion tables
# pass in the name of the file the data should be stored in
def get_all_data():
    """ collect data from the server. """
    
    # open the data stored in a file called "data.json"
    try:
        fp = open("data/data.json")
        response = simplejson.load(fp)
        # but if that file does not exist, download the data from fusiontables
    except IOError:
        logging.info("failed to load file")
        service = build('fusiontables', 'v1', developerKey=API_KEY)
        query = "SELECT * FROM " + TABLE_ID + " WHERE  Animal_Type = 'DOG'"
        response = service.query().sql(sql=query).execute()
        
    return response