# services/nasa_client.py
import requests

API_URL = "https://api.arcsecond.io/exoplanets/"

def fetch_all_exoplanets(limit: int = 5):
    """
    Récupère un nombre limité de planètes depuis l'API.
    Ne garde que les champs essentiels.
    """
    response = requests.get(API_URL)
    if response.status_code != 200:
        raise Exception(f"Erreur API : {response.status_code}")

    data = response.json()  # ici data est déjà une liste

    essential_fields = ['name', 'pl_name', 'pl_masse', 'pl_rade', 'st_dist']

    planets = []
    for p in data[:limit]:  # prend juste les `limit` premières planètes
        filtered = {k: p.get(k) for k in essential_fields if k in p}
        planets.append(filtered)

    return planets


if __name__ == "__main__":
    planets = fetch_all_exoplanets()
    for p in planets:
        print(p)
