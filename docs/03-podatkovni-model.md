# Podatkovni model

## Entitete

1) Uporabnik (generalen)
    - id (PK)
    - ime
    - priimek
    - email
    - geslo
    - vloga (kupec, kmetovalec, admin)

2) Kmetija
    - id (PK)
    - kmetovalec_id (FK -> povezano z Uporabnik.id, kjer je vloga kmetovalec)
    - naziv
    - informacije (tip, sezona obratovanja...)
    - fizični naslov

3) Izdelek (Product)
    - id (PK)
    - kmetija_id (FK -> povezano s tabelo Kmetija)
    - naziv
    - opis
    - cena (trenutna cena na enoto)
    - enota količine (kg, kos, liter...)
    - zaloga (trenutno razpoložljiva količina v enoti izdelka)

4) Naročilo (Order)
    - id (PK)
    - kupec_id (FK -> povezano z Uporabnik.id, kjer je vloga kupec)
    - kmetija_id (FK -> povezano s tabelo Kmetija; vsako naročilo pripada natanko eni kmetiji)
    - datum_naročila
    - status (čaka na potrditev, potrjeno, zavrnjeno, v pripravi, za prevzem, zaprto)
    - skupni_znesek

5) Naročilo Izdelek (OrderItem - Vmesna tabela za relacijo M:N)
    - id (PK)
    - naročilo_id (FK -> povezano s tabelo Naročilo)
    - izdelek_id (FK -> povezano s tabelo Izdelek)
    - količina (naročena količina tega izdelka v enoti izdelka)
    - cena_na_enoto (cena izdelka ob oddaji naročila, da kasnejša sprememba cene ne spremeni preteklih naročil)

## Stanja naročila

čaka na potrditev → potrjeno / zavrnjeno → v pripravi → za prevzem → zaprto

- Novo naročilo dobi stanje "čaka na potrditev".
- Kmetovalec naročilo potrdi ("potrjeno") ali zavrne ("zavrnjeno"). "Zavrnjeno" je končno stanje.
- Potrjeno naročilo gre v "v pripravi", nato "za prevzem", po prevzemu pa v "zaprto".

## Povezave med entitetami

| Entiteta 1 | Tip relacije | Entiteta 2 |
|----:|:----:|:----|
| Uporabnik (kmetovalec) | 1 : 1 | Kmetija |
| Kmetija | 1 : N | Izdelek |
| Kmetija | 1 : N | Naročilo |
| Uporabnik (kupec) | 1 : N | Naročilo |
| Naročilo | 1 : N | Naročilo Izdelek |
| Izdelek | 1 : N | Naročilo Izdelek |

Naročilo in Izdelek sta tako povezana v relaciji M : N preko vmesne tabele Naročilo Izdelek.
