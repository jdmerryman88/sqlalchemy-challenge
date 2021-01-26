import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
         f"/api/v1.0/<start>/<end>"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation numbers"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    precipitation_num = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["Rainfall"] = prcp
        precipitation_num.append(precipitation_dict)

    return jsonify(precipitation_num)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, Station.name).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365.24)

    session = Session(engine)
    

    results = session.query(Measurement.tobs).\
                filter(Measurement.station == 'USC00519281' ).\
                filter(Measurement.date >= year_ago).all()
    session.close()

    all_tobs = []
    for tobs in results:
        
        all_tobs.append(tobs)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    start_date = start.replace(" ","")

    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs).label("Lowest")).\
            filter(Measurement.date >= start_date).all()
    tmax = session.query(func.max(Measurement.tobs).label("Highest")).\
            filter(Measurement.date >= start_date).all()
    tavg = session.query(func.avg(Measurement.tobs).label("Average")).\
            filter(Measurement.date >= start_date).all()       

    
    session.close()

    return (
        f"The mininum temperature starting from {start_date} is {tmin[0]} <br/>"
        f"The maximum temperature starting from {start_date} is {tmax[0]} <br/>"
        f"The average temperature starting from {start_date} is {tavg[0]}"
        
    )


@app.route("/api/v1.0/<start>/<end>")
def range(start,end):
    start_date = start.replace(" ","")
    end_date = end.replace(" ","")
    ##start_date = dt.date(2015, 1, 1)
    ##end_date = dt.date(2016, 8, 20)
    
    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs).label("Lowest")).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tmax = session.query(func.max(Measurement.tobs).label("Highest")).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    tavg = session.query(func.avg(Measurement.tobs).label("Average")).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()       

    
    session.close()

    return (
        f"The mininum temperature starting in range {start_date} to {end_date} is {tmin[0]} <br/>"
        f"The maximum temperature starting range {start_date} to {end_date} is {tmax[0]} <br/>"
        f"The average temperature starting range {start_date} to {end_date} is {tavg[0]}"
        
    )



if __name__ == '__main__':
    app.run(debug=True)
