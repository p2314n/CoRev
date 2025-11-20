import re # Used for regular expression pattern matching (password validation)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from . import mongo  # import mongo from __init__.py

register_bp = Blueprint("register_bp", __name__)

# Main registration route — handles both GET (show form) and POST (submit form)
@register_bp.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
         # Collect form inputs
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        designation = request.form.get("designation")
        other_designation = request.form.get("other_designation")
        username = request.form.get("username")
        password = request.form.get("password")

        # Password validation
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?\":{}|<>]).{6,}$"
        if not re.match(password_pattern, password):
            flash("⚠️ Password must be at least 6 characters long, include one number and one special character.", "error")
            return redirect(url_for("register_bp.register"))

        # Check if username already exists
        existing_user = mongo.db.registrations.find_one({"username": username})
        if existing_user:
            flash("⚠️ Username already exists. Please choose another.", "error")
            return redirect(url_for("register_bp.register"))

        #  Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Prepare the user document for insertion
        entry = {
            "first_name": first_name,
            "last_name": last_name,
            "designation": designation,
            "other_designation": other_designation if designation == "other" else None,
            "username": username,
            "password": hashed_password
        }

        # Insert user details into the database
        mongo.db.registrations.insert_one(entry)

        flash(" Registration successful! Please log in.", "success")
        return redirect(url_for("login_bp.login"))

    return render_template("html/registration.html")