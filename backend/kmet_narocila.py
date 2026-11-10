from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from auth import zahteva_vlogo
from models import DOVOLJENI_PREHODI, STANJA_IMENA, STANJA_NAROCILA, Narocilo, db

kmet_narocila = Blueprint("kmet_narocila", __name__)

GUMBI_PREHODOV = {
    "potrjeno": "Potrdi",
    "zavrnjeno": "Zavrni",
    "v-pripravi": "V pripravi",
    "za-prevzem": "Za prevzem",
    "zaprto": "Zapri",
}


def _id_moje_kmetije():
    if current_user.kmetija is None:
        abort(403)
    return current_user.kmetija.id


def _moje_narocilo(narocilo_id, zakleni=False):
    poizvedba = Narocilo.query.filter_by(id=narocilo_id, kmetija_id=_id_moje_kmetije())
    if zakleni:
        poizvedba = poizvedba.with_for_update()
    narocilo = poizvedba.first()
    if narocilo is None:
        abort(404)
    return narocilo


# naročila kmetije #
@kmet_narocila.route("/kmetovalec/narocila")
@zahteva_vlogo("kmetovalec")
def seznam():
    stanje = request.args.get("stanje", "")
    poizvedba = Narocilo.query.filter_by(kmetija_id=_id_moje_kmetije())
    if stanje in STANJA_NAROCILA:
        poizvedba = poizvedba.filter_by(status=stanje)
    narocila = poizvedba.order_by(Narocilo.datum_narocila.desc()).all()
    return render_template("kmetovalec-narocila.html", narocila=narocila, stanje=stanje)


@kmet_narocila.route("/kmetovalec/narocila/<int:narocilo_id>")
@zahteva_vlogo("kmetovalec")
def podrobnosti(narocilo_id):
    narocilo = _moje_narocilo(narocilo_id)
    prehodi = [(s, GUMBI_PREHODOV[s]) for s in DOVOLJENI_PREHODI[narocilo.status]]
    return render_template("kmetovalec-narocilo.html", narocilo=narocilo, prehodi=prehodi)


@kmet_narocila.route("/kmetovalec/narocila/<int:narocilo_id>/stanje", methods=["POST"])
@zahteva_vlogo("kmetovalec")
def spremeni_stanje(narocilo_id):
    # zaklep naročila #
    narocilo = _moje_narocilo(narocilo_id, zakleni=True)
    novo = request.form.get("stanje", "")

    if novo not in DOVOLJENI_PREHODI[narocilo.status]:
        db.session.rollback()
        flash(f"Iz stanja \"{STANJA_IMENA[narocilo.status]}\" ni mogoče preiti v izbrano stanje.")
        return redirect(url_for("kmet_narocila.podrobnosti", narocilo_id=narocilo.id))

    narocilo.status = novo

    if novo == "zavrnjeno":
        for postavka in narocilo.postavke:
            postavka.izdelek.zaloga += postavka.kolicina
    elif novo == "zaprto":
        narocilo.datum_zaprtja = db.func.now()

    db.session.commit()

    flash(f"Stanje naročila št. {narocilo.id} je zdaj \"{STANJA_IMENA[novo]}\".")
    return redirect(url_for("kmet_narocila.podrobnosti", narocilo_id=narocilo.id))
