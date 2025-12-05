import pandas as pd
import numpy as np
from datetime import datetime
import re

# ==========================================================
# Sujet 1 : RH & "People Analytics" (Focus Sécurité & RGPD)
# ==========================================================

# =========
# Partie 1
# =========

# ===================================================
# 1.1 Ingestion du fichier
# Lecture simple avec pandas.read_csv()
# ===================================================
df = pd.read_csv("./ingestion_et_nettoyage/employees_raw.csv")

# ===================================================
# 1.2 Nettoyage des emails
# Identification et suppression des emails invalides
# ===================================================

# Regex email standard
email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# Flag emails valides
df["email_valide"] = df["email"].astype(str).str.match(email_regex)

# Séparation (on garde uniquement les valides)
emails_invalides = df[~df["email_valide"]]
df = df[df["email_valide"]].drop(columns=["email_valide"])


# ==================================================================================
# 1.3 Nettoyage salaire brut
# Suppression lettres/symboles/espaces
# Extraction chiffres purs
# Conversion en int
# ==================================================================================

def nettoyer_salaire(v):
    if pd.isna(v):
        return np.nan
    v = str(v)
    v = v.replace("EUR", "").replace("€", "").replace(",", "").strip()
    v = re.sub(r"[^\d]", "", v)  # supprime tout sauf chiffres
    return int(v) if v.isdigit() else np.nan

df["salaire_brut"] = df["salaire_brut"].apply(nettoyer_salaire)

# =================================================================
# 1.4 Harmonisation date embauche
# Conversion en datetime avec gestion des erreurs
# Suppression dates incohérentes avant 1970/Après la date actuelle
# =================================================================

# Si la valeur est manquante, on retourne une date nulle (NaT), on enlève les espaces + converti en string + liste des formats de dates observés dans le fichier brut
def nettoyer_date(d):
    if pd.isna(d):
        return pd.NaT
    s = str(d).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",  
        "%Y-%m-%d",           
        "%d/%m/%Y",           
        "%d-%m-%Y",           
        "%Y.%m.%d",           
    ]

    # On parse le texte avec chacun des formats, si échec, on tente le format suivant, si aucun format ne fonctionne = date invalide
    for fmt in formats:
        try:
            return pd.to_datetime(s, format=fmt)
        except ValueError:
            pass
    return pd.NaT

# Application de la fonction à la colonne 'date_embauche'
df["date_embauche"] = df["date_embauche"].apply(nettoyer_date)

# Filtrage des dates incohérentes
# Pas de dates avant 1980 (fusion récente), pas de dates après aujourd'hui
df = df[
    (df["date_embauche"] >= pd.Timestamp("1980-01-01")) &
    (df["date_embauche"] <= pd.Timestamp.today())
]

# Formatage final au format ISO (YYYY-MM-DD)
df["date_embauche"] = df["date_embauche"].dt.strftime("%Y-%m-%d")

# ==========================
# Partie 1. Résultats finaux
# ==========================

print("Emails invalides détectés :", len(emails_invalides))
print("Aperçu dataset nettoyé :")
print(df.head(10))


# =========
# Partie 2
# =========

import hashlib

# =========================================================
# 2. Sécurité & Anonymisation
# =========================================================

# =========================================================================
# 2.1 Création d'un Hash_ID unique à partir de nom + prenom + secu_sociale
# =========================================================================
def make_hash_id(row):
    """
    Construit un identifiant anonymisé et unique pour chaque employé
    à partir de nom + prenom + secu_sociale.
    On utilise SHA-256 pour avoir un hash irréversible.
    """
    nom = str(row.get("nom", "")).strip()
    prenom = str(row.get("prenom", "")).strip()
    secu = str(row.get("secu_sociale", "")).strip()

    base = f"{nom}_{prenom}_{secu}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

# Application du hash sur chaque ligne
df["hash_id"] = df.apply(make_hash_id, axis=1)

# ========================================================================
# 5.2 Masquage du numéro de sécurité sociale (2 derniers chiffres gardés)
# ========================================================================
def mask_secu(value):
    """
    Masque la secu_sociale en ne laissant visibles que les 2 derniers chiffres.
    Exemple : 158046912327970 -> *************70
    """
    if pd.isna(value):
        return np.nan
    # On force en string et on enlève les espaces
    s = str(value).replace(" ", "").strip()
    if len(s) <= 2:
        # Si très court, on remplace tout par des *
        return "*" * len(s)
    # On masque tout sauf les 2 derniers caractères
    return "*" * (len(s) - 2) + s[-2:]

# Nouvelle colonne masquée
df["secu_sociale_masked"] = df["secu_sociale"].apply(mask_secu)

# ============================================================
# 5.3 Fonction de filtrage par rôle (Admin / Manager / Autre)
# ============================================================
def get_dataset_by_role(df_source: pd.DataFrame, role: str) -> pd.DataFrame:
    """
    Retourne une vue du dataset filtrée selon le rôle :
      - Admin   : voit toutes les colonnes (incluant secu_sociale)
      - Manager : ne voit PAS les colonnes secu_sociale*, ni nom/prenom,
                  et les salaires sont arrondis au millier près.
      - Autre   : vue très restreinte (Hash_ID + sexe + catégorie_pro + salaire arrondi)
    """
    role = role.lower()

    if role == "admin":
        # Admin : accès complet au dataset
        return df_source.copy()
    elif role == "manager":
        # Manager : accès partiel au dataset
        df_mgr = df_source.copy()
        # Arrondi des salaires au millier près (ex: 43 062 -> 43 000)
        if "salaire_brut" in df_mgr.columns:
            df_mgr["salaire_brut"] = df_mgr["salaire_brut"].round(-3)
        # On retire les colonnes sensibles
        colonnes_a_exclure = [
            "secu_sociale",
            "secu_sociale_masked",
            "nom",
            "prenom",
        ]
        cols_mgr = [c for c in df_mgr.columns if c not in colonnes_a_exclure]
        return df_mgr[cols_mgr]
    else:
        # Rôle inconnu ou grand public : vue ultra restreinte
        colonnes_minimales = [
            "hash_id",
            "sexe",
            "categorie_pro",
            "salaire_brut",
        ]
        colonnes_minimales = [c for c in colonnes_minimales if c in df_source.columns]
        df_other = df_source.copy()
        if "salaire_brut" in df_other.columns:
            df_other["salaire_brut"] = df_other["salaire_brut"].round(-3)
        return df_other[colonnes_minimales]

# Exemples d'extraction des jeux de données par rôle
df_admin = get_dataset_by_role(df, "Admin")
df_manager = get_dataset_by_role(df, "Manager")

print("\nAperçu dataset Admin :")
print(df_admin.head(10))

print("\nAperçu dataset Manager :")
print(df_manager.head(10))

# =========
# Partie 3
# =========

# ==============================
# 3. Métadonnées & Cycle de vie
# ==============================

# ===============================
# 3.1 Définition du dataset Gold
# ===============================
colonnes_gold = [
    "hash_id",              # identifiant anonymisé
    "sexe",
    "date_naissance",
    "categorie_pro",        # CSP
    "salaire_brut",         # en EUR, integer
    "date_embauche",
    "email",
    "secu_sociale_masked",  # version masquée
]

df_gold = df[colonnes_gold].copy()

# =========
# Partie 4
# =========

import matplotlib.pyplot as plt
from datetime import date

# ==============================
# 4. Visualisation Finale
# Dashboard Matplotlib
# ==============================

# ===========================================================
# 4.1 Enrichissement : calcul de l'âge et des tranches d'âge
# ===========================================================
def ajouter_age(df_source: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute deux colonnes :
      - age : âge en années (approximateur sur l'année)
      - tranche_age : classe d'âge (18-30, 30-40, ...)
    """
    df_age = df_source.copy()
    df_age["date_naissance_dt"] = pd.to_datetime(df_age["date_naissance"])
    df_age["age"] = df_age["date_naissance_dt"].apply(
        lambda d: date.today().year - d.year
    )
    df_age["tranche_age"] = pd.cut(
        df_age["age"],
        bins=[18, 30, 40, 50, 60, 70],
        labels=["18-30", "30-40", "40-50", "50-60", "60-70"]
    )
    return df_age

# On enrichit df (et donc df_gold si besoin) avec l'âge
df = ajouter_age(df)

# =========================================
# 4.2 Construction du dashboard Matplotlib
# =========================================
def construire_dashboard(df_source: pd.DataFrame, emails_invalides: pd.DataFrame):
    """
    Construit un dashboard Matplotlib avec :
      - Distribution globale des salaires
      - Distribution par sexe
      - Boxplot par catégorie socio-professionnelle
      - Salaire moyen par tranche d'âge
      + KPIs affichés sur la figure
    """
    df_visu = df_source.copy()

    # KPIs
    salaire_moyen = df_visu["salaire_brut"].mean()
    nb_emails_invalides = len(emails_invalides)

    # Figure globale avec 2 lignes x 2 colonnes
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Dashboard Parité Salariale - People Analytics", fontsize=16, fontweight="bold")

    # --------------------------------------------------------
    # Graphique 1 : Histogramme global des salaires
    # --------------------------------------------------------
    ax = axes[0, 0]
    ax.hist(df_visu["salaire_brut"].dropna(), bins=30)
    ax.set_title("Distribution globale des salaires")
    ax.set_xlabel("Salaire brut annuel (€)")
    ax.set_ylabel("Nombre d'employés")

    # --------------------------------------------------------
    # Graphique 2 : Histogramme des salaires par sexe
    # --------------------------------------------------------
    ax = axes[0, 1]
    sexes = df_visu["sexe"].dropna().unique()
    for sexe in sexes:
        subset = df_visu[df_visu["sexe"] == sexe]["salaire_brut"].dropna()
        ax.hist(subset, bins=30, alpha=0.5, label=str(sexe))
    ax.set_title("Distribution des salaires par sexe")
    ax.set_xlabel("Salaire brut annuel (€)")
    ax.set_ylabel("Nombre d'employés")
    ax.legend(title="Sexe")

    # --------------------------------------------------------
    # Graphique 3 : Boxplot des salaires par catégorie_pro (CSP)
    # --------------------------------------------------------
    ax = axes[1, 0]
    categories = df_visu["categorie_pro"].dropna().unique()
    data_box = [df_visu[df_visu["categorie_pro"] == cat]["salaire_brut"].dropna() for cat in categories]
    ax.boxplot(data_box, tick_labels=categories, showfliers=False)
    ax.set_title("Salaires par catégorie socio-professionnelle")
    ax.set_xlabel("Catégorie professionnelle")
    ax.set_ylabel("Salaire brut annuel (€)")
    ax.tick_params(axis='x', rotation=20)

    # --------------------------------------------------------
    # Graphique 4 : Salaire moyen par tranche d'âge
    # --------------------------------------------------------
    ax = axes[1, 1]
    moyennes_par_tranche = (
        df_visu.groupby("tranche_age", observed=False)["salaire_brut"]
        .mean()
        .reindex(["18-30", "30-40", "40-50", "50-60", "60-70"])
    )
    ax.bar(moyennes_par_tranche.index.astype(str), moyennes_par_tranche.values)
    ax.set_title("Salaire moyen par tranche d'âge")
    ax.set_xlabel("Tranche d'âge")
    ax.set_ylabel("Salaire brut moyen (€)")

    # --------------------------------------------------------
    # Affichage des KPI sur la figure
    # --------------------------------------------------------
    fig.text(
        0.01, 0.02,
        f"Salaire moyen global : {salaire_moyen:,.2f} €\n"
        f"Nombre d'emails invalides corrigés/rejetés : {nb_emails_invalides}",
        fontsize=10,
        va="bottom",
        ha="left"
    )

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

# =======================
# 4.3 Appel du dashboard
# =======================
construire_dashboard(df, emails_invalides)