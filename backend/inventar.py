import os
import uuid
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template,
    request, send_from_directory, url_for,
)
from flask_login import current_user

from auth import zahteva_vlogo
from models import ENOTE, KATEGORIJE, Izdelek, db

inventar = Blueprint("inventar", __name__)

VRSTE_SLIK = {
    b"\x89PNG\r\n\x1a\n": ".png",
    b"\xff\xd8\xff": ".jpg",
}


# pomožne funkcije #
def _mapa_slik():
    return current_app.config["SLIKE_DIR"]


def _moja_kmetija():
    kmetija = current_user.kmetija
    if kmetija is None:
        abort(403)
    return kmetija


def _moj_izdelek(izdelek_id):
    izdelek = db.session.get(Izdelek, izdelek_id)
    if izdelek is None or not izdelek.aktiven or izdelek.kmetija_id != _moja_kmetija().id:
        abort(404)
    return izdelek


def _preberi_stevilo(besedilo):
    try:
        return Decimal(besedilo.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return None


def _preberi_obrazec():
    f = request.form
    podatki = {
        "naziv": f.get("naziv", "").strip(),
        "kategorija": f.get("kategorija", ""),
        "opis": f.get("opis", "").strip(),
        "cena": f.get("cena", "").strip(),
        "enota": f.get("enota", ""),
        "zaloga": f.get("zaloga", "").strip(),
    }
    napake = []

    if not podatki["naziv"]:
        napake.append("Vnesite naziv izdelka.")
    if podatki["kategorija"] not in KATEGORIJE:
        napake.append("Izberite kategorijo.")
    if not podatki["opis"]:
        napake.append("Vnesite opis izdelka.")
    if podatki["enota"] not in ENOTE:
        napake.append("Izberite enoto količine.")

    cena = _preberi_stevilo(podatki["cena"])
    if cena is None or not cena.is_finite() or cena < 0:
        napake.append("Cena mora biti število, večje ali enako 0.")
    elif cena != cena.quantize(Decimal("0.01")):
        napake.append("Cena ima lahko največ dve decimalki.")

    zaloga = _preberi_stevilo(podatki["zaloga"])
    if zaloga is None or not zaloga.is_finite() or zaloga < 0:
        napake.append("Zaloga mora biti število, večje ali enako 0.")
    elif podatki["enota"] == "kos" and zaloga != zaloga.to_integral_value():
        napake.append("Pri enoti kos mora biti zaloga celo število.")
    elif zaloga != zaloga.quantize(Decimal("0.001")):
        napake.append("Zaloga ima lahko največ tri decimalke.")

    podatki["_cena"] = cena
    podatki["_zaloga"] = zaloga
    return podatki, napake


def _shrani_sliko(datoteka):
    if datoteka is None or not datoteka.filename:
        return None, "Naložite sliko izdelka."

    glava = datoteka.stream.read(8)
    datoteka.stream.seek(0)
    koncnica = next((k for zacetek, k in VRSTE_SLIK.items() if glava.startswith(zacetek)), None)
    if koncnica is None:
        return None, "Slika mora biti v obliki JPG ali PNG."

    ime = uuid.uuid4().hex + koncnica
    os.makedirs(_mapa_slik(), exist_ok=True)
    datoteka.save(os.path.join(_mapa_slik(), ime))
    return ime, None


def _izbrisi_sliko(ime):
    if ime:
        try:
            os.remove(os.path.join(_mapa_slik(), ime))
        except FileNotFoundError:
            pass


# strani #
@inventar.route("/slike/<path:ime>")
def slika(ime):
    return send_from_directory(_mapa_slik(), ime)


@inventar.route("/inventar")
@zahteva_vlogo("kmetovalec")
def seznam():
    izdelki = (
        Izdelek.query
        .filter_by(kmetija_id=_moja_kmetija().id, aktiven=True)
        .order_by(Izdelek.naziv)
        .all()
    )
    return render_template("inventar.html", izdelki=izdelki)


@inventar.route("/inventar/nov", methods=["GET", "POST"])
@zahteva_vlogo("kmetovalec")
def dodaj():
    kmetija = _moja_kmetija()

    if request.method == "GET":
        return render_template("izdelek-dodaj.html", podatki={}, napake=[])

    podatki, napake = _preberi_obrazec()
    if not napake:
        ime_slike, napaka_slike = _shrani_sliko(request.files.get("slika"))
        if napaka_slike:
            napake.append(napaka_slike)

    if napake:
        return render_template("izdelek-dodaj.html", podatki=podatki, napake=napake), 400

    db.session.add(Izdelek(
        kmetija_id=kmetija.id,
        naziv=podatki["naziv"],
        kategorija=podatki["kategorija"],
        opis=podatki["opis"],
        cena=podatki["_cena"],
        enota=podatki["enota"],
        zaloga=podatki["_zaloga"],
        slika=ime_slike,
    ))
    db.session.commit()

    flash(f"Izdelek \"{podatki['naziv']}\" je dodan.")
    return redirect(url_for("inventar.seznam"))


@inventar.route("/inventar/<int:izdelek_id>/uredi", methods=["GET", "POST"])
@zahteva_vlogo("kmetovalec")
def uredi(izdelek_id):
    izdelek = _moj_izdelek(izdelek_id)

    if request.method == "GET":
        podatki = {
            "naziv": izdelek.naziv,
            "kategorija": izdelek.kategorija,
            "opis": izdelek.opis,
            "cena": izdelek.cena,
            "enota": izdelek.enota,
            "zaloga": izdelek.zaloga.normalize(),
        }
        return render_template("izdelek-uredi.html", izdelek=izdelek, podatki=podatki, napake=[])

    podatki, napake = _preberi_obrazec()

    nova_slika = None
    datoteka = request.files.get("slika")
    if not napake and datoteka is not None and datoteka.filename:
        nova_slika, napaka_slike = _shrani_sliko(datoteka)
        if napaka_slike:
            napake.append(napaka_slike)

    if napake:
        return render_template("izdelek-uredi.html", izdelek=izdelek, podatki=podatki, napake=napake), 400

    izdelek.naziv = podatki["naziv"]
    izdelek.kategorija = podatki["kategorija"]
    izdelek.opis = podatki["opis"]
    izdelek.cena = podatki["_cena"]
    izdelek.enota = podatki["enota"]
    izdelek.zaloga = podatki["_zaloga"]
    stara_slika = None
    if nova_slika:
        stara_slika, izdelek.slika = izdelek.slika, nova_slika
    db.session.commit()
    _izbrisi_sliko(stara_slika)

    flash(f"Spremembe izdelka \"{izdelek.naziv}\" so shranjene.")
    return redirect(url_for("inventar.seznam"))


@inventar.route("/inventar/<int:izdelek_id>/izbrisi", methods=["GET", "POST"])
@zahteva_vlogo("kmetovalec")
def izbrisi(izdelek_id):
    izdelek = _moj_izdelek(izdelek_id)

    if request.method == "GET":
        return render_template("izdelek-izbrisi.html", izdelek=izdelek)

    izdelek.aktiven = False
    db.session.commit()

    flash(f"Izdelek \"{izdelek.naziv}\" je odstranjen iz ponudbe.")
    return redirect(url_for("inventar.seznam"))
