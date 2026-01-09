import numpy as np
import matplotlib.pyplot as plt
import requests

# PARAMÈTRES CONFIGURABLES

SCALE = 50.0
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0

WIDTH = 2048
HEIGHT = 1024
MAX_LAT = 85

# DONNÉES NASA

def load_planet():
    url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"
    params = {
        "table": "ps",
        "select": "pl_name",
        "where": "pl_name like 'TRAPPIST-1%'",
        "format": "json"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (PlanetaryMapping/1.0)"
    }

    r = requests.get(url, params=params, headers=headers, timeout=20)

    # Vérification robuste
    if r.status_code != 200:
        print("⚠️ API NASA indisponible, utilisation valeur locale")
        return "TRAPPIST-1 e"

    try:
        data = r.json()
        if not data:
            raise ValueError("JSON vide")
        return data[0]["pl_name"]
    except Exception as e:
        print("⚠️ Erreur JSON NASA, fallback local :", e)
        return "TRAPPIST-1 e"

planet_name = load_planet()

# BRUIT FRACTAL NUMPY 

def fractal_noise(shape, scale, octaves, persistence, lacunarity):
    noise = np.zeros(shape)
    frequency = 1.0
    amplitude = 1.0

    for _ in range(octaves):
        noise += amplitude * np.random.rand(*shape)
        frequency *= lacunarity
        amplitude *= persistence

    return noise / noise.max()

# GRILLE MERCATOR

lon = np.linspace(-np.pi, np.pi, WIDTH)
lat = np.linspace(np.deg2rad(-MAX_LAT), np.deg2rad(MAX_LAT), HEIGHT)
lon, lat = np.meshgrid(lon, lat)

heightmap = fractal_noise(
    (HEIGHT, WIDTH),
    SCALE,
    OCTAVES,
    PERSISTENCE,
    LACUNARITY
)

# AFFICHAGE MERCATOR

plt.figure(figsize=(16, 8))
plt.imshow(
    heightmap,
    cmap="terrain",
    extent=[-180, 180, -MAX_LAT, MAX_LAT]
)

plt.colorbar(label="Relief procédural")
plt.xlabel("Longitude (°)")
plt.ylabel("Latitude (°)")
plt.title(f"{planet_name} — Projection de Mercator (plate)")

plt.tight_layout()
plt.show()
