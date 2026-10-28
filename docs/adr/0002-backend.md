---
status: sprejeto
datum: 27-10-2026
---

# Izbira jezika Python (+ venv) za zaledje

## Kontekst in problem
Potrebujemo stabilen programski jezik za pisanje poslovne logike na strežniku ter mehanizem za izolacijo programskih paketov in odvisnosti projekta.

## Dejavniki odločanja
* Čitljivost in sintaktična preprostost kode
* Enostavno upravljanje odvisnosti projekta brez vpliva na sistemske pakete računalnika
* Širok ekosistem razpoložljivih knjižnic za spletni razvoj
* Izogibanje JavaScriptu

## Obravnavane možnosti
* Python z virtualnim okoljem venv
* Klasičen PHP + JavaScript

## Sprejeta odločitev in utemeljitev
Izbrana opcija: "Python z virtualnim okoljem venv", ker Python jasno in čisto sintakso, venv pa ustvari popolnoma izolirano okolje za namestitev knjižnic. To zagotavlja, da so vse odvisnosti projekta zaklenjene znotraj lokalne mape in ne prihaja do konfliktov z drugimi projekti ali sistemskimi različicami Python paketov.

Python je kot prvi jezik za spletni backend odlična izbira, saj imam z njim več prakse kot JavaScriptom in PHP-jem. Kot jezik mi je tudi bolj všeč. Uporaba venv pa enostavno prereči konflikte z ostalimi deli sistema.

### Pozitivne posledice
* Visoka hitrost razvoja in lažje odpravljanje napak
* Enostavno prenašanje projekta med različnimi računalniki z uporabo datoteke "requirements.txt".
* Zaščita lokalnega operacijskega sistema pred nezdružljivimi različicami paketov

### Negativne posledice
* Python je interpretiran jezik, kar pomeni nižjo hitrost izvajanja v primerjavi s prevajanimi jeziki
* Razvijalec mora ročno poskrbeti za vklop virtualnega okolja pred začetkom dela v terminalu
* Ni podprt za večnitne aplikacije