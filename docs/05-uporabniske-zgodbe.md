## US-01

**Povezana funkcionalnost:** Registracija in prijava uporabnikov (kupec ali kmetovalec)

**Uporabniška vloga:** Novi obiskovalec / Uporabnik

**Uporabniška zgodba:** Kot nov obiskovalec se želim registrirati in prijaviti v platformo kot kupec ali kmetovalec, da lahko dostopam do funkcionalnosti, prilagojenih moji vlogi.

**Acceptance criteria:**
1) Obrazec za registracijo zahteva vnos imena, priimka, veljavnega e-poštnega naslova, gesla in izbiro vloge (kupec ali kmetovalec).
2) Sistem preveri, ali je e-poštni naslov že registriran, in v primeru podvajanja prikaže ustrezno sporočilo o napaki.
3) Gesla se v podatkovni bazi shranjujejo v zgoščenljeni obliki z uporabo knjižnice bcrypt.
4) Po uspešni prijavi je uporabnik preusmerjen na ustrezno začetno stran glede na svojo vlogo.


## US-02

**Povezana funkcionalnost:** Upravljanje zaloge lastnih pridelkov (dodajanje, urejanje, brisanje izdelkov s slikami, opisom in trenutno zalogo)

**Uporabniška vloga:** Kmetovalec

**Uporabniška zgodba:** Kot kmetovalec želim dodajati, urejati in brisati lastne pridelke s slikami, opisom in trenutno zalogo, da lahko kupcem ponudim ažurne informacije o svoji ponudbi.

**Acceptance criteria:** 
1) Kmetovalec lahko doda nov izdelek z vnosom naziva, opisa, cene, enote količine (npr. kg, kos), začetne zaloge in slike izdelka. Za nediskretne količine za diskretno določljive enote (kg) veljajo navedene količine kot zgornje meje &plusmn; 200g. 
2) Kmetovalec lahko kadarkoli spremeni obstoječe podatke o izdelku ali posodobi trenutno zalogo.
3) Kmetovalec lahko izbriše izdelek iz svoje ponudbe, pri čemer se izdelek odstrani iz aktivnega pregleda za kupce.
4) Sistem prepreči vnos negativnih vrednosti za ceno in zalogo.


## US-03

**Povezana funkcionalnost:** Brskanje in napredno filtriranje izdelkov po kategorijah, ceni, tipu, oddaljenosti...

**Uporabniška vloga:** Kupec

**Uporabniška zgodba:** Kot kupec želim brskati in napredno filtrirati izdelke po kategorijah, ceni, tipu in oddaljenosti, da hitro najdem želene pridelke v svoji bližini.

**Acceptance criteria:**
1) Kupec lahko filtrira seznam izdelkov po cenovnem razponu z vnosom minimalne in maksimalne cene.

2) Kupec lahko filtrira izdelke glede na tip kmetije ali kategorijo pridelkov.

3) Seznam rezultatov se dinamično posodobi in prikaže le izdelke, ki ustrezajo izbranim kriterijem.

4) Prikazani rezultati vključujejo naziv izdelka, ceno, enoto in naziv pripadajoče kmetije.


## US-04

**Povezana funkcionalnost:** Oddaja naročila

**Uporabniška vloga:** Kupec

**Uporabniška zgodba:** Kot kupec želim oddati naročilo za izbrane izdelke s posamezne kmetije, da si zagotovim nakup sveže hrane.

**Acceptance criteria:**
1) Kupec lahko doda izdelke v košarico in pred oddajo vidi izračunan skupni znesek naročila.

2) Sistem ob oddaji naročila preveri razpoložljivo zalogo in zavrne naročilo, če naročena količina presega trenutno zalogo izdelka.

3) Uspešno oddano naročilo se shrani v podatkovno bazo z začetnim statusom ob uri oddaje naročila ter se poveže s kupcem in kmetijo.

4) Kupec po oddaji naročila vidi potrditveni zaslon s povzetkom naročila in podatki o prevzemu.


## US-05

**Povezana funkcionalnost:** Pregled in spreminjanje statusa naročil s strani kmetovalca (potrjeno, v pripravi, za prevzem, zaprto)

**Uporabniška vloga:** Kmetovalec

**Uporabniška zgodba:** Kot kmetovalec želim pregledovati in spreminjati status prejetih naročil (potrjeno, v pripravi, za prevzem, zaprto), da kupca in sebe vodim skozi proces priprave.

**Acceptance criteria:**
1) Kmetovalec ima pregled nad vsemi prejetimi naročili z navedenimi podrobnostmi o naročenih izdelkih in kupcu.

2) Kmetovalec lahko posodobi status naročila na enega od dovoljenih stanj: potrjeno, v pripravi, za prevzem ali zaprto.

3) Sprememba statusa se nemudoma shrani v podatkovno bazo in se osveži v vmesniku.

4) Kmetovalec lahko spreminja status izključno naročil, ki pripadajo njegovi kmetiji.


## US-06

**Povezana funkcionalnost:** Sistem ocenjevanja kupljenih izdelkov in kmetij

**Uporabniška vloga:** Kupec

**Uporabniška zgodba:** Kot kupec želim oceniti kakovost kupljenih izdelkov in interakcijo s kmetijo, da delim svoje izkušnje in pomagam drugim kupcem.

**Acceptance criteria:**
1) Kupec lahko odda oceno (številčna vrednost od 1 do 5) in besedilni komentar za kmetijo šele, ko je status naročila nastavljen na "zaprto" in je od le-tega preteklo 24 ur.

2) istem prepreči oddajo več ocen za isto zaključeno naročilo s strani istega kupca.

2) Povprečna ocena kmetije se samodejno izračuna na podlagi vseh oddanih ocen in se prikaže na profilu kmetije.

2) Vse oddane ocene in komentarji so javno vidni na profilu posamezne kmetije.


## US-07

**Povezana funkcionalnost:** Generiranje osnovnih poročil o prodaji in prihodkih za kmetovalce

**Uporabniška vloga:** Kmetovalec

**Uporabniška zgodba:** Kot kmetovalec želim generirati osnovna poročila o prodaji in prihodkih, da lahko analiziram uspešnost svojega poslovanja na platformi.

**Acceptance criteria:**
1) Poročilo prikazuje skupni prihodek in število prodanih enot za izbrano časovno obdobje.

2) Podatki v poročilu se izračunajo izključno na podlagi naročil s statusom "zaprto" za prijavljeno kmetijo.

3) Poročilo vključuje tudi razčlenitev prodaje po posameznih izdelkih.


## US-08

**Povezana funkcionalnost:** Interaktivni seznam in pregled lokacij kmetij

**Uporabniška vloga:** Kupec

**Uporabniška zgodba:** Kot kupec želim pregledovati seznam in lokacije kmetij, da lažje izberem kmetije v svoji geografski bližini.

**Acceptance criteria:**
1) Sistem prikaže le seznam vseh potrjenih kmetij z navedenimi fizičnimi naslovi, opisi in uradnim potrdilom statusa kmeta.

2) Kupec lahko izbere posamezno kmetijo iz seznama in si ogleda njene podrobnosti ter ponudbo.

3) Prikazane so izključno tiste kmetije, katerih verodostojnost je potrdil administrator.


## US-09

**Povezana funkcionalnost:** Avtomatsko obveščanje kupcev prek e-pošte o spremembi statusa naročila

**Uporabniška vloga:** Kupec

**Uporabniška zgodba:** Kot kupec želim prejeti avtomatsko e-poštno obvestilo ob spremembi statusa mojega naročila, da sem vedno obveščen o napredku priprave.

**Acceptance criteria:**
1) Sistem samodejno pošlje e-poštno sporočilo kupcu takoj, ko kmetovalec spremeni status naročila (npr. v "potrjeno/zavrnjeno", "v pripravi" ali "za prevzem").

2) E-poštno sporočilo vsebuje ID naročila, trenutni status in osnovna navodila za prevzem.

3) Sporočilo se posreduje na e-poštni naslov, s katerim je kupec registriran v sistemu.


## US-10

**Povezana funkcionalnost:** Shranjevanje priljubljenih kmetij in izdelkov

**Uporabniška vloga:** Kupec

**Uporabniška zgodba:** Kot kupec želim shranjevati priljubljene kmetije in izdelke na svoj seznam, da lahko hitreje dostopam do njih pri naslednjih nakupih.

**Acceptance criteria:**
1) Kupec lahko z gumbom za priljubljene doda kmetijo ali izdelek na svoj osebni seznam.

2) Kupec ima na svojem profilu namensko stran za pregled vseh shranjenih priljubljenih kmetij in izdelkov.

3) Kupec lahko poljuben element odstrani s seznama priljubljenih.

4) Seznam priljubljenih je vezan izključno na račun prijavljenega kupca.


## US-11

**Povezana funkcionalnost:** Upravljanje certifikatov kakovosti (npr. ekološki pridelki) na profilu kmetije

**Uporabniška vloga:** Kmetovalec

**Uporabniška zgodba:** Kot kmetovalec želim upravljati certifikate kakovosti na profilu svoje kmetije, da kupcem dokažem verodostojnost in visoko kakovost svojih pridelkov.

**Acceptance criteria:**
1) Kmetovalec lahko na svoj profil doda podatke o certifikatu kakovosti (naziv certifikata in opis).

2) Kmetovalec lahko ureja ali briše obstoječe certifikate na svojem profilu.

3) Dodani certifikati so javno vidni vsem kupcem na profilu posamezne kmetije.

4) Kmetovalec lahko ureja certifikate le na profilu, ki je povezan z njegovim računom.


## US-12

**Povezana funkcionalnost:** Administracijski pregled platforme, statistik

**Uporabniška vloga:** Administrator

**Uporabniška zgodba:** Kot administrator želim dostopati do administracijskega pregleda platforme in splošnih statistik, da nadzorujem delovanje sistema in potrjujem verodostojnost kmetij.

**Acceptance criteria:**
1) Administrator ima dostop do namenske nadzorne plošče s prikazom splošnih statistik delovanja platforme (število uporabnikov, aktivnih kmetij in naročil).

2) Administrator lahko z enim klikom potrdi verodostojnost novo registrirane kmetije, s čimer kmetija postane vidna javnosti.

3) Administrator lahko izbriše uporabniški račun v primeru kršitve pravil platforme.

4) Uporabniki z vlogo kupca ali kmetovalca nimajo dostopa do administracijske nadzorne plošče.

5) Administrator ne skrbi za pozabljene prijavne podatke.