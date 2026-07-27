from flask import Blueprint, render_template, request, redirect, session,flash
from config import get_db_connection

doctors_bp = Blueprint("doctors", __name__)


@doctors_bp.route("/doctors")
def doctors():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT *
            FROM doctors
            WHERE full_name LIKE %s
               OR specialization LIKE %s
            ORDER BY doctor_id DESC
        """, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("""
            SELECT *
            FROM doctors
            ORDER BY doctor_id DESC
        """)

    doctors = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "doctors/list.html",
        doctors=doctors,
        search=search
    )


@doctors_bp.route("/doctors/add")
def add_doctor_page():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "doctors/add.html",
        departments=departments
    )


@doctors_bp.route("/add_doctor", methods=["POST"])
def add_doctor():

    if "user_id" not in session:
        return redirect("/login")

    full_name = request.form["full_name"]
    gender = request.form["gender"]
    specialization = request.form["specialization"]
    qualification = request.form["qualification"]
    experience_years = request.form["experience_years"]
    phone = request.form["phone"]
    email = request.form["email"]
    department_id = request.form["department_id"]
    consultation_fee = request.form["consultation_fee"]
    joining_date = request.form["joining_date"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO doctors
        (
            full_name,
            gender,
            specialization,
            qualification,
            experience_years,
            phone,
            email,
            department_id,
            consultation_fee,
            joining_date,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        full_name,
        gender,
        specialization,
        qualification,
        experience_years,
        phone,
        email,
        department_id,
        consultation_fee,
        joining_date,
        status
    ))

    conn.commit()

    cursor.close()
    conn.close()
    flash("Patient added successfully!", "success")

    return redirect("/doctors")


@doctors_bp.route("/doctors/edit/<int:id>")
def edit_doctor(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM doctors WHERE doctor_id=%s",
        (id,)
    )
    doctor = cursor.fetchone()

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "doctors/edit.html",
        doctor=doctor,
        departments=departments
    )


@doctors_bp.route("/doctors/update/<int:id>", methods=["POST"])
def update_doctor(id):

    if "user_id" not in session:
        return redirect("/login")

    full_name = request.form["full_name"]
    gender = request.form["gender"]
    specialization = request.form["specialization"]
    qualification = request.form["qualification"]
    experience_years = request.form["experience_years"]
    phone = request.form["phone"]
    email = request.form["email"]
    department_id = request.form["department_id"]
    consultation_fee = request.form["consultation_fee"]
    joining_date = request.form["joining_date"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE doctors
        SET
            full_name=%s,
            gender=%s,
            specialization=%s,
            qualification=%s,
            experience_years=%s,
            phone=%s,
            email=%s,
            department_id=%s,
            consultation_fee=%s,
            joining_date=%s,
            status=%s
        WHERE doctor_id=%s
    """, (
        full_name,
        gender,
        specialization,
        qualification,
        experience_years,
        phone,
        email,
        department_id,
        consultation_fee,
        joining_date,
        status,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()
    flash("doctor updated successfully!", "success")

    return redirect("/doctors")


@doctors_bp.route("/doctors/delete/<int:id>")
def delete_doctor(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM doctors WHERE doctor_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()
    flash("doctor deleted successfully!", "success")

    return redirect("/doctors")