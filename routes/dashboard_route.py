# routes/dashboard_route.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from . import mongo  # uses the PyMongo instance from your package

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():

    user = session["user"]

    # Fetch all subjects from MongoDB
    subjects = list(mongo.db.subjects.find({}, {"_id": 0}).sort("name", 1))

    # Fetch average ratings for all subjects in one go from reviews collection
    agg = list(mongo.db.reviews.aggregate([
        {"$match": {"rating": {"$ne": None}}},
        {"$group": {"_id": "$subject_id", "avgRating": {"$avg": "$rating"}}}
    ]))

    # Create a lookup dictionary {subject_id: avg_rating}
    avg_lookup = {item["_id"]: round(item["avgRating"], 2) for item in agg}

    # Add average rating info to each subject
    for s in subjects:
        s["avg_rating"] = avg_lookup.get(s["id"], None)

    # Render dashboard
    return render_template("html/dashboard.html", subjects=subjects, user=user)