# Gestionnaire de Tâches

## Description

Le Gestionnaire de Tâches est une application Django conçue pour aider à gérer les tâches, les récompenses et les
objectifs. Il permet de suivre les progrès quotidiens, hebdomadaires et mensuels, et de motiver execution des tâches par
l'obtention de récompenses.

L'application est visitable à cette adresse : https://melody37.pythonanywhere.com/ avec un système d'authentification.
Vous pouvez donc créer un compte pour tester l'application.

## Fonctionnalités

- **Voir et gérer les tâches et récompenses** : Afficher les tâches et les récompenses disponibles, cliquer pour
  exécuter une tâche et suivre l'objectif quotidien.
- **Suivi des objectifs** : Suivi des objectifs quotidiens, hebdomadaires et mensuels.
- **Gestion des sous-managers** : Ajouter, modifier et supprimer des sous-managers.
- **Page d'historique des tâches** : Voir l'historique des tâches complétées.
- **Options de gestion** : Configurer les objectifs, gérer les tâches et les récompenses.

## Instructions d'installation

1. **Cloner le dépôt** :

   ```bash
   git clone <URL_du_dépôt>
   cd manager
   ```

2. **Installer les dépendances** :
   Assurez-vous que Python et pip sont installés, puis exécutez :

   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations de la base de données** :

   ```bash
   python manage.py migrate
   ```

4. **Démarrer le serveur** :

   ```bash
   python manage.py runserver
   ```

5. **Accéder à l'application** :
   Ouvrez votre navigateur et allez sur [http://localhost:8000](http://localhost:8000) pour utiliser le Gestionnaire de
   Tâches.

## Modèles

- **Tâche** : Nom, nombre de pièces, ponctuelle, type, sous-manager.
- **Récompense** : Nom, nombre de pièces, sous-manager.
- **Action** : Nom, date, type, nombre de pièces, sous-manager.
- **Sous-Manager** : Nom, objectif quotidien, mensuel, hebdomadaire, clé étrangère dans d'autres modèles.

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre un pull request ou ouvrir une issue pour toute suggestion ou
amélioration.

## Todo

- [X] Configurer le site d'administration
- [X] Ajouter la page principale pour voir les sous managers
- [X] Ajouter la page de modification d'un sous manager
- [X] Ajouter la page d'ajout d'un sous manager
- [X] Ajouter la suppression d'un sous manager
- [X] Créer la page principale du sous manager (actionner des taches et récompenses, suivre l'objectif quotidien)
- [X] Implémenter la page d'historique des tâches.
- [X] Compléter les options pour configurer les objectifs, gérer les tâches et les récompenses.
- [X] Ajouter le suivi des objectifs hebdomadaires.
- [X] Ajouter le suivi des objectifs mensuels.
- [X] Ajouter des configurations de bases (objectifs de base) à l'ajout d'un sous-manager
- [X] Ajouter un endroit pour ajouter des types de tâches par sous manager (donc dans la page d'option d'un sous
  manager)
- [X] À la création d'une tâche, n'avoir que les types du sous manager actuel
- [X] Ajouter les fonctionnalités des tâches ponctuelles
- [X] Ajouter des filtres sur l'historique (filtres par date et sous manager)
- [X] Implémenter la modification des actions correspondantes lors de la modification d'une tâche
- [X] Ajouter des barres de progressions fusionnées de tous les sous-managers
- [X] Mettre en place des vérifications des erreurs de base
- [X] Voir pour pouvoir désactiver temporairement un sous manager
- [X] Mettre en place des tests unitaires
- [X] Ajouter un bouton annuler action
- [X] Ajout du nombre total de pièces des lignes à la fin du tableau d'historique
- [X] Ajout d'un système d'authentification
- [X] Déployer l'application
- [X] Centrer les types de tâches
- [X] Ajouter l'utilisation de la méthode login après l'inscription et avant la redirection pour que l'utilisateur soit
  directement connecté après inscription, et / ou ajouter un message de confirmation
- [X] Ajout d'une app bar en haut de la page
- [X] Pouvoir ajouter un type de tache en ajoutant une tache
- [X] Améliorer l'authentification (oubli de mot de passe, etc)
- [X] Refaire les tests unitaires
- [ ] ajout d'une barre latéral de navigation a gauche du manager pour naviguer entre les sous manager
- [ ] Améliorer le responsive / interface mobile
- [ ] avoir la possibilité de timers pour mesurer le temps sur les taches (bouton finir la journée, et enregistrement des heures quand on clique sur un bouton)
- [ ] ajouter des stats sur les temps que l'on passe sur les taches
- [ ] Ajout d'un système de badge en fonction des objectifs réalisés ou non
- [ ] Voir la possibilité d'un mode sombre ?
- [ ] Mettre en place des tests d'intégrations et fonctionnels
- [ ] (Archives idées) Avoir des pièces par sous types avec une possibilité d'avoir un nombre de pièces différente pour valider la journée (par exemple, il faut 10 pièces, dont 2 en sous type 1, 3 en sous type 2 et 2 en sous type 3) (demander à Antoine plus de précisions sur son idée)
