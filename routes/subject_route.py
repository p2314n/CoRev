from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from . import mongo
from datetime import datetime

subject_bp = Blueprint("subject_bp", __name__, url_prefix="/subject")

# -------------------------
# Subject Detail Page
# -------------------------
@subject_bp.route("/<subject_id>")
def detail(subject_id):
    # Fetch subject from MongoDB
    subject = mongo.db.subjects.find_one({"id": subject_id}, {"_id": 0})
    if not subject:
        abort(404)

    #  Fetch all reviews for this subject
    reviews = list(mongo.db.reviews.find({"subject_id": subject_id}).sort("created_at", -1))

    #  Check if current user has already reviewed
    user_review = None
    if "user" in session:
        username = session["user"].get("username")
        user_review = mongo.db.reviews.find_one({
            "subject_id": subject_id,
            "user_username": username
        })

    # Compute average rating (only for non-null ratings)
    agg = list(mongo.db.reviews.aggregate([
        {"$match": {"subject_id": subject_id, "rating": {"$ne": None}}},
        {"$group": {"_id": "$subject_id", "avgRating": {"$avg": "$rating"}, "count": {"$sum": 1}}}
    ]))

    avg_rating = round(agg[0]["avgRating"], 2) if agg else None
    review_count = agg[0]["count"] if agg else 0

    return render_template(
        "html/subject.html",
        subject=subject,
        reviews=reviews,
        avg_rating=avg_rating,
        review_count=review_count,
        user_review=user_review
    )


# -------------------------
# Add / Update Review Route
# -------------------------
@subject_bp.route("/<subject_id>/review", methods=["POST"])
def add_review(subject_id):
    # Check if subject exists in MongoDB
    subject = mongo.db.subjects.find_one({"id": subject_id})
    if not subject:
        abort(404)

    #  Require login
    if "user" not in session:
        flash("Please log in to leave a review.", "error")
        return redirect(url_for("login_bp.login"))

    #  Get rating and text safely
    rating_input = request.form.get("rating")
    review_text = (request.form.get("review") or "").strip()

    try:
        rating = int(rating_input) if rating_input else None
        if rating is not None and (rating < 1 or rating > 5):
            raise ValueError
    except ValueError:
        flash("⚠️ Rating must be between 1 and 5.", "error")
        return redirect(url_for("subject_bp.detail", subject_id=subject_id))

    if not review_text and rating is None:
        flash("You didn’t provide a review or rating — that’s okay!", "info")
        return redirect(url_for("subject_bp.detail", subject_id=subject_id))

    #  User info
    user = session["user"]
    username = user.get("username")
    designation = user.get("designation", "Member")
    user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or username

    # Check existing review
    existing_review = mongo.db.reviews.find_one({
        "subject_id": subject_id,
        "user_username": username
    })

    review_doc = {
        "subject_id": subject_id,
        "rating": rating,
        "review": review_text if review_text else None,
        "user_name": user_name,
        "user_username": username,
        "designation": designation,
        "updated_at": datetime.utcnow()
    }

    if existing_review:
        mongo.db.reviews.update_one(
            {"_id": existing_review["_id"]},
            {"$set": review_doc}
        )
        flash("✅ Your review has been updated.", "review")
    else:
        review_doc["created_at"] = datetime.utcnow()
        mongo.db.reviews.insert_one(review_doc)
        flash("✅ Thank you! Your feedback has been submitted.", "review")

    return redirect(url_for("subject_bp.detail", subject_id=subject_id))


# -------------------------
# Delete Review Route
# -------------------------
@subject_bp.route("/<subject_id>/review/delete", methods=["POST"])
def delete_review(subject_id):
    if "user" not in session:
        flash("Please log in to delete your review.", "error")
        return redirect(url_for("login_bp.login"))

    username = session["user"].get("username")
    if not username:
        flash("User not recognized.", "error")
        return redirect(url_for("subject_bp.detail", subject_id=subject_id))

    result = mongo.db.reviews.delete_one({
        "subject_id": subject_id,
        "user_username": username
    })

    if result.deleted_count > 0:
        flash("🗑️ Your review has been deleted.", "review")
    else:
        flash("No review found to delete.", "error")

    return redirect(url_for("subject_bp.detail", subject_id=subject_id))