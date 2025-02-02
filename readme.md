# Gestionnaire de Tâches

## Description

Le Gestionnaire de Tâches est une application Django conçue pour aider à gérer les tâches, les récompenses et les
objectifs. Il permet de suivre les progrès quotidiens, hebdomadaires et mensuels, et de motiver execution des tâches par
l'obtention de récompenses.

L'application est visitable à cette adresse : <https://melody37.pythonanywhere.com/> avec un système d'authentification.
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
