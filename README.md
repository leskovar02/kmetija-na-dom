# Kmetija na dom

### Opis

Kmetija na dom je spletna aplikacija in storitev, ki neposredno poveže kmete s kupci njihovih pridelkov oziroma izdelkov. Skozi aplikacijo je možno izbirati kmetije, brskati po inventarju izbrane kmetije, filtrirati izdelke glede na dane kriterije ter naročevati le-te.

Ob oddanem narpčilu kmet pripravi njegovo vsebino ter pozove kupca za prevzem. Ta nato obišče kmetijo in prevzame naročene artikle.

Namen aplikacije je omogočanje kupcem nakupa sveže, doma pridelane hrane, ki ne prepotuje velikih razdalj, ter kmetom omogočiti pravičen zaslužek.

### Uporabljene tehnologije

HTML5, CSS, Jinja, Python (+ venv), Flask (+ Flash-Session), PostgreSQL, Docker, Git

### Dokumentacija 

Za dostop in uporabo celotne spletne plikacije so potrebni naslednji koraki:
1) Pull iz GitHuba na svoj osebni računalnik
2) Odprite cmd / terminalno okno v direktoriju mape, ki je bila prenesena z GitHuba
3) Potrebno je zagnati Docker Desktop z komando `docker desktop start`
4) Nato je potrebno pognati Docker kontejner, ki zažene vse vsebnike z komando `docker compose up`
5) Po končanem zagonu odpremo katerikoli brskalnik in v naslovno vrstico vnesemo `http://localhost`, če se ta ne odzove poskusimo na `http://localhost:5000`
6) Zdaj bi morali videti naslovno stran spletne aplikacije v katero lahko vstopimo
7) Da vse skupaj ugasnemmo izvršimo komandi `docker compose stop` ali `docker compose down`, če želimo umakniti kontejner in njegove vsebnike z računalnika, na koncu pa še `docker desktop stop` za zaustavitev Docker pogona