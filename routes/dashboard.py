from flask import Blueprint, render_template, session, redirect
from config import get_db_connection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Statistics
    cursor.execute("SELECT COUNT(*) total FROM patients")
    total_patients = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) total FROM doctors")
    total_doctors = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) total FROM appointments")
    total_appointments = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) total FROM rooms")
    total_rooms = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) total
        FROM rooms
        WHERE status='Occupied'
    """)
    occupied_rooms = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) total
        FROM admissions
        WHERE status='Admitted'
    """)
    admitted_patients = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) total
        FROM medicines
    """)
    total_medicines = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT IFNULL(SUM(total_amount),0) revenue
        FROM bills
    """)
    total_revenue = cursor.fetchone()["revenue"]

    # Today's appointments
    cursor.execute("""
        SELECT
            a.appointment_date,
            p.full_name AS patient_name,
            d.full_name AS doctor_name

        FROM appointments a
        JOIN patients p
        ON a.patient_id=p.patient_id

        JOIN doctors d
        ON a.doctor_id=d.doctor_id

        WHERE appointment_date=CURDATE()

        ORDER BY appointment_date
        LIMIT 5
    """)

    today_appointments = cursor.fetchall()

    # Low stock medicines
    cursor.execute("""
        SELECT
            medicine_name,
            stock_quantity

        FROM medicines

        WHERE stock_quantity<=20

        ORDER BY stock_quantity ASC

        LIMIT 5
    """)

    low_stock = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",

        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        admitted_patients=admitted_patients,
        total_medicines=total_medicines,
        total_revenue=total_revenue,

        today_appointments=today_appointments,
        low_stock=low_stock
    )