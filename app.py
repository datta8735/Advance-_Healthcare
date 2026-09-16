from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = "advanced-healthcare-demo-secret"
DB = os.path.join(os.path.dirname(__file__), "healthcare.db")

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, age INTEGER, gender TEXT, phone TEXT,
        email TEXT, address TEXT
    );
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, specialization TEXT, phone TEXT, email TEXT
    );
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, doctor_id INTEGER, date TEXT, time TEXT, status TEXT DEFAULT 'Scheduled'
    );
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, doctor_id INTEGER, medicine TEXT, dosage TEXT, notes TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = db()
    stats = {
        "patients": conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
        "doctors": conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0],
        "appointments": conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0],
        "prescriptions": conn.execute("SELECT COUNT(*) FROM prescriptions").fetchone()[0]
    }
    conn.close()
    return render_template("index.html", stats=stats)

@app.route("/patients", methods=["GET","POST"])
def patients():
    conn = db()
    if request.method == "POST":
        conn.execute("INSERT INTO patients(name,age,gender,phone,email,address) VALUES(?,?,?,?,?,?)",
                     (request.form["name"], request.form.get("age"), request.form.get("gender"),
                      request.form.get("phone"), request.form.get("email"), request.form.get("address")))
        conn.commit()
        flash("Patient added successfully.", "success")
        return redirect(url_for("patients"))
    rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("patients.html", patients=rows)

@app.route("/doctors", methods=["GET","POST"])
def doctors():
    conn = db()
    if request.method == "POST":
        conn.execute("INSERT INTO doctors(name,specialization,phone,email) VALUES(?,?,?,?)",
                     (request.form["name"], request.form.get("specialization"),
                      request.form.get("phone"), request.form.get("email")))
        conn.commit()
        flash("Doctor added successfully.", "success")
        return redirect(url_for("doctors"))
    rows = conn.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("doctors.html", doctors=rows)

@app.route("/appointments", methods=["GET","POST"])
def appointments():
    conn = db()
    if request.method == "POST":
        conn.execute("INSERT INTO appointments(patient_id,doctor_id,date,time,status) VALUES(?,?,?,?,?)",
                     (request.form["patient_id"], request.form["doctor_id"], request.form["date"],
                      request.form["time"], request.form.get("status","Scheduled")))
        conn.commit()
        flash("Appointment scheduled.", "success")
        return redirect(url_for("appointments"))
    patients = conn.execute("SELECT * FROM patients").fetchall()
    doctors = conn.execute("SELECT * FROM doctors").fetchall()
    rows = conn.execute("""
        SELECT a.*, p.name patient, d.name doctor
        FROM appointments a LEFT JOIN patients p ON p.id=a.patient_id
        LEFT JOIN doctors d ON d.id=a.doctor_id ORDER BY a.date DESC, a.time DESC
    """).fetchall()
    conn.close()
    return render_template("appointments.html", appointments=rows, patients=patients, doctors=doctors)

@app.route("/prescriptions", methods=["GET","POST"])
def prescriptions():
    conn = db()
    if request.method == "POST":
        conn.execute("INSERT INTO prescriptions(patient_id,doctor_id,medicine,dosage,notes) VALUES(?,?,?,?,?)",
                     (request.form["patient_id"], request.form["doctor_id"], request.form["medicine"],
                      request.form.get("dosage"), request.form.get("notes")))
        conn.commit()
        flash("Prescription saved.", "success")
        return redirect(url_for("prescriptions"))
    patients = conn.execute("SELECT * FROM patients").fetchall()
    doctors = conn.execute("SELECT * FROM doctors").fetchall()
    rows = conn.execute("""
        SELECT r.*, p.name patient, d.name doctor
        FROM prescriptions r LEFT JOIN patients p ON p.id=r.patient_id
        LEFT JOIN doctors d ON d.id=r.doctor_id ORDER BY r.id DESC
    """).fetchall()
    conn.close()
    return render_template("prescriptions.html", prescriptions=rows, patients=patients, doctors=doctors)

@app.route("/health")
def health():
    return {"status": "ok", "service": "Advanced Healthcare System"}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
