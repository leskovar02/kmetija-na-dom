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
    - kmetovalec id (FK -> povezano z Uporabnik.id, kjer je vloga kmetovalec)
    - naziv
    - informacije (tip, sezona obratovanja...)
    - fizični naslov

3) Izdelek (Product)
    - id (PK)
    - kmetija id (FK -> povezano s tabelo Kmetija)
    - naziv
    - opis
    - cena
    - količina (količina tega specifičnega izdelka v naročilu)
    - enota količine (kg, kos, liter...)
    - zaloga

4) Naročilo (Order)
    - id (PK)
    - kupec_id (FK -> povezano z Uporabnik.id, kjer je vloga kupec)
    - datum_naročila
    - status (npr. v teku, potrjeno, zaključeno)
    - skupni_znesek

5) Naročilo Izdelek (OrderItem - Vmesna tabela za relacijo M:N)
    - id (PK)
    - naročilo_id (FK -> povezano s tabelo Naročilo)
    - izdelek_id (FK -> povezano s tabelo Izdelek)
    
## Povezave med entitetami

| Entiteta 1 | Tip relacije | Entiteta 2 |
|----:|:----:|:----|
| Uporabnik (kmetovalec) | 1 : N | Izdelek |
| Uporabnik (kmetovalec) | 1 : 1 | Kmetija |
| Uporabnik (kupec) | 1 : N | Naročilo |
| Naročilo | 1 : N | Naročilo Izdelek |
| Izdekel | 1 : N | Naročilo Izdelek |
