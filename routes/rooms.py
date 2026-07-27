from flask import Blueprint, render_template, request, redirect, session, flash
from config import get_db_connection

rooms_bp = Blueprint("rooms", __name__)


@rooms_bp.route("/rooms")
def rooms():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        cursor.execute("""
            SELECT *
            FROM rooms
            WHERE room_number LIKE %s
               OR room_type LIKE %s
               OR status LIKE %s
            ORDER BY room_id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM rooms
            ORDER BY room_id DESC
        """)

    rooms = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "rooms/list.html",
        rooms=rooms,
        search=search
    )

@rooms_bp.route("/rooms/add")
def add_room():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("rooms/add.html")


@rooms_bp.route("/add_room", methods=["POST"])
def save_room():

    if "user_id" not in session:
        return redirect("/login")

    room_number = request.form["room_number"]
    room_type = request.form["room_type"]
    floor_number = request.form["floor_number"]
    daily_charge = request.form["daily_charge"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rooms
        (room_number, room_type, floor_number, daily_charge, status)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        room_number,
        room_type,
        floor_number,
        daily_charge,
        status
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Room added successfully!", "success")

    return redirect("/rooms")

@rooms_bp.route("/rooms/edit/<int:id>")
def edit_room(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM rooms WHERE room_id=%s",
        (id,)
    )

    room = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("rooms/edit.html", room=room)


@rooms_bp.route("/rooms/update/<int:id>", methods=["POST"])
def update_room(id):

    if "user_id" not in session:
        return redirect("/login")

    room_number = request.form["room_number"]
    room_type = request.form["room_type"]
    floor_number = request.form["floor_number"]
    daily_charge = request.form["daily_charge"]
    status = request.form["status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE rooms
        SET room_number=%s,
            room_type=%s,
            floor_number=%s,
            daily_charge=%s,
            status=%s
        WHERE room_id=%s
    """, (
        room_number,
        room_type,
        floor_number,
        daily_charge,
        status,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Room updated successfully!", "success")

    return redirect("/rooms")

@rooms_bp.route("/rooms/delete/<int:id>")
def delete_room(id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM rooms WHERE room_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Room deleted successfully!", "success")

    return redirect("/rooms")