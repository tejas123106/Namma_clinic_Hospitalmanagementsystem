from flask import Blueprint, render_template, request, redirect, session,flash
from config import get_db_connection

bills_bp = Blueprint("bills", __name__)


@bills_bp.route("/bills")
def bills():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            b.*,
            p.full_name AS patient_name
        FROM bills b
        JOIN patients p
            ON b.patient_id = p.patient_id
        ORDER BY b.bill_id DESC
    """)

    bills = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "bills/list.html",
        bills=bills
    )


@bills_bp.route("/bills/add")
def add_bill_page():

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
        SELECT appointment_id
        FROM appointments
        ORDER BY appointment_id
    """)
    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "bills/add.html",
        patients=patients,
        appointments=appointments
    )


@bills_bp.route("/bills/add", methods=["POST"])
def add_bill():

    if "user_id" not in session:
        return redirect("/login")

    patient_id = request.form["patient_id"]
    appointment_id = request.form["appointment_id"]

    consultation_fee = float(request.form["consultation_fee"])
    medicine_charge = float(request.form["medicine_charge"])
    lab_charge = float(request.form["lab_charge"])
    room_charge = float(request.form["room_charge"])
    other_charge = float(request.form["other_charge"])

    total_amount = (
        consultation_fee +
        medicine_charge +
        lab_charge +
        room_charge +
        other_charge
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bills
        (
            patient_id,
            appointment_id,
            consultation_fee,
            medicine_charge,
            lab_charge,
            room_charge,
            other_charge,
            total_amount
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        patient_id,
        appointment_id,
        consultation_fee,
        medicine_charge,
        lab_charge,
        room_charge,
        other_charge,
        total_amount
    ))

    conn.commit()

    cursor.close()
    conn.close()
    flash("bill generated successfully!", "success")

    return redirect("/bills")


@bills_bp.route("/bills/delete/<int:id>")
def delete_bill(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bills WHERE bill_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()
    flash("bill deleted successfully!", "success")

    return redirect("/bills")

@bills_bp.route("/bills/edit/<int:id>")
def edit_bill(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM bills
        WHERE bill_id=%s
    """, (id,))
    bill = cursor.fetchone()

    cursor.execute("""
        SELECT patient_id, full_name
        FROM patients
        ORDER BY full_name
    """)
    patients = cursor.fetchall()

    cursor.execute("""
        SELECT appointment_id
        FROM appointments
        ORDER BY appointment_id
    """)
    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "bills/edit.html",
        bill=bill,
        patients=patients,
        appointments=appointments
    )

@bills_bp.route("/bills/update/<int:id>", methods=["POST"])
def update_bill(id):

    if "user_id" not in session:
        return redirect("/login")

    patient_id = request.form["patient_id"]
    appointment_id = request.form["appointment_id"]

    consultation_fee = float(request.form["consultation_fee"])
    medicine_charge = float(request.form["medicine_charge"])
    lab_charge = float(request.form["lab_charge"])
    room_charge = float(request.form["room_charge"])
    other_charge = float(request.form["other_charge"])

    payment_status = request.form["payment_status"]

    total_amount = (
        consultation_fee +
        medicine_charge +
        lab_charge +
        room_charge +
        other_charge
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE bills
        SET
            patient_id=%s,
            appointment_id=%s,
            consultation_fee=%s,
            medicine_charge=%s,
            lab_charge=%s,
            room_charge=%s,
            other_charge=%s,
            total_amount=%s,
            payment_status=%s
        WHERE bill_id=%s
    """, (
        patient_id,
        appointment_id,
        consultation_fee,
        medicine_charge,
        lab_charge,
        room_charge,
        other_charge,
        total_amount,
        payment_status,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()
    flash("bill updated successfully!", "success")

    return redirect("/bills")

@bills_bp.route("/bills/invoice/<int:id>")
def invoice(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["role"] not in ["Admin", "Accountant"]:
        return "Access Denied", 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            b.*,
            p.full_name AS patient_name
        FROM bills b
        JOIN patients p
        ON b.patient_id = p.patient_id
        WHERE b.bill_id=%s
    """, (id,))

    bill = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "bills/invoice.html",
        bill=bill
    )