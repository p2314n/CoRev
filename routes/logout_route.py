from flask import Blueprint, redirect, url_for, session, flash

logout_bp = Blueprint("logout_bp", __name__, url_prefix="/auth")

@logout_bp.route("/logout")
def logout():
    """Logs out the current user and redirects to login page."""
    session.pop("user", None)  # Remove user session
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login_bp.login"))