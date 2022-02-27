import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# function allows us to access and query our SQLite
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# reflect the database into our classes
Base = automap_base()

# Refelct the tables
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#  create a session link from Python to our database
session = Session(engine)

# define our Flask app
app = Flask(__name__)

# This is a special type of variable in Python. 
# Its value depends on where and how the code is run. 
# For example, if we wanted to import our app.py file into another 
# Python file named example.py, the variable __name__ would be set to example


@app.route("/")

# add the precipitation, stations, tobs, and temp routes 
# that we'll need for this module into our return statement. We'll use f-strings to display them 
def welcome():
    # When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. 
    # This convention signifies that this is version 1 of our application. 
    # This line can be updated to support future versions of the app as well.
    return(
    f"Welcome to the Climate Analysis API!<br/>"
    f"Available Routes:</br>" 
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/stations</br>"
    f"/api/v1.0/tobs</br>"
    f"/api/v1.0/temp/start/end</br>")

@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():

    # create a query that will allow us to get all of the stations
    results = session.query(Station.station).all()

    # We want to start by unraveling our results into a one-dimensional array. 
    # To do this, we want to use the function np.ravel(), with results as our parameter.
    stations = list(np.ravel(results))

    # to return the list as json we added stations=stations. 
    # This formats the list into JSON.More doc on Flask: here https://flask.palletsprojects.com/en/2.0.x/api/#flask.json.jsonify
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


def stats(start=None, end=None):

    # We'll start by just creating a list called sel
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Since we need to determine the starting and ending date, 
    # add an if-not statement to our code. This will help us accomplish 
    # a few things
    if not end:

        # query our database using the list that we just made. 
        # In the following code, take note of the asterisk in the query 
        # next to the sel list. Here the asterisk is used to 
        # indicate there will be multiple results for our query: minimum, average, and maximum temperatures
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    # calculate the temperature minimum, average, and maximum with the start and end dates
    # Use the sel list, which is simply the data points we need to collect
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)