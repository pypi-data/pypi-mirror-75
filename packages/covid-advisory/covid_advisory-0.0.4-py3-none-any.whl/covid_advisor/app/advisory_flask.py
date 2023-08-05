from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api
from .covid_stats import COVID_Data
from .security import authenticate, identity
from .user_database import Users_DB
from .config import jwt_cfg


app = Flask(__name__)
app.secret_key = jwt_cfg['secret_key']

jwt = JWT(app, authenticate, identity)

@app.route('/covid', methods = ['POST'])
@jwt_required()
def covid_data():
    try:
        state = request.form.get('state')
        COVID_Tracker = COVID_Data(state)
        stateInfo,status = COVID_Tracker.get_StateData()
        if status !=200:
            return {"message":"No data returned, Probably invalid state:"+ state}, status
        state_data = {}

        state_data['Case Growth Rate'] = COVID_Tracker.getCaseGrowthRate()
        state_data['Mortality Rate'] = COVID_Tracker.getMortalityRate()
        state_data['Hospitalizaiton Rate'] = COVID_Tracker.getTotalHospitalizations()
        state_data['Recovery Rate'] = COVID_Tracker.getRecoveryRate()
        state_data['Advisory'] = COVID_Tracker.TravelAdvisory()   
        return state_data , 200
    except Exception as exp:
        return {"message":str(exp)}, 500

@app.route('/register', methods = ['POST'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    user_DB = Users_DB(username, password)
    user_DB.register()
    return "Register Was Successful"



