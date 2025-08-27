from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models import db, Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(username=request.form["username"]).first()
        if user and user.check_senha(request.form["password"]):
            session["usuario_id"] = user.id
            return redirect(url_for("main.dashboard"))
        flash("Usuário ou senha inválidos.")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    return redirect(url_for("auth.login"))
