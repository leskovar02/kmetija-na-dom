from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request
from flask_login import login_required

from models import KATEGORIJE, TIPI_KMETIJE, Izdelek, Kmetija, Kraj, db
from razdalje import razdalje_od

katalog = Blueprint("katalog", __name__)


def _decimalno(besedilo):
    if not besedilo:
        return None
    try:
        vrednost = Decimal(besedilo.replace(",", "."))
    except InvalidOperation:
        return None
    return vrednost if vrednost.is_finite() and vrednost >= 0 else None


# katalog #
@katalog.route("/izdelki")
@login_required
def izdelki():
    a = request.args
    filtri = {
        "iskanje": a.get("iskanje", "").strip(),
        "kategorija": a.get("kategorija", ""),
        "tip": a.get("tip", ""),
        "cena_od": a.get("cena_od", "").strip(),
        "cena_do": a.get("cena_do", "").strip(),
        "kraj_id": a.get("kraj_id", ""),
        "oddaljenost": a.get("oddaljenost", ""),
        "kmetija_id": a.get("kmetija_id", ""),
    }

    kmetija = db.session.get(Kmetija, int(filtri["kmetija_id"])) if filtri["kmetija_id"].isdigit() else None

    poizvedba = (
        Izdelek.query
        .join(Kmetija)
        .filter(Izdelek.aktiven.is_(True), Izdelek.zaloga > 0)
    )

    if kmetija is not None:
        poizvedba = poizvedba.filter(Izdelek.kmetija_id == kmetija.id)
    if filtri["iskanje"]:
        vzorec = f"%{filtri['iskanje']}%"
        poizvedba = poizvedba.filter(Izdelek.naziv.ilike(vzorec) | Izdelek.opis.ilike(vzorec))
    if filtri["kategorija"] in KATEGORIJE:
        poizvedba = poizvedba.filter(Izdelek.kategorija == filtri["kategorija"])
    if filtri["tip"] in TIPI_KMETIJE:
        poizvedba = poizvedba.filter(Kmetija.tip == filtri["tip"])

    cena_od = _decimalno(filtri["cena_od"])
    cena_do = _decimalno(filtri["cena_do"])
    if cena_od is not None:
        poizvedba = poizvedba.filter(Izdelek.cena >= cena_od)
    if cena_do is not None:
        poizvedba = poizvedba.filter(Izdelek.cena <= cena_do)

    rezultati = poizvedba.order_by(Izdelek.naziv).all()

    razdalje = {}
    kraj = db.session.get(Kraj, int(filtri["kraj_id"])) if filtri["kraj_id"].isdigit() else None
    if kraj is not None:
        razdalje = razdalje_od(kraj.id)
        if filtri["oddaljenost"].isdigit():
            najvec = int(filtri["oddaljenost"])
            rezultati = [i for i in rezultati if razdalje.get(i.kmetija.kraj_id, float("inf")) <= najvec]
        rezultati.sort(key=lambda i: razdalje.get(i.kmetija.kraj_id, float("inf")))

    return render_template(
        "izdelki.html",
        izdelki=rezultati,
        razdalje=razdalje,
        filtri=filtri,
        izbrana_kmetija=kmetija,
        kraji=Kraj.query.order_by(Kraj.naziv).all(),
    )
