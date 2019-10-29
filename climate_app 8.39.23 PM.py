import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta
from datetime import date
from flask import Flask , jsonify

# Connecting to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)

Base = automap_base()
Base.prepare( engine , reflect = True)
# creating refelection classes of tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#creating the app

app = Flask(__name__)


@app.route ("/")
def welcome ():
    return (
        f" Welcome to Climate API ! <br/>"
        f"Available routes : <br/>"
        f" /api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend"
    )

@app.route ("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
     
    prcp_dict = dict(results)


    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query( Station.station).all()
    results_list = list(np.ravel(results))

    session.close
    return jsonify(results_list)

@app.route("/api/v1.0/tobs")
def temp ():
    session = Session(engine)
    max_date = session.query(func.max(Measurement.date)).all()[0][0]
    year = int(max_date[0:4])
    month = int(max_date[5:7])
    day= int(max_date[8:])
    last_date = date(year,month,day)
    query_date = last_date - timedelta(days=365)
    results = session.query( Measurement.tobs).filter(Measurement.date >= query_date, Measurement.date <=last_date ).all()

    session.close
    return jsonify(results)

@app.route("/api/v1.0/start")
def tempstart ():
    session = Session (engine)

    #st_dt = session.query(func.min(Measurement.date)).all() 
    start_date = session.query(func.min(Measurement.date)).all()[0][0]

    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    temp_lstuple = session.query(*sel).filter(Measurement.date >= start_date).all()

    session.close()

    temp_pram1_list = list(np.ravel(temp_lstuple))
    temp_list =[]
    for t in temp_lstuple:
        temp_dict = {}
        temp_dict["Min Temp after Start Date 2010-01-01"] = temp_pram1_list[0]
        temp_dict["Avg Temp after Start Date 2010-01-01"] = temp_pram1_list[1]
        temp_dict["Max Temp after Start Date 2010-01-01"] = temp_pram1_list[2]
        temp_list.append(temp_dict)
    return jsonify(temp_list)

    
@app.route("/api/v1.0/startend")
def tempstartend ():
    session = Session (engine)
    #st_dt = session.query(func.min(Measurement.date)).all() 
    start_date = session.query(func.min(Measurement.date)).all()[0][0]
    date_format = date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:]))
    end_date = date_format + timedelta(weeks = 60)
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    temp_lstuple = session.query(*sel).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()

    temp_pram1_list = list(np.ravel(temp_lstuple))

    temp_list =[]
    for t in temp_lstuple:
        temp_dict = {}
        temp_dict["Min Temp between 2010-01-01 and 2011-02-25"] = temp_pram1_list[0]
        temp_dict["Avg Temp between 2010-01-01 and 2011-02-25"] = temp_pram1_list[1]
        temp_dict["Max Temp between 2010-01-01 and 2011-02-25"] = temp_pram1_list[2]
        temp_list.append(temp_dict)

    return jsonify(temp_list)



if __name__ =="__main__":
    app.run(debug=True)