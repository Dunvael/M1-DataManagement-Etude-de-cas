# **People Analytics – Étude de cas Data Management (Sujet 1)**

### *RH & People Analytics — Focus Sécurité & RGPD*

Ce projet met en œuvre une chaîne complète de traitement de données RH après fusion d’entreprise.
Il couvre l’ingestion, le nettoyage, l’anonymisation, la production d’un dataset Gold, la gouvernance RGPD, ainsi qu’un dashboard final de parité salariale.

Les travaux sont organisés en **5 parties**, chacune dans un dossier dédié.

---

# **Structure du Projet**

```
M1-DataManagement-Etude-de-cas/
│
├── ingestion_et_nettoyage/          # Partie 1 : Nettoyage & normalisation
│   ├── employees_raw.csv
│   ├── ingestion_nettoyage.py
│   └── nettoyage_ingestion_sorties.PNG
│
├── securite_et_anonymisation/       # Partie 2 : Sécurité & anonymisation
│   ├── employees_raw.csv
│   ├── securite_anonymisation.py
│   └── securite_anonymisation_sorties.PNG
│
├── metadonnees_et_cycle_de_vie/     # Partie 3 : Dataset Gold & Backfill
│   ├── dataset_gold.md
│   ├── dataset_gold.yaml
│   ├── dataset_gold.py
│   └── backfill_maintenance.md
│
├── strategie_gouvernance/           # Partie 5 : Archivage & RGPD
│   └── strategie_gouvernance.md
│
├── visualisation_finale/            # Partie 4 : Dashboard Matplotlib
│   ├── dashboard_parite_salariale.py
│   ├── graphique_et_kpi.png
│   └── employees_raw.csv
│
└── projet_complet/                  # Version finalisée (main)
    ├── main.py
    ├── dataset_gold.md
    ├── dataset_gold.yaml
    ├── graphique_et_kpi.png
    ├── nettoyage_ingestion_sorties.PNG
    ├── securite_anonymisation_sorties.PNG
    └── employees_raw.csv
```

---

# **1. Ingestion & Nettoyage**

Cette étape traite un fichier CSV hétérogène comportant :

* des emails invalides
* des salaires non numériques
* des dates d’embauche dans des formats variés

Le script réalise :

* Nettoyage des emails via regex
* Suppression des adresses impossibles (KPI généré)
* Standardisation du salaire (`EUR`, symboles, espaces → int)
* Harmonisation des dates via plusieurs formats (`%d/%m/%Y`, `%Y-%m-%d`, etc.)
* Filtrage des dates incohérentes (<1980 ou > aujourd’hui)

Sorties :

* Dataset propre
* KPI : nombre d’emails invalides
* Prévisualisation des données nettoyées

---

# **2. Sécurité & Anonymisation**

*Objectif* : garantir la conformité RGPD tout en permettant l’analyse RH.

Le pipeline effectue :

* ### Hash irréversible des identités

`hash_id = SHA256(nom + prenom + secu_sociale)`

* ### Masquage du numéro de sécurité sociale

Format :
`158046912327970 → *************70`

* ### Gestion des accès par rôle

| Rôle        | Colonnes accessibles                                   |
| ----------- | ------------------------------------------------------ |
| **Admin**   | Toutes les colonnes                                    |
| **Manager** | Pas de nom, pas de prénom, pas de NIR, salaire arrondi |
| **Autre**   | Hash_ID + sexe + CSP + salaire arrondi                 |

Sorties :

* Dataset Admin
* Dataset Manager

---

# **3. Dataset Gold & Métadonnées**

Le dataset Gold synthétise uniquement les colonnes nécessaires à l’analyse :

```
hash_id, sexe, date_naissance,
categorie_pro, salaire_brut,
date_embauche, email,
secu_sociale_masked
```

Documentation fournie :

* `dataset_gold.md` — description métier
* `dataset_gold.yaml` — version machine-readable (type, owner, sensibilité)

### Backfill & Maintenance

Documenté dans `backfill_maintenance.md`.

Principes retenus :

* recalcul **uniquement** pour les employés embauchés après **2022**
* recalcul restreint aux années **2023 → 2025**
* architecture recommandée : **Parquet partitionné** ou **Delta Lake**
* pas de recalcul historique complet → pipeline incrémental

---

# **4. Dashboard Final – Parité Salariale**

Généré avec `dashboard_parite_salariale.py` (Matplotlib).

### Graphiques produits :

* Histogramme global des salaires
* Distribution des salaires par **sexe**
* Boxplot par **CSP (catégorie professionnelle)**
* Salaire moyen par **tranche d’âge**

### KPI affichés :

* Salaire moyen global
* Nombre d’emails invalides corrigés/rejetés

Sortie principale :
`visualisation_finale/graphique_et_kpi.png`

---

# **5. Stratégie & Gouvernance (Archivage & RGPD)**

Document détaillé dans `strategie_gouvernance.md`.

Principes adoptés :

* Données actives → *Hot Storage*
* Après départ salarié → migration en *Cold Storage*
* Conservation uniquement des éléments légalement obligatoires (bulletins de paie)
* Suppression définitive : nom, email, NIR, données non nécessaires
* Maintien d’un identifiant anonymisé (hash) pour la traçabilité
* Respect des principes RGPD : minimisation, limitation, sécurité

---

# **Résumé**

Ce projet fournit une approche complète, cohérente et sécurisée de People Analytics :

* Nettoyage robuste du CSV
* Anonymisation forte & gestion des rôles
* Dataset Gold documenté
* Backfill maîtrisé
* Dashboard de parité salariale
* Gouvernance & archivage conformes au RGPD
