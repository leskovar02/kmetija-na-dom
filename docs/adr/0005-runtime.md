---
status: sprejeto
datum: 27-10-2026
---

# Uporaba orodja Docker za lokalni zagon podatkovne baze

## Kontekst in problem
Zagotoviti moramo enostaven, hiter in ponovljiv zagon PostgreSQL strežnika v lokalnem razvojnem okolju brez kompleksnih ročnih namestitev.

## Dejavniki odločanja
* Enostavna vzpostavitev enakega razvojnega okolja na različnih računalnikih in operacijskih sistemih
* Izogibanje ročni namestitvi in konfiguraciji strežnika podatkovne baze neposredno na operacijski sistem
* Hitro ponastavljanje ali brisanje testnih podatkov

## Obravnavane možnosti
* Docker
* Kubernetes

## Sprejeta odločitev in utemeljitev
Izbrana opcija: "Docker", ker omogoča zagon celotne spletne aplikacije znotraj izoliranega vsebnika z enim samim ukazom. Poenostavi konfiguracijo in namestitev baze na lokalnem računalniku.

Je edino okolje za zagon, s katerim imam že neke izkušnje.

### Pozitivne posledice
* Enaka konfiguracija baze za vse člane ekipe ne glede na operacijski sistem
* Izolacija storitve – ko baze ne potrebujemo več, vsebnik enostavno ustavimo
* Možnost hitre ponovne vzpostavitve čiste baze med testiranjem v primeru konflikotv

### Negativne posledice
* Potrebna je namestitev orodja Docker Desktop, ki porabi precej sistemskega pomnilnika in diska
* Prvotna namestitev in sinhronizacija vseh delov aplikacije je kompleksna