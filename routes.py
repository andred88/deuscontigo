from flask import render_template, redirect, url_for, request, session, Blueprint
from models import Consagrado, db
from functools import wraps
from datetime import datetime

bp = Blueprint("main", __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

@bp.route("/")
@login_required
def dashboard():
    consagrados = Consagrado.query.all()
    return render_template("dashboard.html", consagrados=consagrados)

@bp.route("/consagrados/novo", methods=["GET", "POST"])
@login_required
def novo_consagrado():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form.get("telefone")
        data_nascimento = datetime.strptime(request.form["data_nascimento"], "%Y-%m-%d")
        consagrado = Consagrado(nome=nome, email=email, telefone=telefone, data_nascimento=data_nascimento)
        db.session.add(consagrado)
        db.session.commit()
        return redirect(url_for("main.dashboard"))
    return render_template("novo_consagrado.html")
