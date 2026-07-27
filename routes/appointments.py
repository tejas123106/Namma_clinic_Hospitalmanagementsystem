from flask import Blueprint, render_template, request, redirect, session,flash
from config import get_db_connection

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.route("/appointments")
def appointments():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT a.*, p.full_name AS patient_name,
                   d.full_name AS doctor_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE p.full_name LIKE %s
               OR d.full_name LIKE %s
               OR a.status LIKE %s
            ORDER BY a.appointment_id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
            SELECT a.*, p.full_name AS patient_name,
                   d.full_name AS doctor_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_id DESC
        """)

    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "appointments/list.html",
        appointments=appointments,
        search=search
    )


@appointments_bp.route("/appointments/add")
def add_appointment_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT patient_id, full_name
        FROM patients
        ORDER BY full_name
    """)
    patients = cursor.fetchall()

    cursor.execute("""
        SELECT doctor_id, full_name
        FROM doctors
        ORDER BY full_name
    """)
    doctors = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "appointments/add.html",
        patients=patients,
        doctors=doctors
    )


@appointments_bp.route("/appointments/add", methods=["POST"])
def add_appointment():

    if "user_id" not in session:
        return redirect("/login")

    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    reason = request.form["reason"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            reason,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
    """, (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason,
        status
    ))

    conn.commit()

    cursor.close()
    conn.close()
    flash("appointment scheduled successfully!", "success")

    return redirect("/appointments")


@appointments_bp.route("/appointments/edit/<int:id>")
def edit_appointment(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM appointments
        WHERE appointment_id = %s
    """, (id,))
    appointment = cursor.fetchone()

    cursor.execute("""
        SELECT patient_id, full_name
        FROM patients
        ORDER BY full_name
    """)
    patients = cursor.fetchall()

    cursor.execute("""
        SELECT doctor_id, full_name
        FROM doctors
        ORDER BY full_name
    """)
    doctors = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "appointments/edit.html",
        appointment=appointment,
        patients=patients,
        doctors=doctors
    )


@appointments_bp.route("/appointments/update/<int:id>", methods=["POST"])
def update_appointment(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] not in ["Admin", "Receptionist", "Doctor"]:
        return "Access Denied", 403

    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    reason = request.form["reason"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE appointments
        SET
            patient_id=%s,
            doctor_id=%s,
            appointment_date=%s,
            appointment_time=%s,
            reason=%s,
            status=%s
        WHERE appointment_id=%s
    """, (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason,
        status,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()
    flash("Appointment updated successfully!", "success")

    return redirect("/appointments")


@appointments_bp.route("/appointments/delete/<int:id>")
def delete_appointment(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM appointments WHERE appointment_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()
    flash("Appointment deleted successfully!", "success")

    return redirect("/appointments")