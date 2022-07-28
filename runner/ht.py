from distutils.log import debug
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask_bootstrap import Bootstrap
import sys
app=Flask(__name__,template_folder='templates')


# Flask-Bootstrap requires this line
Bootstrap(app)

# the name of the database; add path if necessary
conn="mysql+pymysql://{0}:@{1}/{2}".format('root','localhost','monorail')


app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Train(db.Model):
    __tablename__ = 'trains'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    departure_time = db.Column(db.String)
    expected_at = db.Column(db.String)
    average_speed = db.Column(db.Integer)
    position = db.Column(db.String)
    route = db.Column(db.String)
class maintenance(db.Model):
    __tablename__ = 'maintenance'
    TR_ID = db.Column(db.Integer)
    schedule_ID  = db.Column(db.Integer, primary_key=True)
    maintenance_start_date = db.Column(db.String)
    maintenance_end_date = db.Column(db.String)
    new_TR_ID= db.Column(db.Integer)
class Trainhistory(db.Model):
    __tablename__ = 'train_history'
    History_ID=db.Column(db.Integer, primary_key=True)
    TR_ID = db.Column(db.Integer)
    TR_Status  = db.Column(db.String)
    Trip_Time = db.Column(db.String)
    Number_of_Trip = db.Column(db.Integer)
class Operator(db.Model):
    __tablename__ = 'operator'
    OP_ID=db.Column(db.Integer, primary_key=True)
    OP_username  = db.Column(db.String)
    OP_name = db.Column(db.String)
    OP_password = db.Column(db.Integer)
    Log_id=db.Column(db.Integer)
class login(db.Model):
    __tablename__ = 'logins'
    Login_ID=db.Column(db.Integer, primary_key=True)
    Login_Username  = db.Column(db.String)
    Login_Password = db.Column(db.Integer)
    Login_Time = db.Column(db.String)

@app.route('/')
def index():
    try:
        return render_template('home.html')
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error1:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
@app.route('/report')
def trainreport():
    try:
        trains = Train.query.order_by(Train.id).all()
        return render_template('TrainReport.html', trains=trains)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error2:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
@app.route('/maintenance')
def maintenancerep():
    try:
        maintenances = maintenance.query.order_by(maintenance.schedule_ID).all()
        return render_template('maintenance.html', maintenances=maintenances)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error3:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
@app.route('/Trainhistory')
def Trainhistoryrep():
    try:
        Trainhistorys = Trainhistory.query.order_by(Trainhistory.History_ID).all()
        return render_template('Trainhistory.html', Trainhistorys=Trainhistorys)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error4:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
@app.route('/operator')
def operatorrep():
    try:
        operators = Operator.query.order_by(Operator.OP_ID).all()
        return render_template('operator.html', operators=operators)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error5:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
@app.route('/login')
def loginrep():
    try:
        logins = login.query.order_by(login.Login_ID).all()
        return render_template('login.html', logins=logins)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error6:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')