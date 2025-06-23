# Guide de Déploiement - Gestion Comptable SFEC

## Prérequis

### Serveur
- Debian/Ubuntu 20.04 ou supérieur
- PostgreSQL 13 ou supérieur
- Python 3.8 ou supérieur
- Git
- Supervisor
- Nginx

### Configuration du Serveur
```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install -y postgresql python3-pip git supervisor nginx

# Installation de Python et des packages
sudo pip3 install odoo

# Configuration de PostgreSQL
sudo -u postgres createuser -s odoo
sudo -u postgres createdb -O odoo odoo_db
```

## Installation du Module

### 1. Cloner le Repository
```bash
git clone https://github.com/SFEC/gestion_comptable_sfec.git
```

### 2. Configuration de l'Add-on
```bash
cd gestion_comptable_sfec
# Installation des dépendances Python
pip3 install -r requirements.txt

# Configuration du fichier de configuration Odoo
odoo -c /etc/odoo/odoo.conf -u gestion_comptable_sfec
```

### 3. Configuration de la Base de Données
- Créer une nouvelle base de données Odoo
- Importer les données initiales
- Configurer les séquences
- Configurer les groupes d'utilisateurs

## Procédures de Mise à Jour

### 1. Sauvegarde
```bash
# Sauvegarde de la base de données
docker exec -t odoo_db pg_dump -U odoo odoo_db > backup.sql

# Sauvegarde des fichiers
rsync -avz /var/odoo/filestore /var/odoo/backups/
```

### 2. Mise à jour des Fichiers
```bash
# Arrêter le serveur
sudo supervisorctl stop odoo

# Mise à jour du code
git pull origin main

# Installation des nouvelles dépendances
pip3 install -r requirements.txt

# Redémarrer le serveur
sudo supervisorctl start odoo
```

### 3. Migration des Données
```bash
# Mettre à jour le module via l'interface web
# Allez dans "Apps"
# Cliquez sur "Update Apps List"
# Recherchez "Gestion Comptable SFEC"
# Cliquez sur "Update"
```

## Procédures de Sauvegarde Automatique

### Configuration de la Sauvegarde
```bash
# Créer un fichier de configuration pour les sauvegardes
sudo nano /etc/odoo/backup.conf

# Ajouter les lignes suivantes
[backup]
backup_path = /var/odoo/backups
keep_days = 30
```

### Configuration de Supervisor
```bash
# Créer un fichier de configuration pour Supervisor
sudo nano /etc/supervisor/conf.d/odoo-backup.conf

# Ajouter les lignes suivantes
[program:odoo-backup]
command=/usr/local/bin/odoo-backup
autostart=true
autorestart=true
stderr_logfile=/var/log/odoo-backup.err.log
stdout_logfile=/var/log/odoo-backup.out.log
```

## Procédures de Restauration

### 1. Arrêter le Serveur
```bash
sudo supervisorctl stop odoo
```

### 2. Restaurer la Base de Données
```bash
# Restaurer la base de données
docker exec -t odoo_db psql -U odoo -d odoo_db < backup.sql

# Restaurer les fichiers
rsync -avz /var/odoo/backups/filestore /var/odoo/filestore/
```

### 3. Redémarrer le Serveur
```bash
sudo supervisorctl start odoo
```

## Procédures de Déploiement Continu

### Configuration de GitLab CI/CD
```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - pip3 install -r requirements.txt
    - python3 -m pytest tests/

test:
  stage: test
  script:
    - python3 -m pytest tests/ --cov=gestion_comptable_sfec

deploy:
  stage: deploy
  script:
    - git pull origin main
    - supervisorctl restart odoo
```

## Procédures de Maintenance

### Nettoyage des Données
```bash
# Nettoyage des logs
sudo find /var/log/odoo/ -type f -mtime +30 -exec rm {} \;

# Nettoyage des sauvegardes
sudo find /var/odoo/backups/ -type f -mtime +30 -exec rm {} \;
```

### Vérification des Performances
```bash
# Vérifier les logs d'erreurs
tail -f /var/log/odoo/odoo-server.log

# Vérifier les performances
docker exec -t odoo_db psql -U odoo -d odoo_db -c "
SELECT query, total_time, calls 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;
"
