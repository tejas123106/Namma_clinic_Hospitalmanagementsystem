from flask import Blueprint, render_template, request, redirect, session, flash
from config import get_db_connection

patients_bp = Blueprint("patients", __name__)



@patients_bp.route("/patients")
def patients():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE full_name LIKE %s
               OR phone LIKE %s
            ORDER BY patient_id DESC
        """, (f"%{search}%", f"%{search}%"))

    else:

        cursor.execute("""
            SELECT *
            FROM patients
            ORDER BY patient_id DESC
        """)

    patients = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "patients/list.html",
        patients=patients,
        search=search
    )


@patients_bp.route("/patients/add")
def patient_add():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("patients/add.html")


@patients_bp.route("/add_patient", methods=["POST"])
def add_patient():

    if "user_id" not in session:
        return redirect("/login")

    full_name = request.form["full_name"]
    gender = request.form["gender"]
    date_of_birth = request.form["date_of_birth"]
    blood_group = request.form["blood_group"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]
    emergency_contact = request.form["emergency_contact"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients
        (full_name, gender, date_of_birth, blood_group,
         phone, email, address, emergency_contact)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        full_name,
        gender,
        date_of_birth,
        blood_group,
        phone,
        email,
        address,
        emergency_contact
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/patients")


@patients_bp.route("/patients/edit/<int:id>")
def edit_patient(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id=%s",
        (id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    conn.close()
    

    return render_template("patients/edit.html", patient=patient)


@patients_bp.route("/patients/update/<int:id>", methods=["POST"])
def update_patient(id):

    if "user_id" not in session:
        return redirect("/login")

    full_name = request.form["full_name"]
    gender = request.form["gender"]
    date_of_birth = request.form["date_of_birth"]
    blood_group = request.form["blood_group"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]
    emergency_contact = request.form["emergency_contact"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET
            full_name=%s,
            gender=%s,
            date_of_birth=%s,
            blood_group=%s,
            phone=%s,
            email=%s,
            address=%s,
            emergency_contact=%s
        WHERE patient_id=%s
    """, (
        full_name,
        gender,
        date_of_birth,
        blood_group,
        phone,
        email,
        address,
        emergency_contact,
        id
    ))

    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash("Patient updated successfully!", "success")
    
    return redirect("/patients")


@patients_bp.route("/patients/delete/<int:id>")
def delete_patient(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE patient_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Patient deleted successfully!", "success")

    return redirect("/patients")