import sys
import os

# Force Python à considérer le dossier racine comme racine des modules
sys.path.insert(0, os.path.abspath('.'))

from steps.step1_cleaning import run_step1

if __name__ == "__main__":
    run_step1(limit=5)  # limite pour test
