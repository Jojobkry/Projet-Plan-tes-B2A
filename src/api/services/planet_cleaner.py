# services/planet_cleaner.py

from core.model_planet import Planet

def clean_planets(raw_planets):
    """
    Nettoie les données brutes de planètes.
    - Garde seulement les champs essentiels
    - Supprime les planètes sans nom ou masse
    - Convertit les unités si nécessaire
    Retourne une liste de dictionnaires propres.
    """

    cleaned = []

    for p in raw_planets:
        try:
            name = p.get('name') or p.get('pl_name')
            mass = p.get('pl_masse')  # masse en masse terrestre
            radius = p.get('pl_rade')  # rayon en rayon terrestre
            distance = p.get('st_dist')  # distance en parsec ou autre

            # on ignore si une info critique est manquante
            if name is None or mass is None or radius is None:
                continue

            # conversion : Terre → kg et rayon → m
            mass_kg = mass * 5.972e24  # masse terrestre → kg
            radius_m = radius * 6371000  # rayon terrestre → m
            distance_km = distance * 3.086e13 if distance else None  # parsec → km

            planet = Planet(name=name, mass=mass_kg, radius=radius_m, distance=distance_km)
            cleaned.append(planet.__dict__)  # on garde dict pour JSON

        except Exception as e:
            # si une planète pose problème, on l'ignore
            print(f"⚠️ Planète ignorée: {p.get('name', 'unknown')} ({e})")
            continue

    return cleaned
