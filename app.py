
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import os
import pandas as pd

database_path = os.path.join("Resources", "hawaii.sqlite")
engine = create_engine(f"sqlite:///{database_path}")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Init

app = Flask(__name__)


#Routes
@app.route("/")
def Home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "En la siguiente api incluir una fecha de inicio para realizar el análisis en formato YYYY-MM-DD<br/>"
        f"/api/v1.0/<start><br/>"
        "---------------<br/>"
        "En la siguiente api incluir una fecha de inicio y fin para realizar el análisis en formato YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Calculate the date 1 year ago 
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date = dt.datetime.strptime(recent_date, "%Y-%m-%d")
    search_date = last_date - dt.timedelta(days=365)
    
    prcp_base = (session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= search_date)
        .order_by(Measurement.date)
        .all()
    )

    return jsonify(prcp_base)

    session.close

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    st_number = session.query(Station.station, Station.name).all()

    return jsonify(st_number)
    session.close

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    active_stations = pd.DataFrame(session.query(Measurement.station).all()).value_counts()
    last_date = session.query(Measurement.date).filter(Measurement.station == active_stations.index[0][0])\
    .order_by(Measurement.date.desc()).first()[0]
    search_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    year_ago = search_date - dt.timedelta(days=365)

    station_data = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date >= year_ago,Measurement.station == active_stations.index[0][0])
        .order_by(Measurement.date)
        .all()
    )
    return jsonify(station_data)
    session.close

@app.route("/api/v1.0/<start>")
def start(start):
    """Date in format (YYYY-MM-DD)"""
    session = Session(engine)
    temperatures= (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    temps = []
    for min, avg, max in temperatures:
        temps_dict = {}
        temps_dict["min"] = temperatures[0][0]
        temps_dict["avg"] = temperatures[0][1]
        temps_dict["max"] = temperatures[0][2]
        temps.append(temps_dict)

    return jsonify(temps)
    
    session.close

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Date in format (YYYY-MM-DD)"""
    session = Session(engine)
    temperatures= (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date < end)
        .all()
    )
    temps = []
    for min, avg, max in temperatures:
        temps_dict = {}
        temps_dict["min"] = temperatures[0][0]
        temps_dict["avg"] = temperatures[0][1]
        temps_dict["max"] = temperatures[0][2]
        temps.append(temps_dict)

    return jsonify(temps)
    
    session.close


#Run
if __name__ == "__main__":
    app.run(debug=True)