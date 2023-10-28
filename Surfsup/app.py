# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurment = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Home Page route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/end<br/>"
    )

#ask number 2 
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the rain data from the most recent date to the last 12 months"""

    most_recent_date = session.query(Measurment.date).order_by(Measurment.date.desc()).first()

    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    data_query = session.query(Measurment.date,Measurment.prcp).\
    filter(Measurment.date >= year_ago_date).all()

    rain_data=[]
    for date, prcp in data_query:
        rain_dict= {}
        rain_dict["date"] = date
        rain_dict["precipitation"] = prcp
        
        rain_data.append(rain_dict)

    return jsonify(rain_data)


#ask number 3
@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of dates and temp for the most active station for a year"""
    stations_query = session.query(Station.station, Station.name).all()
    station_list = []
    for station, name in stations_query:
        station_dict = {}
        station_dict["station"]= station
        station_dict["name"]= name

        station_list.append(station_dict)

    return jsonify(station_list)

#ask number 4 
@app.route("/api/v1.0/tobs")
def tempdata():
    """Returns a list of all the stations"""

    most_recent_date = session.query(Measurment.date).order_by(Measurment.date.desc()).first()

    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    stat_temp_most_active = session.query(Measurment.date, Measurment.tobs).\
        filter(Measurment.station == 'USC00519281').\
            filter(Measurment.date >= year_ago_date).all()
    temp_data = []
    for date, tob in stat_temp_most_active:
        temp_dict = {}
        temp_dict["date"]= date
        temp_dict["Temperutare"]= tob

        temp_data.append(temp_dict)

    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)
