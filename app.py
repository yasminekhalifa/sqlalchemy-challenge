# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    date = dt.datetime(2016, 8, 23)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > date).all()
    dic_results = dict(results)
    return jsonify(dic_results)


@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'About' page...")
    active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()
    all_names = list(np.ravel(active_station))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'About' page...")
    date = dt.datetime(2016, 8, 23)
    observations = session.query(Measurement.tobs).\
    filter(Measurement.date > date).filter(Measurement.station == 'USC00519281').all()
    all_temp = list(np.ravel(observations))
    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'About' page...")
    search_term = start.split(" ")
    date = dt.datetime(int(search_term[0]), int(search_term[1]), int(search_term[2]))
    Max = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= date).filter(Measurement.station == 'USC00519281').all()
    Min = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= date).filter(Measurement.station == 'USC00519281').all()
    Avr = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= date).filter(Measurement.station == 'USC00519281').all()
    start_max = list(np.ravel(Max))
    start_min = list(np.ravel(Min))
    start_avr = list(np.ravel(Avr))

    return jsonify(start_max, start_min, start_avr)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    print("Server received request for 'About' page...")
    start_date = start.split(" ")
    s_date = dt.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = end.split(" ")
    e_date = dt.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    Max = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= s_date).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date <= e_date).all()
    Min = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= s_date).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date <= e_date).all()
    Avr = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= s_date).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date <= e_date).all()

    return (
        f"The maximum tempurature is {Max}<br/>"
        f"The minimum tempurature is {Min}<br/>"
        f"The average tempurature is {Avr}<br/>"
)

if __name__ == "__main__":
    app.run(debug=True)