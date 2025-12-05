| **Colonne** | **Description** | **Type logique** | **Sensibilité** | **Owner principal** |
| :-------------------: | :------------------------------------------------------------------: | :----------: | :------------------: | :-------------: |
| `hash_id`             | Identifiant unique anonymisé de l’employé, dérivé de nom+prénom+secu | string       | PII (pseudonymisé)   | DRH / DPO       |
| `sexe`                | Sexe déclaré de l’employé (M/F/autre)                                | string       | PII                  | DRH             |
| `date_naissance`      | Date de naissance de l’employé                                       | date         | PII sensible         | DRH / DPO       |
| `categorie_pro`       | Catégorie socio-professionnelle (Ouvrier, Cadre, etc.)               | string       | Confidentiel interne | DRH             |
| `salaire_brut`        | Salaire brut annuel en euros, nettoyé et typé en integer             | integer      | Confidentiel         | DRH / Direction |
| `date_embauche`       | Date d’embauche, format ISO `YYYY-MM-DD`                             | date         | Confidentiel         | DRH             |
| `email`               | Adresse email professionnelle de l’employé                           | string       | PII                  | DSI / DRH       |
| `secu_sociale_masked` | Numéro de sécurité sociale masqué (tous * sauf 2 derniers chiffres)  | string       | PII très sensible    | DPO             |

***Informations tableau :***

* Sensibilité PII = donnée personnelle identifiante (RGPD)
* Confidentiel interne = nécessaire au pilotage RH mais non nominatif
* Owner = responsable métier de la donnée (en général : DRH pour les RH, DPO pour la conformité, DSI pour les aspects techniques)