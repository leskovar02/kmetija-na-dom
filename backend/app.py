import os
from decimal import Decimal

import click
from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager

from auth import auth, zgosti_geslo
from inventar import inventar
from katalog import katalog
from nakup import nakup
from kmet_narocila import kmet_narocila
from ocene import ocene
from kmetije import kmetije
from models import KATEGORIJE_IMENA, STANJA_IMENA, Uporabnik, db
from seme import napolni_kraje

FRONTEND_DIR = os.environ.get("FRONTEND_DIR", os.path.join(os.path.dirname(__file__), "frontend"))

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="",
)

# nastavitve #
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["SLIKE_DIR"] = os.environ.get("SLIKE_DIR", os.path.join(os.path.dirname(__file__), "slike"))
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

db.init_app(app)

# prijava #
login_manager = LoginManager(app)


@login_manager.user_loader
def nalozi_uporabnika(uporabnik_id):
    return db.session.get(Uporabnik, int(uporabnik_id))


@login_manager.unauthorized_handler
def neprijavljen():
    return redirect(url_for("vstopna_stran"))


@app.after_request
def brez_predpomnjenja(odgovor):
    if odgovor.mimetype == "text/html":
        odgovor.headers["Cache-Control"] = "no-store"
    return odgovor


# moduli #
app.register_blueprint(auth)
app.register_blueprint(inventar)
app.register_blueprint(katalog)
app.register_blueprint(nakup)
app.register_blueprint(kmet_narocila)
app.register_blueprint(ocene)
app.register_blueprint(kmetije)


# filtri za predloge #
@app.template_filter("evro")
def evro(znesek):
    return f"{Decimal(znesek):.2f}".replace(".", ",")


@app.template_filter("kolicina")
def kolicina(vrednost):
    return f"{Decimal(vrednost).normalize():f}".replace(".", ",")


@app.template_filter("datum")
def datum(vrednost):
    return vrednost.strftime("%d. %m. %Y %H:%M") if vrednost else ""


app.jinja_env.globals["KATEGORIJE_IMENA"] = KATEGORIJE_IMENA
app.jinja_env.globals["STANJA_IMENA"] = STANJA_IMENA


# nazaj na vstop #
@app.route("/")
def vstopna_stran():
    return render_template("index.html")

# baza init #
with app.app_context():
    db.create_all()
    napolni_kraje()


# ukazi #
@app.cli.command("ustvari-admina")
@click.option("--ime", prompt="Ime")
@click.option("--priimek", prompt="Priimek")
@click.option("--email", prompt="E-poštni naslov")
@click.option("--geslo", prompt="Geslo", hide_input=True, confirmation_prompt=True)
def ustvari_admina(ime, priimek, email, geslo):
    email = email.strip().lower()
    if Uporabnik.query.filter_by(email=email).first():
        raise click.ClickException("Uporabnik s tem e-poštnim naslovom že obstaja.")
    db.session.add(Uporabnik(
        ime=ime.strip(),
        priimek=priimek.strip(),
        email=email,
        geslo=zgosti_geslo(geslo),
        vloga="admin",
    ))
    db.session.commit()
    click.echo(f"Administrator {email} je ustvarjen.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
