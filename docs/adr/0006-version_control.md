---
status: sprejeto
datum: 27-10-2026
---

# Uporaba sistema Git (+ GitHub) za kotrolo verzij

## Kontekst in problem
Potrebujemo sistem za sledenje zgodovini sprememb v kodi, varovanje pred izgubo dela ter omogočanje varnega preizkušanja novih funkcionalnosti.

## Dejavniki odločanja
* Sledenje vsem spremembam v kodi skozi čas z možnostjo povratka na prejšnje delujoče stanje
* Varno shranjevanje kode na oddaljenem strežniku
* Vzdrževanje dobre prakse

## Obravnavane možnosti
* Git (+ GitHub)

## Sprejeta odločitev in utemeljitev
Izbrana opcija: "Git (+ GitHub)", ker gre za industrijski standard sledenja verzijam kode. Git omogoča lokalno shranjevanje verzij, ustvarjanje vej za razvijanje posameznih funkcionalnosti ter enostaven vpogled v zgodovino sprememb ali odpravljanje napak. GitHub deluje kot varnostna kopija v primeru okvar ali težav lokalnega računalnika.

### Pozitivne posledice
* Popolna zgodovina vseh sprememb z opisi in možnostjo povrnitve na starejše različice
* Izolirano testiranje funkcionalnosti v ločenih vejah brez vpliva na glavno
* Enostavno varnostno kopiranje projekta na oddaljen strežnik

### Negativne posledice
* Potrebno reševanje težav v primeru pull konflikotv ali zrušitve GitHub-ove storitve