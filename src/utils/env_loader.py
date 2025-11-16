# src/utils/env_loader.py
import os
from dotenv import load_dotenv

# On charge le fichier .env situé à la racine du projet
# Path automatique : remonte un cran depuis ce fichier
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", ".env")

load_dotenv(env_path)

def get_env(key: str, default=None):
    """Récupère une variable du .env"""
    return os.getenv(key, default)
