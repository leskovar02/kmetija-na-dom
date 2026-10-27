# Tehnične specifikacije

## Arhitektura

### Glavni deli sistema

1) Frontend (Jinja): Uporabniški vmesnik v brskalniku, ki skrbi za prikaz podatkov in interakcijo z uporabnikom

2) Backend (Flask): Strežniška aplikacija, ki obdeluje poslovno logiko

3) Database (PostgreSQL): Relacijska podatkovna baza za trajno hranjenje podatkov

### Komunikacija med deli

Komunikacija poteka v frontendu prek GET in POST metod, strežnik pa jih obdela, preveri pravice in vrne generirano HTML stran.

### Podatkovna baza

Uporabljena bo podatkovna baza PostgreSQL. Je klasična relacijska podatkovna baza, ki ustreza našim potrebam.

### Avtentikacija

Uporabniške seje se upravljajo preko Session-based authentication s piškotki v kombinaciji z Flask-Login, kar omogoča zelo preprosto preverjanje vlog. Gesla se shranjujejo v zgoščenljeni obliki z uporabo knjižnice bcrypt.

### Lokalni zagon

Aplikacija se lokalno zažene preko Docker.

## Tehnološki sklad

1) Frontend: Jinja, CSS
    - Jinjo uporabljamo, ker je template za Python, ki je tudi podlaga za flask. Jinja omogoča fleksibilnost, ki je sicer nimamo. CSS za uporabo urejanja izgleda kot zunanjega stylesheeta zaradi preglednosti kode in datotečnega sistema.

2) Backend: Python, Flask
    - Za Python sem se odločil, ker mi je ljubši kot javaScript ter ga bolje razumem. Zaradi tega tudi Flask, saj je Python-based in lahka knjižnica zaradi česar se mi je tudi zdela primerna izbira za začetek - nikoli še nisem delal s ogrodji, le surovo kodo jS, HTML, php, CSS.

3) Podatkovna baza: PostgreSQL
    - Izbira te podatkovne baze temelji na njeni definiciji kot relacijska podatkovna baza ter podpora ORM.

4) Avtentikacija: Na podlagi seje in Flask-Login
    - Enostavnejša hramba seje in prijavnega sistema ter razdelitev in identifikacija vlog uporabnikov.

5) Lokalni razvoj: Docker
    - Edino kar poznam od takšnih orodij

6) Drugo: git, GitHub
    - Uporaba kot backup za skrajne primere ter lažje sledenje spremembam, lažje testiranje večih različic
