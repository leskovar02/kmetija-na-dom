from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# dovoljene vrednosti #
VLOGE = ("kupec", "kmetovalec", "admin")

TIPI_KMETIJE = ("ekoloska", "integrirana", "mesana")

KATEGORIJE_IMENA = {
    "zelenjava": "Zelenjava",
    "sadje": "Sadje",
    "mlecni-izdelki": "Mlečni izdelki",
    "jajca": "Jajca",
    "med": "Med",
    "drugo": "Drugo",
}
KATEGORIJE = tuple(KATEGORIJE_IMENA)

ENOTE = ("kg", "kos", "liter")

STANJA_IMENA = {
    "caka-na-potrditev": "Čaka na potrditev",
    "potrjeno": "Potrjeno",
    "zavrnjeno": "Zavrnjeno",
    "v-pripravi": "V pripravi",
    "za-prevzem": "Za prevzem",
    "zaprto": "Zaprto",
}
STANJA_NAROCILA = tuple(STANJA_IMENA)

# potek stanj #
DOVOLJENI_PREHODI = {
    "caka-na-potrditev": ("potrjeno", "zavrnjeno"),
    "potrjeno": ("v-pripravi",),
    "v-pripravi": ("za-prevzem",),
    "za-prevzem": ("zaprto",),
    "zavrnjeno": (),
    "zaprto": (),
}


# tabele #
def _v_seznamu(stolpec, vrednosti):
    seznam = ", ".join(f"'{v}'" for v in vrednosti)
    return f"{stolpec} IN ({seznam})"


class Uporabnik(UserMixin, db.Model):
    __tablename__ = "uporabnik"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    priimek = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    geslo = db.Column(db.String(128), nullable=False)
    vloga = db.Column(db.String(20), nullable=False)

    kmetija = db.relationship("Kmetija", back_populates="kmetovalec", uselist=False)
    narocila = db.relationship("Narocilo", back_populates="kupec")

    __table_args__ = (
        db.CheckConstraint(_v_seznamu("vloga", VLOGE), name="ck_uporabnik_vloga"),
    )


class Kraj(db.Model):
    __tablename__ = "kraj"

    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False, unique=True)

    kmetije = db.relationship("Kmetija", back_populates="kraj")


class Povezava(db.Model):
    __tablename__ = "povezava"

    id = db.Column(db.Integer, primary_key=True)
    kraj_a_id = db.Column(db.Integer, db.ForeignKey("kraj.id"), nullable=False)
    kraj_b_id = db.Column(db.Integer, db.ForeignKey("kraj.id"), nullable=False)
    razdalja_km = db.Column(db.Numeric(6, 1), nullable=False)

    kraj_a = db.relationship("Kraj", foreign_keys=[kraj_a_id])
    kraj_b = db.relationship("Kraj", foreign_keys=[kraj_b_id])

    __table_args__ = (
        db.UniqueConstraint("kraj_a_id", "kraj_b_id", name="uq_povezava_kraja"),
        db.CheckConstraint("kraj_a_id <> kraj_b_id", name="ck_povezava_razlicna_kraja"),
        db.CheckConstraint("razdalja_km > 0", name="ck_povezava_razdalja"),
    )


class Kmetija(db.Model):
    __tablename__ = "kmetija"

    id = db.Column(db.Integer, primary_key=True)
    kmetovalec_id = db.Column(db.Integer, db.ForeignKey("uporabnik.id"), nullable=False, unique=True)
    kraj_id = db.Column(db.Integer, db.ForeignKey("kraj.id"), nullable=False)
    naziv = db.Column(db.String(150), nullable=False)
    tip = db.Column(db.String(20), nullable=False)
    informacije = db.Column(db.Text)
    naslov = db.Column(db.String(255), nullable=False)

    kmetovalec = db.relationship("Uporabnik", back_populates="kmetija")
    kraj = db.relationship("Kraj", back_populates="kmetije")
    izdelki = db.relationship("Izdelek", back_populates="kmetija")
    narocila = db.relationship("Narocilo", back_populates="kmetija")
    ocene = db.relationship("Ocena", back_populates="kmetija")

    __table_args__ = (
        db.CheckConstraint(_v_seznamu("tip", TIPI_KMETIJE), name="ck_kmetija_tip"),
    )


class Izdelek(db.Model):
    __tablename__ = "izdelek"

    id = db.Column(db.Integer, primary_key=True)
    kmetija_id = db.Column(db.Integer, db.ForeignKey("kmetija.id"), nullable=False)
    naziv = db.Column(db.String(150), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    kategorija = db.Column(db.String(30), nullable=False)
    cena = db.Column(db.Numeric(10, 2), nullable=False)
    enota = db.Column(db.String(10), nullable=False)
    zaloga = db.Column(db.Numeric(10, 3), nullable=False, default=0)
    slika = db.Column(db.String(255))
    aktiven = db.Column(db.Boolean, nullable=False, default=True)

    kmetija = db.relationship("Kmetija", back_populates="izdelki")

    __table_args__ = (
        db.CheckConstraint("cena >= 0", name="ck_izdelek_cena"),
        db.CheckConstraint("zaloga >= 0", name="ck_izdelek_zaloga"),
        db.CheckConstraint(_v_seznamu("kategorija", KATEGORIJE), name="ck_izdelek_kategorija"),
        db.CheckConstraint(_v_seznamu("enota", ENOTE), name="ck_izdelek_enota"),
    )


class Narocilo(db.Model):
    __tablename__ = "narocilo"

    id = db.Column(db.Integer, primary_key=True)
    kupec_id = db.Column(db.Integer, db.ForeignKey("uporabnik.id"), nullable=False)
    kmetija_id = db.Column(db.Integer, db.ForeignKey("kmetija.id"), nullable=False)
    datum_narocila = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(20), nullable=False, default="caka-na-potrditev")
    skupni_znesek = db.Column(db.Numeric(10, 2), nullable=False)
    datum_zaprtja = db.Column(db.DateTime)

    kupec = db.relationship("Uporabnik", back_populates="narocila")
    kmetija = db.relationship("Kmetija", back_populates="narocila")
    postavke = db.relationship("NarociloIzdelek", back_populates="narocilo", cascade="all, delete-orphan")
    ocena = db.relationship("Ocena", back_populates="narocilo", uselist=False)

    __table_args__ = (
        db.CheckConstraint(_v_seznamu("status", STANJA_NAROCILA), name="ck_narocilo_status"),
        db.CheckConstraint("skupni_znesek >= 0", name="ck_narocilo_znesek"),
    )


class NarociloIzdelek(db.Model):
    __tablename__ = "narocilo_izdelek"

    id = db.Column(db.Integer, primary_key=True)
    narocilo_id = db.Column(db.Integer, db.ForeignKey("narocilo.id"), nullable=False)
    izdelek_id = db.Column(db.Integer, db.ForeignKey("izdelek.id"), nullable=False)
    kolicina = db.Column(db.Numeric(10, 3), nullable=False)
    cena = db.Column(db.Numeric(10, 2), nullable=False)

    narocilo = db.relationship("Narocilo", back_populates="postavke")
    izdelek = db.relationship("Izdelek")

    __table_args__ = (
        db.UniqueConstraint("narocilo_id", "izdelek_id", name="uq_postavka_izdelek"),
        db.CheckConstraint("kolicina > 0", name="ck_postavka_kolicina"),
        db.CheckConstraint("cena >= 0", name="ck_postavka_cena"),
    )


class Ocena(db.Model):
    __tablename__ = "ocena"

    id = db.Column(db.Integer, primary_key=True)
    narocilo_id = db.Column(db.Integer, db.ForeignKey("narocilo.id"), nullable=False, unique=True)
    kupec_id = db.Column(db.Integer, db.ForeignKey("uporabnik.id"), nullable=False)
    kmetija_id = db.Column(db.Integer, db.ForeignKey("kmetija.id"), nullable=False)
    ocena = db.Column(db.Integer, nullable=False)
    komentar = db.Column(db.Text, nullable=False)
    datum = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    narocilo = db.relationship("Narocilo", back_populates="ocena")
    kupec = db.relationship("Uporabnik")
    kmetija = db.relationship("Kmetija", back_populates="ocene")

    __table_args__ = (
        db.CheckConstraint("ocena BETWEEN 1 AND 5", name="ck_ocena_vrednost"),
    )
