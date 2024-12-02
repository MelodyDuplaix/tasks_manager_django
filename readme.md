# Gestionnaire de Tâches

## Description

Le Gestionnaire de Tâches est une application Django conçue pour aider à gérer les tâches, les récompenses et les objectifs. Il permet de suivre les progrès quotidiens, hebdomadaires et mensuels, et de motiver l'execution des tâches par l'obtention de récompenses.

## Fonctionnalités

- **Voir et gérer les tâches et récompenses** : Afficher les tâches et les récompenses disponibles, cliquer pour exécuter une tâche et suivre l'objectif quotidien.
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
   Ouvrez votre navigateur et allez sur [http://localhost:8000](http://localhost:8000) pour utiliser le Gestionnaire de Tâches.

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
- **Sous-Manager** : Nom, objectif quotidien, mensuel, hebdomadaire,  clé étrangère dans d'autres modèles.

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour toute suggestion ou amélioration.

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
- [x] Ajouter un endroit pour ajouter des types de tâches par sous manager (donc dans la page d'option d'un sous manager)
- [x] A la création d'une tâche, n'avoir que les types du sous manager actuel
- [ ] Ajouter les fonctionnalités des tâches ponctuelles
- [ ] Ajouter des filtres sur l'historique (filtres par date et sous manager)
- [ ] Mettre en place des vérifications des erreurs
- [ ] Mettre en place des tests
- [ ] Ajouter un bouton annuler dernière action
- [ ] Ajouter des barres de progressions fusionnées de tous les sous-managers
- [ ] Voir la possibilité d'un mode sombre ?
- [ ] Voir pour pourvoir désactiver temporairement un sous manager

