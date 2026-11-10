from functools import wraps

import bcrypt
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from models import TIPI_KMETIJE, Kmetija, Kraj, Uporabnik, db

auth = Blueprint("auth", __name__)

JAVNE_VLOGE = ("kupec", "kmetovalec")


# vloge #
def zahteva_vlogo(*vloge):
    def dekorator(funkcija):
        @wraps(funkcija)
        @login_required
        def ovoj(*args, **kwargs):
            if current_user.vloga not in vloge:
                abort(403)
            return funkcija(*args, **kwargs)
        return ovoj
    return dekorator


# registracija #
def zgosti_geslo(geslo):
    return bcrypt.hashpw(geslo.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _prikazi_registracijo(podatki=None, napake=None, status=200):
    kraji = Kraj.query.order_by(Kraj.naziv).all()
    return render_template(
        "register.html",
        kraji=kraji,
        podatki=podatki or {},
        napake=napake or [],
    ), status


@auth.route("/registracija", methods=["GET", "POST"])
def registracija():
    if request.method == "GET":
        return _prikazi_registracijo()

    f = request.form
    podatki = {
        "ime": f.get("ime", "").strip(),
        "priimek": f.get("priimek", "").strip(),
        "email": f.get("email", "").strip().lower(),
        "vloga": f.get("vloga", ""),
        "naziv_kmetije": f.get("naziv_kmetije", "").strip(),
        "naslov": f.get("naslov", "").strip(),
        "kraj_id": f.get("kraj_id", ""),
        "tip": f.get("tip", ""),
        "informacije": f.get("informacije", "").strip(),
    }
    geslo = f.get("geslo", "")
    napake = []

    if not podatki["ime"] or not podatki["priimek"]:
        napake.append("Vnesite ime in priimek.")
    if "@" not in podatki["email"] or "." not in podatki["email"].split("@")[-1]:
        napake.append("Vnesite veljaven e-poštni naslov.")
    if not geslo:
        napake.append("Vnesite geslo.")
    if podatki["vloga"] not in JAVNE_VLOGE:
        napake.append("Izberite vlogo: kupec ali kmetovalec.")

    kraj = None
    if podatki["vloga"] == "kmetovalec":
        if not podatki["naziv_kmetije"]:
            napake.append("Vnesite naziv kmetije.")
        if not podatki["naslov"]:
            napake.append("Vnesite naslov kmetije za prevzem.")
        if podatki["kraj_id"].isdigit():
            kraj = db.session.get(Kraj, int(podatki["kraj_id"]))
        if kraj is None:
            napake.append("Izberite najbližji kraj.")
        if podatki["tip"] not in TIPI_KMETIJE:
            napake.append("Izberite tip kmetije.")

    if not napake and Uporabnik.query.filter_by(email=podatki["email"]).first():
        napake.append("Uporabnik s tem e-poštnim naslovom je že registriran.")

    if napake:
        return _prikazi_registracijo(podatki, napake, status=400)

    uporabnik = Uporabnik(
        ime=podatki["ime"],
        priimek=podatki["priimek"],
        email=podatki["email"],
        geslo=zgosti_geslo(geslo),
        vloga=podatki["vloga"],
    )
    db.session.add(uporabnik)

    if uporabnik.vloga == "kmetovalec":
        db.session.add(Kmetija(
            kmetovalec=uporabnik,
            kraj=kraj,
            naziv=podatki["naziv_kmetije"],
            tip=podatki["tip"],
            informacije=podatki["informacije"] or None,
            naslov=podatki["naslov"],
        ))

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return _prikazi_registracijo(
            podatki, ["Uporabnik s tem e-poštnim naslovom je že registriran."], status=400
        )

    flash("Registracija je uspela. Zdaj se lahko prijavite.")
    return redirect(url_for("auth.prijava"))


# prijava in odjava #
def zacetna_stran(uporabnik):
    if uporabnik.vloga == "kmetovalec" and uporabnik.kmetija is not None:
        return f"/kmetije/{uporabnik.kmetija.id}"
    return "/kmetije"


def _varna_naslednja(naslov):
    if naslov and naslov.startswith("/") and not naslov.startswith("//"):
        return naslov
    return None


@auth.route("/prijava", methods=["GET", "POST"])
def prijava():
    if current_user.is_authenticated:
        return redirect(zacetna_stran(current_user))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    geslo = request.form.get("geslo", "")
    naslednja = request.form.get("next", "")

    uporabnik = Uporabnik.query.filter_by(email=email).first()
    geslo_pravilno = uporabnik is not None and bcrypt.checkpw(
        geslo.encode("utf-8"), uporabnik.geslo.encode("utf-8")
    )

    if not geslo_pravilno:
        return render_template(
            "login.html",
            napaka="Napačen e-poštni naslov ali geslo.",
            email=email,
            naslednja=naslednja,
        ), 401

    login_user(uporabnik)
    return redirect(_varna_naslednja(naslednja) or zacetna_stran(uporabnik))


@auth.route("/odjava")
@login_required
def odjava():
    logout_user()
    return redirect(url_for("vstopna_stran"))
