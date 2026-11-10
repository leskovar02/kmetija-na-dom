from decimal import Decimal, InvalidOperation

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from auth import zahteva_vlogo
from models import Izdelek, Narocilo, NarociloIzdelek, db

nakup = Blueprint("nakup", __name__)

KLJUC_KOSARICE = "kosarica"


# košarica v seji #
def _kosarica():
    return session.get(KLJUC_KOSARICE, {})


def _shrani_kosarico(kosarica):
    session[KLJUC_KOSARICE] = kosarica
    session.modified = True


def _aktiven_izdelek(izdelek_id):
    izdelek = db.session.get(Izdelek, izdelek_id)
    if izdelek is None or not izdelek.aktiven:
        abort(404)
    return izdelek


def _preberi_kolicino(besedilo):
    try:
        kolicina = Decimal((besedilo or "").replace(",", "."))
    except InvalidOperation:
        return None
    return kolicina if kolicina.is_finite() else None


def _napaka_kolicine(izdelek, kolicina):
    if kolicina is None or kolicina <= 0:
        return "Vnesite količino, večjo od 0."
    korak = Decimal("1") if izdelek.enota == "kos" else Decimal("0.5")
    if kolicina % korak != 0:
        return f"Količina za {izdelek.naziv} mora biti večkratnik {str(korak.normalize()).replace('.', ',')} {izdelek.enota}."
    if kolicina > izdelek.zaloga:
        return f"Količina za {izdelek.naziv} presega trenutno zalogo ({izdelek.zaloga.normalize()} {izdelek.enota})."
    return None


def _postavke_kosarice():
    kosarica = _kosarica()
    po_kmetijah = {}
    skupaj = Decimal("0")
    spremenjena = False

    for izdelek_id, kolicina_niz in list(kosarica.items()):
        izdelek = db.session.get(Izdelek, int(izdelek_id))
        if izdelek is None or not izdelek.aktiven:
            del kosarica[izdelek_id]
            spremenjena = True
            continue

        kolicina = Decimal(kolicina_niz)
        znesek = (izdelek.cena * kolicina).quantize(Decimal("0.01"))
        blok = po_kmetijah.setdefault(izdelek.kmetija_id, {
            "kmetija": izdelek.kmetija, "postavke": [], "vmesna_vsota": Decimal("0"),
        })
        blok["postavke"].append({"izdelek": izdelek, "kolicina": kolicina, "skupaj": znesek})
        blok["vmesna_vsota"] += znesek
        skupaj += znesek

    if spremenjena:
        _shrani_kosarico(kosarica)
    return list(po_kmetijah.values()), skupaj


# stran izdelka #
@nakup.route("/izdelki/<int:izdelek_id>")
@login_required
def izdelek(izdelek_id):
    return render_template("izdelek.html", izdelek=_aktiven_izdelek(izdelek_id))


# košarica #
@nakup.route("/kosarica")
@zahteva_vlogo("kupec")
def kosarica():
    bloki, skupni_znesek = _postavke_kosarice()
    return render_template("kosarica.html", bloki=bloki, skupni_znesek=skupni_znesek)


@nakup.route("/kosarica/dodaj", methods=["POST"])
@zahteva_vlogo("kupec")
def dodaj_v_kosarico():
    izdelek_id = request.form.get("izdelek_id", "")
    if not izdelek_id.isdigit():
        abort(400)
    izdelek = _aktiven_izdelek(int(izdelek_id))

    kosarica = _kosarica()
    ze_v_kosarici = Decimal(kosarica.get(izdelek_id, "0"))
    dodano = _preberi_kolicino(request.form.get("kolicina"))
    napaka = _napaka_kolicine(izdelek, dodano) or (
        _napaka_kolicine(izdelek, ze_v_kosarici + dodano) if ze_v_kosarici else None
    )

    if napaka:
        flash(napaka)
    else:
        kosarica[izdelek_id] = str(ze_v_kosarici + dodano)
        _shrani_kosarico(kosarica)
        flash(f"{izdelek.naziv} je dodan v košarico.")
    return redirect(url_for("nakup.izdelek", izdelek_id=izdelek.id))


@nakup.route("/kosarica/posodobi", methods=["POST"])
@zahteva_vlogo("kupec")
def posodobi_kosarico():
    izdelek_id = request.form.get("izdelek_id", "")
    kosarica = _kosarica()
    if izdelek_id not in kosarica:
        return redirect(url_for("nakup.kosarica"))

    kolicina = _preberi_kolicino(request.form.get("kolicina"))
    if kolicina == 0:
        del kosarica[izdelek_id]
    else:
        izdelek = _aktiven_izdelek(int(izdelek_id))
        napaka = _napaka_kolicine(izdelek, kolicina)
        if napaka:
            flash(napaka)
            return redirect(url_for("nakup.kosarica"))
        kosarica[izdelek_id] = str(kolicina)

    _shrani_kosarico(kosarica)
    return redirect(url_for("nakup.kosarica"))


@nakup.route("/kosarica/odstrani", methods=["POST"])
@zahteva_vlogo("kupec")
def odstrani_iz_kosarice():
    kosarica = _kosarica()
    kosarica.pop(request.form.get("izdelek_id", ""), None)
    _shrani_kosarico(kosarica)
    return redirect(url_for("nakup.kosarica"))


# oddaja naročila #
@nakup.route("/narocilo/oddaj", methods=["POST"])
@zahteva_vlogo("kupec")
def oddaj_narocilo():
    kosarica = _kosarica()
    if not kosarica:
        flash("Košarica je prazna.")
        return redirect(url_for("nakup.kosarica"))

    # zaklep zaloge #
    izdelki = (
        Izdelek.query
        .filter(Izdelek.id.in_([int(i) for i in kosarica]))
        .with_for_update()
        .all()
    )
    izdelki = {str(i.id): i for i in izdelki}

    napake = []
    for izdelek_id, kolicina_niz in kosarica.items():
        izdelek = izdelki.get(izdelek_id)
        if izdelek is None or not izdelek.aktiven:
            napake.append("Eden od izdelkov ni več v ponudbi.")
            continue
        napaka = _napaka_kolicine(izdelek, Decimal(kolicina_niz))
        if napaka:
            napake.append(napaka)

    if napake:
        db.session.rollback()
        for napaka in napake:
            flash(napaka)
        flash("Naročilo ni bilo oddano. Prilagodite košarico in poskusite znova.")
        return redirect(url_for("nakup.kosarica"))

    narocila = {}
    for izdelek_id, kolicina_niz in kosarica.items():
        izdelek = izdelki[izdelek_id]
        kolicina = Decimal(kolicina_niz)

        narocilo = narocila.get(izdelek.kmetija_id)
        if narocilo is None:
            narocilo = Narocilo(
                kupec_id=current_user.id,
                kmetija_id=izdelek.kmetija_id,
                status="caka-na-potrditev",
                skupni_znesek=Decimal("0"),
            )
            db.session.add(narocilo)
            narocila[izdelek.kmetija_id] = narocilo

        narocilo.postavke.append(NarociloIzdelek(izdelek=izdelek, kolicina=kolicina, cena=izdelek.cena))
        narocilo.skupni_znesek += (izdelek.cena * kolicina).quantize(Decimal("0.01"))
        izdelek.zaloga -= kolicina

    db.session.commit()

    _shrani_kosarico({})
    session["oddana_narocila"] = [n.id for n in narocila.values()]
    return redirect(url_for("nakup.narocilo_oddano"))


@nakup.route("/narocilo/oddano")
@zahteva_vlogo("kupec")
def narocilo_oddano():
    idji = session.get("oddana_narocila", [])
    narocila = (
        Narocilo.query
        .filter(Narocilo.id.in_(idji), Narocilo.kupec_id == current_user.id)
        .order_by(Narocilo.id)
        .all()
    )
    if not narocila:
        return redirect(url_for("nakup.kosarica"))
    return render_template("narocilo-oddano.html", narocila=narocila)
