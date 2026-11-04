---
status: sprejeto
datum: 27-10-2026
---

# Uporaba orodja Docker (+ Docker Compose) za lokalni zagon celotne aplikacije

## Kontekst in problem
Zagotoviti moramo enostaven, hiter in ponovljiv zagon celotne aplikacije (podatkovna baza, zaledje in spletni vmesnik) v lokalnem razvojnem okolju brez kompleksnih ročnih namestitev.

## Dejavniki odločanja
* Enostavna vzpostavitev enakega razvojnega okolja na različnih računalnikih in operacijskih sistemih
* Izogibanje ročni namestitvi in konfiguraciji strežnika podatkovne baze neposredno na operacijski sistem
* Zagon vseh delov aplikacije z enim samim ukazom
* Hitro ponastavljanje ali brisanje testnih podatkov

## Obravnavane možnosti
* Docker (+ Docker Compose)
* Kubernetes

## Sprejeta odločitev in utemeljitev
Izbrana opcija: "Docker (+ Docker Compose)", ker omogoča zagon celotne spletne aplikacije z enim samim ukazom (`docker compose up`). Docker Compose služi kot zaganjalnik aplikacije, ki deluje v treh vsebnikih, opredeljenih v `docker-compose.yml`:

* `db` – podatkovna baza PostgreSQL (slika `postgres:15-alpine`)
* `backend` – Flask strežnik (lastna slika iz `backend/Dockerfile`)
* `frontend` – spletni vmesnik (lastna slika iz `frontend/Dockerfile`)

Je edino okolje za zagon, s katerim imam že neke izkušnje.

### Pozitivne posledice
* Enaka konfiguracija vseh delov aplikacije za vse člane ekipe ne glede na operacijski sistem
* Izolacija storitev – ko aplikacije ne potrebujemo več, vsebnike enostavno ustavimo
* Možnost hitre ponovne vzpostavitve čiste baze med testiranjem v primeru konfliktov

### Negativne posledice
* Potrebna je namestitev orodja Docker Desktop, ki porabi precej sistemskega pomnilnika in diska
* Prvotna namestitev in sinhronizacija vseh delov aplikacije je kompleksna
