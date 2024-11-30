A faire :
- [x] créer les modèles
- [x] activer le site d'administration
- [ ] faire les pages
- [ ] faire les formulaires et affichages divers
- [ ] ajouter les chanegements des objets via affichages et formulaires


Liste des pages / fonctionnalités:
- voir les tâches et récompense / cliquer pour en faire une / suivre l'objectif quotidien
- suivi hebodmaire
- suivi mensuel
- options (objectifs, gérer tâches, gérer récompenses)
- Gestion des sous-manager
- page d'historique des tâches

- [x] / : page menu principale
- [ ] sous-manager/ : page d'accès aux pages du sous-manager
- [ ] sous-manager/tasks/ : page pour voir et cliquer sur les tâches et récompenses, suivre l'objectif quotidien
- [ ] sous-manager/options/ : (objectifs, gérer tâches, gérer récompenses)
- [x] options/ : gestion des sous manager
- [ ] historique/ : page d'historique
- [ ] hebdomadaire/ : objectif mensuel
- [ ] mensuel/ objectif mensuel

Liste des modèles:
- tâche (avec option tâche ponctuelle)
  - nom -> champs de caractère
  - nombre de pièce -> entier
  - ponctuel ? -> booléen
  - type -> champs de caractère (ou choices ?)
  - sous-mmanager -> clé étrangère
- récompense
  - nom -> champs de caractère
  - nombre de pièce -> entier
  - sous-manager -> clé étrangère
- action (qui serviront à calculer le solde daily, total, mensuel, hebdomadaire)
  - nom -> champs de caractère
  - date -> datetime
  - sous-manager -> clé étrangère
  - type -> champs de caractère (ou choices ?)
  - nombre de pièce -> entier
  - sous-manager -> clé étrangère
- objectif (daily, mensuel, hebdomadaire)
  - name -> champs de caractère
  - nombre de pièce -> entier
  - sous-manager -> clé étrangère
- sous-manager (clé étrangère dans les autres modèles)
  - nom -> champs de caractère