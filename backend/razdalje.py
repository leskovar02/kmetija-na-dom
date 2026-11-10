import heapq

from models import Povezava


def razdalje_od(zacetni_kraj_id):
    # graf #
    sosedi = {}
    for p in Povezava.query.all():
        km = float(p.razdalja_km)
        sosedi.setdefault(p.kraj_a_id, []).append((p.kraj_b_id, km))
        sosedi.setdefault(p.kraj_b_id, []).append((p.kraj_a_id, km))

    # dijkstra algo #
    razdalje = {zacetni_kraj_id: 0.0}
    vrsta = [(0.0, zacetni_kraj_id)]

    while vrsta:
        razdalja, kraj = heapq.heappop(vrsta)
        if razdalja > razdalje.get(kraj, float("inf")):
            continue

        for sosed, km in sosedi.get(kraj, []):
            nova = razdalja + km
            if nova < razdalje.get(sosed, float("inf")):
                razdalje[sosed] = nova
                heapq.heappush(vrsta, (nova, sosed))

    return razdalje
