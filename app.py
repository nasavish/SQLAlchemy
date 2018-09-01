from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

@app.route('/')
def home():
    return 'you are at the homepage'


@app.route('/api/v1.0/stations')
def stations_route():
    stations = session.query(Station.station).all()
    stations_list = []
    for item in stations:
        stations_list.append(item[0])

    return jsonify(stations_list)
    
@app.route('/api/v1.0/tobs')
def tobs_route():
    prev_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.tobs).filter(Measurement.date > prev_date).all()
    temp_list = []
    for item in tobs:
        temp_list.append(item[0])

    return jsonify(temp_list)

@app.route('/api/v1.0/precipitation')
def precip_route():
    prev_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > prev_date).all()
   
    return jsonify(results)

@app.route('/api/v1.0/<start>')


@app.route('/api/v1.0/<start>/<end>')
def date_range(start, end):
    prev_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # def calc_temps(start_date, end_date):
        
    results = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
        .filter(Measurement.date >= '2012-02-28').filter(Measurement.date <= '2012-03-05').all())

    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True)