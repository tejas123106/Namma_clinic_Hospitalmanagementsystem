from flask import Blueprint, render_template, redirect, session,request,flash
from config import get_db_connection

medicines_bp = Blueprint("medicines", __name__)

@medicines_bp.route("/medicines")
def medicines():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT *
            FROM medicines
            WHERE medicine_name LIKE %s
               OR manufacturer LIKE %s
               OR category LIKE %s
            ORDER BY medicine_id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
            SELECT *
            FROM medicines
            ORDER BY medicine_id DESC
        """)

    medicines = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "medicines/list.html",
        medicines=medicines,
        search=search
    )

@medicines_bp.route("/medicines/add")
def add_medicine():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("medicines/add.html")

@medicines_bp.route("/medicines/add", methods=["POST"])
def save_medicine():

    if "user_id" not in session:
        return redirect("/login")

    medicine_name = request.form["medicine_name"]
    category = request.form["category"]
    manufacturer = request.form["manufacturer"]
    unit_price = request.form["unit_price"]
    stock_quantity = int(request.form["stock_quantity"])
    manufacture_date = request.form["manufacture_date"]
    expiry_date = request.form["expiry_date"]

    # Automatically determine status
    status = "Available" if stock_quantity > 0 else "Out of Stock"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medicines
        (
            medicine_name,
            category,
            manufacturer,
            unit_price,
            stock_quantity,
            manufacture_date,
            expiry_date,
            status
        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        medicine_name,
        category,
        manufacturer,
        unit_price,
        stock_quantity,
        manufacture_date,
        expiry_date,
        status
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Medicine added successfully!", "success")

    return redirect("/medicines")

@medicines_bp.route("/medicines/edit/<int:id>")
def edit_medicine(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM medicines
        WHERE medicine_id=%s
    """, (id,))

    medicine = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "medicines/edit.html",
        medicine=medicine
    )

@medicines_bp.route("/medicines/update/<int:id>", methods=["POST"])
def update_medicine(id):

    if "user_id" not in session:
        return redirect("/login")

    medicine_name = request.form["medicine_name"]
    category = request.form["category"]
    manufacturer = request.form["manufacturer"]
    unit_price = request.form["unit_price"]
    stock_quantity = int(request.form["stock_quantity"])
    manufacture_date = request.form["manufacture_date"]
    expiry_date = request.form["expiry_date"]

    status = "Available" if stock_quantity > 0 else "Out of Stock"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE medicines
        SET
            medicine_name=%s,
            category=%s,
            manufacturer=%s,
            unit_price=%s,
            stock_quantity=%s,
            manufacture_date=%s,
            expiry_date=%s,
            status=%s
        WHERE medicine_id=%s
    """, (
        medicine_name,
        category,
        manufacturer,
        unit_price,
        stock_quantity,
        manufacture_date,
        expiry_date,
        status,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Medicine updated successfully!", "success")

    return redirect("/medicines")

@medicines_bp.route("/medicines/delete/<int:id>")
def delete_medicine(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM medicines
        WHERE medicine_id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Medicine deleted successfully!", "success")

    return redirect("/medicines")