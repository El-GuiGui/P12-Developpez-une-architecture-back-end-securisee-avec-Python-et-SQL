# Projet 12 - Développez une architecture back-end sécurisée avec Python et SQL
# Epic Events - Documentation

## Table des matières

1. [Introduction](#introduction)
2. [Installation](#installation)
   - [Prérequis](#prérequis)
   - [Cloner le Repository](#cloner-le-repository)
   - [Installation des dépendances](#installation-des-dépendances)
   - [Mise en place de la base de données](#mise-en-place-de-la-base-de-données)
   - [Initialisation des tables](#initialisation-des-tables)
3. [Configuration](#configuration)
   - [Configuration Sentry](#configuration-sentry)
   - [Configuration des variables d'environnement](#configuration-des-variables-denvironnement)
4. [Utilisation de l'application](#utilisation-de-lapplication)
   - [Authentification et autorisation](#authentification-et-autorisation)
   - [Gestion des rôles et permissions](#gestion-des-rôles-et-permissions)
   - [Interface utilisateur (Rich)](#interface-utilisateur-rich)
5. [Fonctionnalités principales](#fonctionnalités-principales)
   - [Gestion des collaborateurs](#gestion-des-collaborateurs)
   - [Gestion des clients](#gestion-des-clients)
   - [Gestion des contrats](#gestion-des-contrats)
   - [Gestion des événements](#gestion-des-événements)
6. [Tests](#tests)
7. [Journalisation avec Sentry](#journalisation-avec-sentry)
8. [Base de données](#base-de-données)
   - [Utilisation de PostgreSQL et PgAdmin](#utilisation-de-postgresql-et-pgadmin)
   - [Modèles et ORM SQLAlchemy](#modèles-et-orm-sqlalchemy)

## Introduction

Epic Events est une application de gestion de la relation client (CRM) développée en Python. L'application permet de gérer les clients, contrats, et événements, tout en offrant une interface utilisateur en ligne de commande améliorée avec la bibliothèque Rich.

## Installation

### Prérequis

- Python 3.1x
- PostgreSQL
- PgAdmin (facultatif)
- Git

### Cloner le Repository

Clonez ce repository sur votre machine locale :

\`\`\`bash
git clone https://github.com/El-GuiGui/P12-Developpez-une-architecture-back-end-securisee-avec-Python-et-SQL.git
cd P12-Developpez-une-architecture-back-end-securisee-avec-Python-et-SQL-main
\`\`\`

### Installation des dépendances

Créez un environnement virtuel et installez les dépendances requises :

\`\`\`bash
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r requirements.txt
\`\`\`

### Mise en place de la base de données

Vérifiez la présence de PostgreSQL. Créez une base de données pour l'application :

\`\`\`sql
CREATE DATABASE crm_db;
\`\`\`

### Initialisation des tables

Le script \`models.py\` à la racine du projet contient la création des tables. Pour initialiser la base de données, exécutez :

\`\`\`bash
python models.py
\`\`\`

**ou** 

On peut églement utiliser \`Alembic\` pour gérer les migrations de base de données. 
Pour initialiser la base de données, suivez ces étapes :

Générez une migration initiale :


\`\`\`bash
alembic revision --autogenerate -m "Initial migration"
\`\`\`

Appliquez la migration pour créer les tables dans la base de données :


\`\`\`bash
alembic upgrade head
\`\`\`

## Configuration

### Configuration Sentry

Pour capturer les erreurs et exceptions, Sentry a été intégré. Configurez le DSN Sentry en ajoutant la clé dans un fichier \`.env\` à la racine du projet :

(la clé DSN s'obtient en créant un nouveau projet sur Sentry, vous lié donc ce projet Sentry à l'application)

\`\`\`env
SENTRY_DSN=votre_clé_dsn
\`\`\`

### Configuration des variables d'environnement

Le fichier \`config.py\` doit contenir les informations de connexion à la base de données et le DSN Sentry :
(on rajoutera seulement le raccourci de la clé DSN ici, question de confidentialité ...)
Pour le reste le fichier \`config.py\` déjà fournis contient les données suffisantes :

\`\`\`config.py
from dotenv import load_dotenv
import os

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crm_db

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
\`\`\`

## Utilisation de l'application

### Authentification et autorisation

L'authentification est gérée via JSON Web Tokens (JWT). Les utilisateurs reçoivent un token JWT lors de la connexion, stocké localement dans un fichier \`token.txt\`.

- Le token expire après une durée prédéfinie et doit être rafraîchi en se reconnectant.
- Les rôles des utilisateurs (Admin, Commercial, Support) déterminent leurs permissions dans l'application.

### Gestion des rôles et permissions

- **Admin** : Peut gérer les collaborateurs, clients, contrats et événements.
- **Commercial** : Peut gérer les clients et contrats dont ils sont responsables.
- **Support** : Peut mettre à jour les événements qui leur sont attribués.

### Interface utilisateur (Rich)

L'interface utilisateur est développée avec la bibliothèque \`Rich\`, ajoutant une utilisation bien plus agréable.

## Fonctionnalités principales

(équipe de gestion = les administrateurs)

### Gestion des collaborateurs

- **Créer un collaborateur** : Accessible uniquement par les administrateurs.
- **Mettre à jour un collaborateur** : Accessible uniquement par les administrateurs.
- **Supprimer un collaborateur** : Accessible uniquement par les administrateurs.

### Gestion des clients

- **Créer un client** : Accessible par les commerciaux.
- **Mettre à jour un client** : Les commerciaux peuvent mettre à jour leurs propres clients.
- **Voir les clients** : Accessible par tous les rôles.

### Gestion des contrats

- **Créer et modifier des contrats** : Accessible par les administrateurs et les commerciaux pour leurs propres clients.
- **Voir les contrats** : Accessible par tous les rôles.

### Gestion des événements

- **Créer un événement** : Les commerciaux peuvent créer des événements pour leurs clients.
- **Mettre à jour un événement** : Les administrateurs et le support peuvent modifier les événements qui leur sont attribués.
- **Voir les événements** : Accessible par tous les rôles.


Les administrateurs n'ont pas besoin d'avoir les attributions de leur modification, ils ont les privilèges de modifiés chaque donnée et menu dont ils ont l'accès ! 

## Tests

Les tests unitaires sont présents dans le répertoire \`tests/\`. Pour exécuter les tests, utilisez :

    \`\`\`bash
    pytest --cov=.
    \`\`\`

La couverture des tests est de xx%

## Journalisation avec Sentry

Sentry capture automatiquement les exceptions inattendues et enregistre les actions importantes telles que :

- **Création, suppression et modification des collaborateurs**
- **Les Signature de contrats**


## Base de données

### Utilisation de PostgreSQL et PgAdmin

PostgreSQL est utilisé comme système de gestion de base de données. PgAdmin est utilisé pour gérer et visualiser la base de données de manière graphique.

### Modèles et ORM SQLAlchemy

L'application utilise SQLAlchemy comme ORM pour interagir avec la base de données. Les modèles de données se trouvent dans le dossier \`models/\` et sont utilisés pour créer et manipuler les tables dans la base de données.
