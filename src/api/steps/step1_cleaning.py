from services.nasa_client import fetch_all_exoplanets
from services.planet_cleaner import clean_planets
from services.planet_repository import (
    save_raw_planets,
    save_cleaned_planets
)


def run_step1(limit: int | None = None):
    """
    Pipeline complet de l'étape 1 :
    - récupération NASA
    - nettoyage
    - sauvegarde
    """

    print(" Récupération des données NASA...")
    raw_planets = fetch_all_exoplanets(limit=limit)

    print(" Sauvegarde des données brutes...")
    save_raw_planets(raw_planets)

    print(" Nettoyage des données...")
    cleaned_planets = clean_planets(raw_planets)

    print(" Sauvegarde des données nettoyées...")
    save_cleaned_planets(cleaned_planets)

    print("✅ Étape 1 terminée avec succès.")


if __name__ == "__main__":
    run_step1()
