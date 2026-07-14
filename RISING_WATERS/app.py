from flask import Flask, render_template, request, redirect, session

from database import *
from model import predict_flood

app = Flask(__name__)
app.secret_key = "risingwaters"

create_tables()


# ---------------- Home ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- Register ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        register_user(name, email, password, role)

        return redirect("/login")

    return render_template("register.html")


# ---------------- Login ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user_id"] = user["id"]
            session["name"] = user["name"]

            return redirect("/dashboard")

        else:

            return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- Dashboard ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["name"]
    )


# ---------------- Prediction Page ----------------

@app.route("/Predict")
def Predict():

    if "user_id" not in session:

        return redirect("/login")

    return render_template("predict.html")


# ---------------- Prediction ----------------

@app.route("/predict", methods=["POST"])
def predict():

    temp = float(request.form["Temp"])
    humidity = float(request.form["Humidity"])
    cloud = float(request.form["Cloud Cover"])
    annual = float(request.form["ANNUAL"])
    jan = float(request.form["Jan-Feb"])
    mar = float(request.form["Mar-May"])
    jun = float(request.form["Jun-Sep"])
    oct = float(request.form["Oct-Dec"])
    avg = float(request.form["avgjune"])
    sub = float(request.form["sub"])

    values = [
        temp,
        humidity,
        cloud,
        annual,
        jan,
        mar,
        jun,
        oct,
        avg,
        sub
    ]

    # ML Prediction
    result, probability = predict_flood(values)

    # Save Prediction
    save_prediction(
        session["user_id"],
        temp,
        humidity,
        cloud,
        annual,
        jan,
        mar,
        jun,
        oct,
        avg,
        sub,
        "Flood" if result == 1 else "No Flood"
    )

    if result == 1:

        return render_template(
            "chance.html",
            probability=probability
        )

    return render_template(
        "no_chance.html",
        probability=probability
    )


# ---------------- Prediction History ----------------

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect("/login")

    history = get_history(session["user_id"])

    return render_template(
        "history.html",
        history=history
    )


# ---------------- Logout ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------- Run ----------------

if __name__ == "__main__":

    app.run(debug=True)