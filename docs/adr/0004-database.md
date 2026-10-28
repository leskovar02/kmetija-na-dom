---
status: sprejeto
datum: 27-10-2026
---

# Izbira klasične relacijske podatkovne baze PostgreSQL

## Kontekst in problem
Aplikacija potrebuje zanesljivo hrambo strukturiranih podatkov (uporabniki, kmetije, izdelki, naročila) ter zagotavljanje relacijskih povezav.

## Dejavniki odločanja
* Zahteva po uporabi prave klasične strežniške podatkovne baze
* Podpora relacijam (tuji ključi, transakcije) in celovitosti podatkov
* Odlična integracija z orodji za objektno-relacijsko preslikovanje

## Obravnavane možnosti
* PostgreSQL
* SQLite
* mySql
* MariaDB

## Sprejeta odločitev in utemeljitev
Izbrana opcija: "PostgreSQL", ker gre za stabilno, odprtokodno relacijsko podatkovno bazo, ki zagotavlja doslednost podatkov in striktno preverjanje tujih ključev. To preprečuje nekonzistentne zapise v bazi (npr. naročilo brez obstoječega kupca ali izdelka). Poleg tega ponuja združljivost s Python ORM knjižnicami (kot je SQLAlchemy).

Odločitev za PostgreSQL je bila izvedena zaradi preteklih problemov z MySQL podatkovnimi bazami na tem računalniku, v upanju, da bo ta delala nemoteno. SQLite se je izkazal za preenostavnega za uporabno na tem projektu.

### Pozitivne posledice
* Visoka stopnja zanesljivosti in varnosti podatkov s podporo ACID transakcijam
* Izjemne zmogljivosti pri kompleksnih relacijskih poizvedbah in pridobivanju povezanih podatkov
* Standardizirana rešitev, ki je široko uporabljena v industriji

### Negativne posledice
* Zahteva zagon ločenega strežniškega procesa v primerjavi z lahkimi datotečnimi bazami