from models import Kraj, Povezava, db

# kraji #
KRAJI = (
    "Ajdovščina",
    "Brežice",
    "Celje",
    "Domžale",
    "Jesenice",
    "Kamnik",
    "Koper",
    "Kranj",
    "Krško",
    "Ljubljana",
    "Maribor",
    "Murska Sobota",
    "Nova Gorica",
    "Novo mesto",
    "Postojna",
    "Ptuj",
    "Slovenj Gradec",
    "Škofja Loka",
    "Trbovlje",
    "Velenje",
)

# povezave #
POVEZAVE = (
    ("Ljubljana", "Domžale", 15),
    ("Ljubljana", "Kamnik", 25),
    ("Ljubljana", "Kranj", 30),
    ("Ljubljana", "Škofja Loka", 25),
    ("Ljubljana", "Postojna", 50),
    ("Ljubljana", "Novo mesto", 70),
    ("Ljubljana", "Trbovlje", 50),
    ("Domžale", "Kamnik", 12),
    ("Domžale", "Trbovlje", 40),
    ("Domžale", "Celje", 55),
    ("Kranj", "Škofja Loka", 12),
    ("Kranj", "Jesenice", 35),
    ("Kranj", "Kamnik", 25),
    ("Postojna", "Koper", 50),
    ("Postojna", "Ajdovščina", 35),
    ("Ajdovščina", "Nova Gorica", 25),
    ("Nova Gorica", "Koper", 75),
    ("Celje", "Velenje", 25),
    ("Celje", "Maribor", 55),
    ("Celje", "Trbovlje", 35),
    ("Celje", "Krško", 55),
    ("Velenje", "Slovenj Gradec", 25),
    ("Slovenj Gradec", "Maribor", 60),
    ("Maribor", "Ptuj", 30),
    ("Maribor", "Murska Sobota", 60),
    ("Ptuj", "Murska Sobota", 50),
    ("Krško", "Brežice", 12),
    ("Krško", "Novo mesto", 40),
    ("Trbovlje", "Krško", 40),
)


# vnos #
def napolni_kraje():
    if Kraj.query.first() is None:
        db.session.add_all(Kraj(naziv=naziv) for naziv in KRAJI)
        db.session.commit()

    if Povezava.query.first() is None:
        id_kraja = {k.naziv: k.id for k in Kraj.query.all()}
        db.session.add_all(
            Povezava(kraj_a_id=id_kraja[a], kraj_b_id=id_kraja[b], razdalja_km=km)
            for a, b, km in POVEZAVE
            if a in id_kraja and b in id_kraja
        )
        db.session.commit()
