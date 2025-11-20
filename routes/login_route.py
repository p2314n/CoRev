from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from . import mongo  # import mongo instance from __init__.py

login_bp = Blueprint("login_bp", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check in the same collection used for registration
        user = mongo.db.registrations.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            session["user"] = {
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "designation": user.get("other_designation") if user.get("designation") == "other" else user.get("designation"),
                "username": user.get("username")
            }
            return redirect(url_for("dashboard_bp.dashboard"))
        else:
            flash("❌ Invalid username or password!", "error")
            return redirect(url_for("login_bp.login"))

    return render_template("html/login.html")