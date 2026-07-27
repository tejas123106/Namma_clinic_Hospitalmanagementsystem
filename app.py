from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from flask import Flask, render_template, request, redirect, session
from config import get_db_connection
from routes.patients import patients_bp
from routes.doctors import doctors_bp
from routes.appointments import appointments_bp
from routes.bills import bills_bp
from routes.rooms import rooms_bp
from routes.admissions import admissions_bp
from routes.medicines import medicines_bp
from routes.reports import reports_bp

app = Flask(__name__)
app.secret_key = "hospital_management_secret_key_2026"
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(doctors_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(bills_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(admissions_bp)
app.register_blueprint(medicines_bp)
app.register_blueprint(reports_bp)





if __name__ == "__main__":
    app.run(debug=True)