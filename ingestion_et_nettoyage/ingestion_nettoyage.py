import pandas as pd
# import numpy as np
# from datetime import datetime
# import re

# 1. Ingestion du fichier
df = pd.read_csv("employees_raw.csv")

# ==========================
# 2. Nettoyage des EMAILS
# ==========================

# Regex email standard
email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# Flag emails valides
df["email_valide"] = df["email"].astype(str).str.match(email_regex)

# Séparation (on garde uniquement les valides)
emails_invalides = df[~df["email_valide"]]
df = df[df["email_valide"]].drop(columns=["email_valide"])





















# # Exemple : normalisation des noms de colonnes si besoin
# df.columns = [c.strip().lower() for c in df.columns]

# # On suppose les colonnes suivantes (à adapter selon ton fichier réel) :
# # ['nom', 'prenom', 'email', 'salaire_brut', 'date_embauche', 'secu_sociale', 'sexe', 'csp', 'age']

# # 1.a Nettoyage des emails invalides
# # règle simple : contient '@' et au moins un '.' après
# def is_valid_email(email: str) -> bool:
#     if not isinstance(email, str):
#         return False
#     if "@" not in email:
#         return False
#     local, _, domain = email.partition("@")
#     if "." not in domain:
#         return False
#     return True

# df["email_valide"] = df["email"].apply(is_valid_email)
# nb_emails_invalides = (~df["email_valide"]).sum()
# # On peut soit supprimer, soit mettre NaN pour les invalides
# df.loc[~df["email_valide"], "email"] = np.nan

# # 1.b Conversion salaire_brut texte -> int
# # ex : "50 000 €", "EUR 45000", "50000"
# def parse_salaire(s):
#     if pd.isna(s):
#         return np.nan
#     if not isinstance(s, str):
#         s = str(s)
#     s = s.replace("€", "").replace("EUR", "").replace("eur", "")
#     s = s.replace(" ", "").replace("\u00a0", "")
#     try:
#         return int(float(s))
#     except ValueError:
#         return np.nan

# df["salaire_brut_int"] = df["salaire_brut"].apply(parse_salaire)

# # 1.c Harmonisation date_embauche au format ISO, rejet des dates incohérentes
# def parse_date_safe(d):
#     try:
#         return pd.to_datetime(d, errors="raise", dayfirst=True)
#     except Exception:
#         return pd.NaT

# df["date_embauche_parsed"] = df["date_embauche"].apply(parse_date_safe)

# # Ex : on considère incohérentes les dates avant 1980 ou après aujourd'hui
# today = pd.Timestamp.today()
# mask_dates_valides = (df["date_embauche_parsed"].notna() &
#                       (df["date_embauche_parsed"] >= "1980-01-01") &
#                       (df["date_embauche_parsed"] <= today))

# df = df[mask_dates_valides].copy()
# df["date_embauche_iso"] = df["date_embauche_parsed"].dt.strftime("%Y-%m-%d")

# # KPI email corrigés/rejetés
# kpi_nb_emails_corriges_ou_rejetes = nb_emails_invalides
