import numpy as np
import matplotlib.pyplot as plt

SIZE = 300  

# on peut aussi juste appeler la fonction main qui relie tout ce dont on n'a besoin s'il y en a

def normalize(data):
    return (data - data.min()) / (data.max() - data.min())
#On peut ici appeler la fonction qui calcul l'altitude
def generate_altitude(size):
    x = np.linspace(0, 1, size)
    y = np.linspace(0, 1, size)
    X, Y = np.meshgrid(x, y)
    
    altitude = (
        0.5 * np.sin(3 * np.pi * X) * np.sin(3 * np.pi * Y) +
        0.2 * np.sin(10 * np.pi * X) * np.cos(10 * np.pi * Y) +
        0.1 * np.random.normal(0, 0.1, (size, size)) # Bruit plus doux
    )
    return normalize(altitude)

#   on appele la fonction de la temperature
def generate_temperature(size, altitude):
    # Gradient de latitude (pôles froids, équateur chaud)
    latitude = np.linspace(-1, 1, size)
    lat_2d = np.abs(np.repeat(latitude[:, None], size, axis=1))
    
    # La température baisse avec l'altitude et la latitude
    temp = 1.0 - (0.6 * lat_2d + 0.4 * altitude)
    return np.clip(temp, 0, 1)

#on peut appeler ici la fonction de l'humidité
def generate_humidité(size, altitude, temperature):
    # Plus chaud + plus bas = souvent plus humide (proche océan)
    humidity = (1 - altitude) * 0.7 + (temperature) * 0.3
    humidity += np.random.normal(0, 0.05, (size, size))
    return np.clip(humidity, 0, 1)

# Couleurs normalisées (0 à 1 pour matplotlib)
COLORS = {
    "ocean":    [0.0, 0.3, 0.6],
    "forest":   [0.1, 0.5, 0.1],
    "plains":   [0.5, 0.7, 0.3],
    "desert":   [0.8, 0.7, 0.4],
    "mountain": [0.6, 0.6, 0.6],
    "tundra":   [0.8, 0.9, 1.0]
}

def get_biome_map(a, t, h):
    # Création d'une matrice vide pour les couleurs (R, G, B)
    map_rgb = np.zeros((SIZE, SIZE, 3))
    
    # On crée des masques booléens
    is_ocean    = a < 0.35
    is_mountain = (a >= 0.35) & (a > 0.75)
    is_tundra   = (a >= 0.35) & (a <= 0.75) & (t < 0.25)
    is_desert   = (a >= 0.35) & (a <= 0.75) & (t >= 0.25) & (h < 0.3)
    is_forest   = (a >= 0.35) & (a <= 0.75) & (t >= 0.25) & (h >= 0.3) & (h > 0.6)
    is_plains   = (a >= 0.35) & (a <= 0.75) & (t >= 0.25) & (h >= 0.3) & (h <= 0.6)

    # Application des couleurs par masque
    map_rgb[is_ocean]    = COLORS["ocean"]
    map_rgb[is_mountain] = COLORS["mountain"]
    map_rgb[is_tundra]   = COLORS["tundra"]
    map_rgb[is_desert]   = COLORS["desert"]
    map_rgb[is_forest]   = COLORS["forest"]
    map_rgb[is_plains]   = COLORS["plains"]
    
    return map_rgb

# Pipeline d'exécution
alt = generate_altitude(SIZE)
temp = generate_temperature(SIZE, alt)
hum = generate_humidité(SIZE, alt, temp)
img = get_biome_map(alt, temp, hum)

plt.figure(figsize=(8, 8))
plt.imshow(img, interpolation='bilinear') # 'bilinear' adoucit les transitions
plt.title("Génération de Biomes Optimisée")
plt.axis("off")
plt.show()