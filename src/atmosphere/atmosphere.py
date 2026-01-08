import numpy as np
import logging
from PIL import Image, ImageDraw
from typing import Tuple, Dict

# Configuration du Logger pour le projet PHACAV
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
LOGGER = logging.getLogger("PHACAV_E5")

class AtmosphereSimulator:
    """
    Simulateur atmosphérique dynamique pour l'Étape 5.
    Calcule la circulation des vents en couplant les données NASA (E1) 
    et la topographie (E2).
    """

    def __init__(self, planet_data: Dict, width: int = 1024, height: int = 512):
        self.width = width
        self.height = height
        
        # CALIBRATION PHYSIQUE 
        # Énergie : Plus l'étoile est lumineuse, plus les vents sont rapides
        star_lum = 10**planet_data.get('st_lum', 0) if planet_data.get('st_lum') else 1.0
        self.thermal_intensity = np.sqrt(star_lum) * 3.0
        
        # Rotation : La période orbitale (souvent synchrone) influence Coriolis
        # Plus la rotation est rapide (période courte), plus l'effet zonal est marqué
        rotation_period = planet_data.get('pl_orbper', 1.0) 
        self.coriolis_factor = 1.0 / np.sqrt(max(rotation_period, 0.1))

    def compute_atmospheric_circulation(self, topo_map: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcule les vecteurs U (Est-Ouest) et V (Nord-Sud).
        Le gradient de topo_map dévie les vents.
        """
        if topo_map.shape != (self.height, self.width):
            raise ValueError(f"Erreur E5: Topographie {topo_map.shape} incohérente.")

        LOGGER.info("Calcul des flux : Modèle de circulation globale dynamique...")

        # Analyse du relief (Gradient oographique)
        grad_y, grad_x = np.gradient(topo_map)

        # Création de la grille de latitude
        lats_rad = np.linspace(-np.pi/2, np.pi/2, self.height).reshape(-1, 1)
        lats_deg = np.abs(np.degrees(lats_rad))
        v_direction = np.sign(lats_rad) * np.ones((1, self.width))

        # Initialisation
        u_base = np.zeros((self.height, self.width))
        v_base = np.zeros((self.height, self.width))

        # --- MODÉLISATION DES CELLULES (Adaptée à la rotation) ---
        # Coefficient global combinant chaleur et rotation
        global_force = self.thermal_intensity * self.coriolis_factor

        # Zone Hadley (0-30°) : Alizés vers l'Ouest
        m_hadley = lats_deg < 30
        u_base[m_hadley] = -global_force
        v_base[m_hadley] = -v_direction[m_hadley] * (global_force * 0.3)

        # Zone Ferrel (30-60°) : Westerlies vers l'Est
        m_ferrel = (lats_deg >= 30) & (lats_deg < 60)
        u_base[m_ferrel] = global_force * 0.8
        v_base[m_ferrel] = v_direction[m_ferrel] * (global_force * 0.2)

        # Zone Polaire (>60°) : Vents d'Est froids
        m_polar = lats_deg >= 60
        u_base[m_polar] = -global_force * 0.6
        v_base[m_polar] = -v_direction[m_polar] * (global_force * 0.4)

        # COUPLAGE RELIEF (Interaction physique)
        # Le vent dévie selon la pente (gradient)
        u_final = u_base + (grad_y * global_force * 3.0)
        v_final = v_base - (grad_x * global_force * 3.0)

        return u_final, v_final


#FONCTIONS DE TEST ET MOCK DATA (Pour isolation)
def generate_mock_previous_steps() -> Tuple[Dict, np.ndarray]:
    """Simule E1 et E2 pour valider l'E5 sans attendre les autres groupes."""
    # Mock E1 : TRAPPIST-1 e
    mock_e1 = {"pl_name": "TRAPPIST-1 e", "st_lum": -2.28, "pl_orbper": 6.1}
    
    # Mock E2 : Topographie (Un continent et une montagne)
    w, h = 1024, 512
    y, x = np.ogrid[0:h, 0:w]
    # Un volcan géant au milieu pour tester la déviation des vents
    topo = np.exp(-((x - w//2)**2 / 15000 + (y - h//2)**2 / 15000))
    topo = (topo - topo.min()) / (topo.max() - topo.min())
    
    return mock_e1, topo

def render_e5_debug_pil(topo: np.ndarray, u: np.ndarray, v: np.ndarray):
    """Génère l'image de preuve visuelle via PIL uniquement."""
    #Fond : Relief
    topo_img = (topo * 255).astype(np.uint8)
    img = Image.fromarray(topo_img).convert("RGB")
    draw = ImageDraw.Draw(img)

    #Dessin des vecteurs (Jaune = Vent)
    step = 32
    for j in range(0, topo.shape[0], step):
        for i in range(0, topo.shape[1], step):
            # La direction montre si le vent contourne la montagne
            dx, dy = u[j, i] * 5, v[j, i] * 5
            draw.line((i, j, i + dx, j - dy), fill=(255, 255, 0), width=1)

    img.save("debug_etape5_concordance.png")
    LOGGER.info("Fichier 'debug_etape5_concordance.png' généré.")

# --- POINT D'ENTRÉE ---
if __name__ == "__main__":
    #Simulation des données entrantes
    data_nasa, map_topo = generate_mock_previous_steps()

    #Simulation Étape 5
    sim = AtmosphereSimulator(data_nasa)
    u_map, v_map = sim.compute_atmospheric_circulation(map_topo)

    # Rendu PIL
    render_e5_debug_pil(map_topo, u_map, v_map)