import sqlite3

DB_NAME = "medicine.db"

def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compartments(
        section_id TEXT PRIMARY KEY,
        medicine_name TEXT NOT NULL,
        medicine_type TEXT,
        servo_angle INTEGER,
        expiry_date TEXT,
        current_quantity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id TEXT,
        time TEXT,
        dosage INTEGER,
        before_after_food TEXT,
        water_ml INTEGER,
        FOREIGN KEY (section_id) REFERENCES compartments(section_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intake_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        actual_time TEXT,
        status TEXT,
        FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id)
    )
    """)

    conn.commit()
    conn.close()


def add_compartment(section_id, medicine_name, medicine_type, servo_angle, expiry_date, current_quantity):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO compartments
        VALUES(?,?,?,?,?,?)
    """, (section_id, medicine_name, medicine_type, servo_angle, expiry_date, current_quantity))

    conn.commit()
    conn.close()


def get_all_compartments():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM compartments")
    data = cursor.fetchall()

    conn.close()
    return data


def get_compartment_by_id(section_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM compartments WHERE section_id=?", (section_id,))
    data = cursor.fetchone()

    conn.close()
    return data

def get_schedule_by_id(schedule_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schedule WHERE schedule_id=?", (schedule_id,))
    data = cursor.fetchone()

    conn.close()
    return data

# NEW PART : UPDATE/EDIT & DELETE - 7.03.26

def delete_compartment(section_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM compartments WHERE section_id=?", (section_id,))

    conn.commit()
    conn.close()

def update_compartment(section_id, medicine_name, medicine_type, servo_angle, expiry_date, current_quantity):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE compartments
        SET medicine_name=?,
            medicine_type=?,
            servo_angle=?,
            expiry_date=?,
            current_quantity=?
        WHERE section_id=?
    """, (
        medicine_name,
        medicine_type,
        servo_angle,
        expiry_date,
        current_quantity,
        section_id
    ))

    conn.commit()
    conn.close()

# NEW PART : UPDATE/EDIT & DELETE - 7.03.26

#EDIT PART
def update_schedule(schedule_id, section_id, time, dosage, before_after_food, water_ml):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE schedule
        SET section_id=?,
            time=?,
            dosage=?,
            before_after_food=?,
            water_ml=?
        WHERE schedule_id=?
    """, (
        section_id,
        time,
        dosage,
        before_after_food,
        water_ml,
        schedule_id
    ))

    conn.commit()
    conn.close()

# DELETE PART
def delete_schedule(schedule_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM schedule WHERE schedule_id=?", (schedule_id,))

    conn.commit()
    conn.close()





def add_schedule(section_id, time, dosage, before_after_food, water_ml):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO schedule
        (section_id, time, dosage, before_after_food, water_ml)
        VALUES (?,?,?,?,?)
    """, (section_id, time, dosage, before_after_food, water_ml))

    conn.commit()
    conn.close()


def get_schedule_by_time(current_time):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schedule WHERE time=?", (current_time,))
    data = cursor.fetchall()

    conn.close()
    return data


def log_intake(schedule_id, actual_time, status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO intake_log
        (schedule_id, actual_time, status)
        VALUES (?,?,?)
    """, (schedule_id, actual_time, status))
    
    conn.commit()
    conn.close()


def clear_compartments():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM compartments")

    

    print("All compartments deleted")

    conn.commit()
    conn.close()

def reduce_quantity(section_id, dosage):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE compartments
        SET current_quantity = current_quantity - ?
        WHERE section_id = ?
    """, (dosage, section_id))

    conn.commit()
    conn.close()