from flask import Blueprint, render_template, request, redirect, session, flash
from config import get_db_connection

admissions_bp = Blueprint("admissions", __name__)

@admissions_bp.route("/admissions")
def admissions():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT
                a.*,
                p.full_name AS patient_name,
                r.room_number,
                d.full_name AS doctor_name
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN rooms r ON a.room_id = r.room_id
            JOIN doctors d ON a.attending_doctor_id = d.doctor_id
            WHERE p.full_name LIKE %s
               OR r.room_number LIKE %s
               OR d.full_name LIKE %s
               OR a.status LIKE %s
            ORDER BY a.admission_id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
            SELECT
                a.*,
                p.full_name AS patient_name,
                r.room_number,
                d.full_name AS doctor_name
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN rooms r ON a.room_id = r.room_id
            JOIN doctors d ON a.attending_doctor_id = d.doctor_id
            ORDER BY a.admission_id DESC
        """)

    admissions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admissions/list.html",
        admissions=admissions,
        search=search
    )



@admissions_bp.route("/admissions/add")
def add_admission():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Patients
    cursor.execute("""
        SELECT patient_id, full_name
        FROM patients
        ORDER BY full_name
    """)
    patients = cursor.fetchall()

    # Doctors
    cursor.execute("""
        SELECT doctor_id, full_name
        FROM doctors
        ORDER BY full_name
    """)
    doctors = cursor.fetchall()

    # Only Available Rooms
    cursor.execute("""
        SELECT room_id, room_number
        FROM rooms
        WHERE status='Available'
        ORDER BY room_number
    """)
    rooms = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admissions/add.html",
        patients=patients,
        doctors=doctors,
        rooms=rooms
    )

@admissions_bp.route("/add_admission", methods=["POST"])
def save_admission():

    if "user_id" not in session:
        return redirect("/login")

    patient_id = request.form["patient_id"]
    room_id = request.form["room_id"]
    doctor_id = request.form["doctor_id"]
    admission_date = request.form["admission_date"]
    diagnosis = request.form["diagnosis"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert Admission
    cursor.execute("""
        INSERT INTO admissions
        (
            patient_id,
            room_id,
            attending_doctor_id,
            admission_date,
            diagnosis
        )
        VALUES (%s,%s,%s,%s,%s)
    """, (
        patient_id,
        room_id,
        doctor_id,
        admission_date,
        diagnosis
    ))

    # Occupy Room
    cursor.execute("""
        UPDATE rooms
        SET status='Occupied'
        WHERE room_id=%s
    """, (room_id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Patient admitted successfully!", "success")

    return redirect("/admissions")

@admissions_bp.route("/admissions/edit/<int:id>")
def edit_admission(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Current Admission
    cursor.execute("""
        SELECT *
        FROM admissions
        WHERE admission_id=%s
    """, (id,))

    admission = cursor.fetchone()

    # Patients
    cursor.execute("""
        SELECT patient_id, full_name
        FROM patients
        ORDER BY full_name
    """)
    patients = cursor.fetchall()

    # Doctors
    cursor.execute("""
        SELECT doctor_id, full_name
        FROM doctors
        ORDER BY full_name
    """)
    doctors = cursor.fetchall()

    # Rooms
    cursor.execute("""
        SELECT room_id, room_number
        FROM rooms
        ORDER BY room_number
    """)
    rooms = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admissions/edit.html",
        admission=admission,
        patients=patients,
        doctors=doctors,
        rooms=rooms
    )

@admissions_bp.route("/admissions/update/<int:id>", methods=["POST"])
def update_admission(id):

    if "user_id" not in session:
        return redirect("/login")

    patient_id = request.form["patient_id"]
    room_id = request.form["room_id"]
    doctor_id = request.form["doctor_id"]
    admission_date = request.form["admission_date"]
    diagnosis = request.form["diagnosis"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE admissions
        SET
            patient_id=%s,
            room_id=%s,
            attending_doctor_id=%s,
            admission_date=%s,
            diagnosis=%s
        WHERE admission_id=%s
    """, (
        patient_id,
        room_id,
        doctor_id,
        admission_date,
        diagnosis,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Admission updated successfully!", "success")

    return redirect("/admissions")

@admissions_bp.route("/admissions/discharge/<int:id>")
def discharge_patient(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT room_id
        FROM admissions
        WHERE admission_id=%s
    """, (id,))

    admission = cursor.fetchone()

    if admission:

        cursor.execute("""
            UPDATE admissions
            SET
                status='Discharged',
                discharge_date=CURDATE()
            WHERE admission_id=%s
        """, (id,))

        cursor.execute("""
            UPDATE rooms
            SET status='Available'
            WHERE room_id=%s
        """, (admission["room_id"],))

        conn.commit()

    cursor.close()
    conn.close()

    flash("Patient discharged successfully!", "success")

    return redirect("/admissions")

@admissions_bp.route("/admissions/delete/<int:id>")
def delete_admission(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT room_id, status
        FROM admissions
        WHERE admission_id=%s
    """, (id,))

    admission = cursor.fetchone()

    if admission:

        # If the patient is still admitted, free the room first
        if admission["status"] == "Admitted":
            cursor.execute("""
                UPDATE rooms
                SET status='Available'
                WHERE room_id=%s
            """, (admission["room_id"],))

        cursor.execute("""
            DELETE FROM admissions
            WHERE admission_id=%s
        """, (id,))

        conn.commit()

    cursor.close()
    conn.close()

    flash("Admission deleted successfully!", "success")

    return redirect("/admissions")