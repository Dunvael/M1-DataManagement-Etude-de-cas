# Mise en situation

Un bug est découvert 6 mois plus tard : les salaires des personnes embauchés après 2022 sont faux (non prise en compte des augmentations entre 2022 et 2025).

## Question

Expliquez comment vous relancez le calcul uniquement sur les mois concernés sans tout recalculer depuis 2018. Quel mécanisme de stockage (format de fichier) faciliterait cette opération ?

## Réponse pour la correction du bug sur les salaires post-2022

Pour corriger le bug affectant les salaires des employés embauchés après 2022, sans recalculer tout l’historique depuis 2018, il est essentiel de mettre en place une architecture en trois couches : Raw, Silver et Gold.  

* La couche Raw contient les données brutes d’origine, immuables
* La couche Silver regroupe les données nettoyées et typées (issues des étapes 1 et 2)
* Enfin, la couche Gold contient les tables agrégées ou transformées destinées au reporting, comme les métriques de parité salariale

Le bug se situant dans la logique de calcul de la couche Gold, il n’est pas nécessaire de rejouer tout le pipeline depuis le Raw.

La stratégie consiste donc à effectuer un backfill partiel.

1) On commence par identifier uniquement les employés concernés : ceux dont la date_embauche est supérieure ou égale au 1er janvier 2023, ainsi que les périodes de reporting impactées (ici, les années 2023 à 2025).
2) Le pipeline de calcul des salaires est ensuite rejoué uniquement sur ce sous-ensemble, en rechargeant leurs données depuis la Silver puis en appliquant la nouvelle logique correcte. 
3) Une fois les résultats recalculés, on met à jour la table Gold de manière ciblée : si cette table est partitionnée par année (et éventuellement par mois), il suffit d’écraser ou de remplacer uniquement les partitions year >= 2023.
4) Une alternative consiste à effectuer un upsert (merge) pour ne remplacer que les lignes corrigées.

Pour faciliter ce type d’opération, la table Gold doit être stockée dans un format optimisé pour le partitionnement et les opérations incrémentales.  
Le Parquet est déjà un bon choix grâce à sa structure column-store et son support natif du partitionnement.  
Encore mieux, l’utilisation d’un format transactionnel comme Delta Lake, Apache Iceberg ou Apache Hudi permet de gérer le versioning (time-travel), les merges propres, et les réécritures partielles de partitions. Ainsi, la correction est rapide, fiabilisante et évite de recalculer inutilement cinq années d’historique.