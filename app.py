from flask import Flask, render_template, request, redirect
import database

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_compartment")
def add_compartment():
    return render_template("add_compartment.html")


@app.route("/insert_compartment", methods=["POST"])
def insert_compartment():

    section_id = request.form["section_id"]
    medicine_name = request.form["medicine_name"]
    medicine_type = request.form["medicine_type"]
    servo_angle = request.form["servo_angle"]
    expiry_date = request.form["expiry_date"]
    current_quantity = request.form["current_quantity"]

    database.add_compartment(
        section_id,
        medicine_name,
        medicine_type,
        servo_angle,
        expiry_date,
        current_quantity
    )

    return redirect("/view_compartment")


@app.route("/view_compartment")
def view_compartment():

    data = database.get_all_compartments()

    return render_template("view_compartment.html", data=data)


@app.route("/delete_compartment/<section_id>")
def delete_compartment(section_id):

    database.delete_compartment(section_id)

    return redirect("/view_compartment") 

@app.route("/edit_compartment/<section_id>")
def edit_compartment(section_id):

    data = database.get_compartment_by_id(section_id)

    return render_template("edit_compartment.html", data=data)

@app.route("/update_compartment", methods=["POST"])
def update_compartment():

    section_id = request.form["section_id"]
    medicine_name = request.form["medicine_name"]
    medicine_type = request.form["medicine_type"]
    servo_angle = request.form["servo_angle"]
    expiry_date = request.form["expiry_date"]
    current_quantity = request.form["current_quantity"]

    database.update_compartment(
        section_id,
        medicine_name,
        medicine_type,
        servo_angle,
        expiry_date,
        current_quantity
    )

    return redirect("/view_compartment")


@app.route("/add_schedule")
def add_schedule():
    return render_template("add_schedule.html")


@app.route("/insert_schedule", methods=["POST"])
def insert_schedule():

    section_id = request.form["section_id"]
    time = request.form["time"]
    dosage = request.form["dosage"]
    before_after_food = request.form["before_after_food"]
    water_ml = request.form["water_ml"]

    database.add_schedule(
        section_id,
        time,
        dosage,
        before_after_food,
        water_ml
    )

    return redirect("/view_schedule")


@app.route("/view_schedule")
def view_schedule():

    conn = database.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schedule")
    data = cursor.fetchall()

    conn.close()

    return render_template("view_schedule.html", data=data)

#NEW : EDIT AND DELETE PART ADDED - 7.03.2025

@app.route("/delete_schedule/<int:schedule_id>")
def delete_schedule(schedule_id):

    database.delete_schedule(schedule_id)

    return redirect("/view_schedule")


@app.route("/edit_schedule/<int:schedule_id>")
def edit_schedule(schedule_id):

    data = database.get_schedule_by_id(schedule_id)

    return render_template("edit_schedule.html", data=data)


@app.route("/update_schedule", methods=["POST"])
def update_schedule():

    schedule_id = request.form["schedule_id"]
    section_id = request.form["section_id"]
    time = request.form["time"]
    dosage = request.form["dosage"]
    before_after_food = request.form["before_after_food"]
    water_ml = request.form["water_ml"]

    database.update_schedule(
        schedule_id,
        section_id,
        time,
        dosage,
        before_after_food,
        water_ml
    )

    return redirect("/view_schedule")


if __name__ == "__main__":
    database.create_tables()
    app.run(debug=True)