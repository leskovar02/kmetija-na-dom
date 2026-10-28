---
status: sprejeto
datum: 27-10-2026
---

# Uporaba ogrodja Flask (+ Flask-Session)

## Kontekst in problem
Izbrati moramo spletno ogrodje za usmerjanje HTTP zahtev ter varen način upravljanja uporabniških sej in preverjanja pravic glede na vloge.

## Dejavniki odločanja
* Nizek prag učenja za postavitev prve spletne aplikacije
* Popolna kontrola nad projektom brez nepotrebne navlake
* Enostavno in varno upravljanje sej prijavljenih uporabnikov
* Izogibanje kompleksnim ogrodjem

## Obravnavane možnosti
* Flask
* Django
* Laravel

## Sprejeta odločitev in utemeljitev
Izbrana opcija: "Flask", ker je Flask mikro-ogrodje, ki zagotavlja le bistvene elemente za delo s spletnimi zahtevami (usmerjanje/routing, obdelava zahtev in odgovorov), brez kompleksne strukture. Knjižnica "Flask-Session" dodaja podporo za varno shranjevanje sej na strežniški strani, kar omogoča preprosto preverjanje avtentikacije ter uporabniških vlog.

Za nekoga, ki prvič dela s spletnim ogrodjem, je Flask idealen, zaradi njegove obežnosti. Ima enostavejnšo osnovno konfiguracijo napram ostalim ogrodjem.

### Pozitivne posledice
* Izjemno hiter začetek razvoja in svoboda pri organizaciji
* Majhna poraba sistemskih virov zaradi "okrnjenosti"
* Enostavna implementacija funkcij za preverjanje prijavljenih uporabnikov in vlog

### Negativne posledice
* Ker ogrodje nima vgrajenih vseh orodij (npr. za obrazce ali baze), je treba ročno izbrati in povezati dodatne knjižnice
* Zaradi svobode lahko koda postane nepregledna v primeru nekonsistentnega vzdrževanja