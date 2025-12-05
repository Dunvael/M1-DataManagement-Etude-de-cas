# Question

La loi impose de conserver les bulletins de paie pendant une longue durée, mais le RGPD impose de minimiser les données personnelles. Si un employé quitte l'entreprise, décrivez votre politique d'archivage : À quel moment passez-vous sa donnée de la base active (Hot storage) à une base d'archive (Cold storage) ? Que supprimez-vous définitivement ?

## Réponse

La gestion des données RH doit concilier deux obligations contradictoires :

* l’obligation légale de conserver les bulletins de paie pendant plusieurs années, même après le départ d’un employé,

* l’obligation RGPD de minimiser les données personnelles, en ne conservant que ce qui est strictement nécessaire une fois que la relation de travail est terminée.

Pour répondre à ces contraintes, nous mettons en place une politique d’archivage progressive, basée sur deux environnements distincts :

* une base active (Hot Storage) utilisée pour les besoins opérationnels au quotidien
* une base d’archive (Cold Storage) utilisée uniquement pour les obligations légales et les audits.

Lorsqu’un employé quitte l’entreprise, sa donnée suit un cycle en plusieurs étapes :

1) Sortie de la base active dès la fin du contrat
À partir du moment où la relation contractuelle est terminée, l’employé n’a plus de raison opérationnelle d’apparaître dans les dashboards RH actifs.
Nous migrons donc ses données vers une base d’archive Cold Storage dans les 30 jours suivant son départ.

2) Conservation en archive uniquement des informations légalement obligatoires
La loi impose la conservation des bulletins de paie et de certains états comptables pendant plusieurs années.

Par conséquent, seuls les éléments suivants sont conservés en Cold Storage :

* bulletins de paie (généralement 5 ans minimum)
* informations contractuelles exigées par le Code du travail
* identifiants strictement nécessaires pour relier les pièces (ex : hash_id ou numéro interne anonymisé)

Toutes ces données sont stockées dans un environnement isolé, chiffré et avec accès restreint (DRH + DPO uniquement).

3) Suppression définitive des données personnelles non nécessaires
Conformément au RGPD (principe de minimisation), nous supprimons de manière irréversible les éléments suivants :

* nom et prénom
* adresse email professionnelle
* numéro de sécurité sociale (même masqué)
* âge, sexe et catégorie professionnelle (non requis légalement pour l'archivage)
* tout identifiant directement ou indirectement ré-identifiant

L’employé n’étant plus actif, ces données ne sont plus légitimes pour aucun traitement.

4) Transformation des identifiants restants en identifiants non ré-identifiants
Lorsque cela est nécessaire pour conserver la cohérence des archives (ex : liens entre bulletins de paie), les identifiants bruts sont remplacés par des identifiants anonymes non réversibles (hash).
Cela garantit que l’organisation peut produire des justificatifs en cas d’audit, tout en empêchant toute ré-identification de l’ancien salarié.

5) Durée de conservation contrôlée puis suppression finale automatique
Au terme de la durée légale (souvent 5 à 10 ans selon les documents), l’ensemble des données archivées sont automatiquement supprimées du Cold Storage, conformément à la politique de rétention validée par le DPO.

Cette stratégie permet :

* de respecter les obligations légales de conservation,
* de minimiser l’exposition des données personnelles,
* et de garantir que seules les informations nécessaires à l’entreprise subsistent après le départ d’un employé.

Elle assure aussi une nette séparation entre les données opérationnelles (Hot) et les données strictement archivées (Cold), renforçant à la fois la conformité RGPD et la sécurité globale du système d’information.