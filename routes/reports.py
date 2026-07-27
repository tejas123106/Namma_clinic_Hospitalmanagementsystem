from flask import Blueprint, render_template, session, redirect
from config import get_db_connection

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Patients
    cursor.execute("SELECT COUNT(*) AS total FROM patients")
    total_patients = cursor.fetchone()["total"]

    # Total Doctors
    cursor.execute("SELECT COUNT(*) AS total FROM doctors")
    total_doctors = cursor.fetchone()["total"]

    # Total Appointments
    cursor.execute("SELECT COUNT(*) AS total FROM appointments")
    total_appointments = cursor.fetchone()["total"]

    # Total Bills
    cursor.execute("SELECT COUNT(*) AS total FROM bills")
    total_bills = cursor.fetchone()["total"]

    # Total Revenue
    cursor.execute("SELECT IFNULL(SUM(total_amount),0) AS revenue FROM bills")
    total_revenue = cursor.fetchone()["revenue"]

    # Total Rooms
    cursor.execute("SELECT COUNT(*) AS total FROM rooms")
    total_rooms = cursor.fetchone()["total"]

    # Occupied Rooms
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM rooms
        WHERE status='Occupied'
    """)
    occupied_rooms = cursor.fetchone()["total"]

    # Available Rooms
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM rooms
        WHERE status='Available'
    """)
    available_rooms = cursor.fetchone()["total"]

    # Current Admissions
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM admissions
        WHERE status='Admitted'
    """)
    admitted_patients = cursor.fetchone()["total"]

    # Total Medicines
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM medicines
    """)
    total_medicines = cursor.fetchone()["total"]

    # Out of Stock Medicines
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM medicines
        WHERE status='Out of Stock'
    """)
    out_of_stock = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template(
        "reports/dashboard.html",

        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_bills=total_bills,
        total_revenue=total_revenue,

        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        available_rooms=available_rooms,

        admitted_patients=admitted_patients,

        total_medicines=total_medicines,
        out_of_stock=out_of_stock
    )