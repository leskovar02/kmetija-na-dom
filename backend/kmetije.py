from flask import Blueprint, render_template, request
from flask_login import login_required

from models import Kmetija, Kraj, Ocena, db
from razdalje import razdalje_od

kmetije = Blueprint("kmetije", __name__)


# seznam kmetij #
@kmetije.route("/kmetije")
@login_required
def seznam():
    kraj_id = request.args.get("kraj_id", "")
    kraj = db.session.get(Kraj, int(kraj_id)) if kraj_id.isdigit() else None

    vse_kmetije = Kmetija.query.order_by(Kmetija.naziv).all()

    ocene = {
        kmetija_id: (povprecje, stevilo)
        for kmetija_id, povprecje, stevilo in db.session.execute(
            db.select(Ocena.kmetija_id, db.func.avg(Ocena.ocena), db.func.count(Ocena.id))
            .group_by(Ocena.kmetija_id)
        )
    }

    razdalje = {}
    if kraj is not None:
        razdalje = razdalje_od(kraj.id)
        vse_kmetije.sort(key=lambda k: razdalje.get(k.kraj_id, float("inf")))

    return render_template(
        "kmetije.html",
        kmetije=vse_kmetije,
        ocene=ocene,
        razdalje=razdalje,
        izbran_kraj=kraj,
        kraji=Kraj.query.order_by(Kraj.naziv).all(),
    )
