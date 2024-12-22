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

## Structure du Projet

- **admin/** : Interface d'administration pour gérer le contenu.
- **/** : Page principale du menu et gestion des sous-managers.
- **update-sous-manager/** : Modifier un sous-manager existant.
- **add-sous-manager/** : Ajouter un nouveau sous-manager.
- **delete-sous-manager/** : Supprimer un sous-manager.
- **sous-manager/** : Page pour gérer les tâches et récompenses et suivre les objectifs quotidiens.
- **sous-manager/options/** : Options pour configurer les objectifs, les tâches et les récompenses.
- **historique/** : Page pour voir l'historique des tâches.
- **hebdomadaire/** : Suivi des objectifs hebdomadaires.
- **mensuel/** : Suivi des objectifs mensuels.

## Modèles

- **Tâche** : Nom, nombre de pièces, ponctuelle, type, sous-manager.
- **Récompense** : Nom, nombre de pièces, sous-manager.
- **Action** : Nom, date, type, nombre de pièces, sous-manager.
- **Sous-Manager** : Nom, objectif quotidien, mensuel, hebdomadaire, clé étrangère dans d'autres modèles.

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre un pull request ou ouvrir une issue pour toute suggestion ou
amélioration.

## Todo

- [x] Configurer le site d'administration
- [x] Ajouter la page principale pour voir les sous managers
- [x] Ajouter la page de modification d'un sous manager
- [x] Ajouter la page d'ajout d'un sous manager
- [x] Ajouter la suppression d'un sous manager
- [x] Créer la page principale du sous manager (actionner des taches et récompenses, suivre l'objectif quotidien)
- [x] Implémenter la page d'historique des tâches.
- [x] Compléter les options pour configurer les objectifs, gérer les tâches et les récompenses.
- [x] Ajouter le suivi des objectifs hebdomadaires.
- [x] Ajouter le suivi des objectifs mensuels.
- [x] Ajouter des configurations de bases (objectifs de base) à l'ajout d'un sous-manager
- [x] Ajouter un endroit pour ajouter des types de tâches par sous manager (donc dans la page d'option d'un sous
  manager)
- [x] À la création d'une tâche, n'avoir que les types du sous manager actuel
- [x] Ajouter les fonctionnalités des tâches ponctuelles
- [x] Ajouter des filtres sur l'historique (filtres par date et sous manager)
- [x] Implémenter la modification des actions correspondantes lors de la modification d'une tâche
- [x] Ajouter des barres de progressions fusionnées de tous les sous-managers
- [x] Mettre en place des vérifications des erreurs de base
- [x] Voir pour pouvoir désactiver temporairement un sous manager
- [x] Mettre en place des tests unitaires
- [x] Ajouter un bouton annuler action
- [x] Ajout du nombre total de pièces des lignes à la fin du tableau d'historique
- [x] Ajout d'un système d'authentification
- [x] Déployer l'application
- [x] Centrer les types de tâches
- [x] Ajouter l'utilisation de la méthode login après l'inscription et avant la redirection pour que l'utilisateur soit
  directement connecté après inscription, et / ou ajouter un message de confirmation
- [x] Ajout d'une app bar en haut de la page
- [x] Pouvoir ajouter un type de tache en ajoutant une tache
- [ ] Améliorer l'authentification (oubli de mot de passe, etc)
- [ ] Refaire les tests unitaires
- [ ] avoir la possibilité de timers pour mesurer le temps sur les taches (bouton finir la journée, et enregistrement
  des heures quand on clique sur un bouton)
- [ ] ajouter des stats sur les temps que l'on passe sur les taches
- [ ] Ajout d'un système de badge en fonction des objectifs réalisés ou non
- [ ] Voir la possibilité d'un mode sombre ?
- [ ] Mettre en place des tests d'intégrations et fonctionnels

- [ ] (Archives idées) Avoir des pièces par sous types avec une possibilité d'avoir un nombre de pièces différente pour
  valider la journée (par exemple, il faut 10 pièces, dont 2 en sous type 1, 3 en sous type 2 et 2 en sous type 3) (
  demander à Antoine plus de précisions sur son idée)