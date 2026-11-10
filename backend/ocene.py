from datetime import timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from auth import zahteva_vlogo
from models import Kmetija, Narocilo, Ocena, db

ocene = Blueprint("ocene", __name__)

CAS_DO_OCENE = timedelta(hours=24)


# pogoji za oceno #
def _cas_baze():
    return db.session.scalar(db.select(db.func.now())).replace(tzinfo=None)


def _razlog_da_ni_mogoce(narocilo, zdaj=None):
    if narocilo.ocena is not None:
        return "To naročilo je že ocenjeno."
    if narocilo.status != "zaprto" or narocilo.datum_zaprtja is None:
        return "Oceniti je mogoče le zaprto naročilo."
    if (zdaj or _cas_baze()) - narocilo.datum_zaprtja < CAS_DO_OCENE:
        return "Oceniti je mogoče šele 24 ur po zaprtju naročila."
    return None


# moja naročila #
@ocene.route("/narocila")
@zahteva_vlogo("kupec")
def moja_narocila():
    narocila = (
        Narocilo.query
        .filter_by(kupec_id=current_user.id)
        .order_by(Narocilo.datum_narocila.desc())
        .all()
    )
    zdaj = _cas_baze()
    lahko_oceni = {n.id for n in narocila if _razlog_da_ni_mogoce(n, zdaj) is None}
    return render_template("narocila.html", narocila=narocila, lahko_oceni=lahko_oceni)


# ocena #
@ocene.route("/narocila/<int:narocilo_id>/ocena", methods=["GET", "POST"])
@zahteva_vlogo("kupec")
def oceni(narocilo_id):
    narocilo = Narocilo.query.filter_by(id=narocilo_id, kupec_id=current_user.id).first()
    if narocilo is None:
        abort(404)

    razlog = _razlog_da_ni_mogoce(narocilo)
    napake = []

    if request.method == "POST" and razlog is None:
        ocena = request.form.get("ocena", "")
        komentar = request.form.get("komentar", "").strip()
        if ocena not in ("1", "2", "3", "4", "5"):
            napake.append("Izberite oceno od 1 do 5.")
        if not komentar:
            napake.append("Napišite komentar.")

        if not napake:
            db.session.add(Ocena(
                narocilo_id=narocilo.id,
                kupec_id=current_user.id,
                kmetija_id=narocilo.kmetija_id,
                ocena=int(ocena),
                komentar=komentar,
            ))
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                razlog = "To naročilo je že ocenjeno."
            else:
                flash("Hvala za oceno! Objavljena je na profilu kmetije.")
                return redirect(url_for("ocene.profil_kmetije", kmetija_id=narocilo.kmetija_id))

    status = 400 if request.method == "POST" else 200
    return render_template("ocena.html", narocilo=narocilo, razlog=razlog, napake=napake), status


# profil kmetije #
@ocene.route("/kmetije/<int:kmetija_id>")
@login_required
def profil_kmetije(kmetija_id):
    kmetija = db.session.get(Kmetija, kmetija_id)
    if kmetija is None:
        abort(404)

    povprecje, stevilo = db.session.execute(
        db.select(db.func.avg(Ocena.ocena), db.func.count(Ocena.id)).filter(Ocena.kmetija_id == kmetija.id)
    ).one()

    vse_ocene = Ocena.query.filter_by(kmetija_id=kmetija.id).order_by(Ocena.datum.desc()).all()

    return render_template(
        "kmetija.html",
        kmetija=kmetija,
        ocene=vse_ocene,
        povprecna_ocena=povprecje,
        stevilo_ocen=stevilo,
    )
