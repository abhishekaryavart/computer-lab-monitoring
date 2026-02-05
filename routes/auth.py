from flask import render_template, request, redirect, url_for, session, flash
from db.mongo import staff_col

def login():
    if request.method == "POST":
        staff_id = request.form.get("staff_id")
        password = request.form.get("password")

        user = staff_col.find_one({"_id": staff_id})

        if user and user["password"] == password:
            session["staff_id"] = staff_id
            session["staff_name"] = user.get("name", staff_id)
            session["role"] = user.get("role", "staff")
            flash("Login successful!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid Staff ID or Password", "error")
            return render_template("login.html")

    return render_template("login.html")

def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))
