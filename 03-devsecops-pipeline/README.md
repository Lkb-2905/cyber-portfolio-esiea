# Dossier de Consultation des Entreprises (DCE) - Technique : 03-DevSecOps-Pipeline

## 1. Contexte et Objectifs
Le projet **DevSecOps Pipeline** est un modèle d'application API conçu pour s'intégrer dans une chaîne d'intégration et de déploiement continus (CI/CD) sécurisée.

**Objectif Principal :** Démontrer les meilleures pratiques de sécurité "Shift-Left", où la sécurité est intégrée dès le code et le build, et non ajoutée à la fin.

**Cas d'Usage :**
- Base pour nouveaux micro-services sécurisés.
- Démonstration de pipelines GitHub Actions / GitLab CI.
- Tests de sécurité automatisés (SAST/DAST).

## 2. Spécifications Techniques

### 2.1 Architecture Logicielle
Une architecture API RESTful classique mais durcie.

- **Frontend :** HTML/JS simple pour visualisation.
- **Backend :** FastAPI avec validation stricte des entrées (Input Validation).
- **Sécurité :**
    - Gestion des erreurs uniforme (pas de fuite de stacktrace).
    - Headers de sécurité HTTP via middleware.
    - Analyse statique de code (Linting/SAST) intégrée via `ruff`.

### 2.2 Stack Technologique
| Composant | Technologie | Version | Description |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.11 | Standard industriel pour l'implémentation backend. |
| **Framework** | FastAPI | 0.115.6 | Performance et sécurité par design (Pydantic). |
| **Qualité Code** | Ruff | Configuré | Linter ultra-rapide pour garantir la conformité PEP8. |
| **Conteneur** | Docker | Distroless-like | Image minimale basée sur python-slim. |

## 3. Installation et Déploiement

### 3.1 Prérequis
- Docker (v20.10+)

### 3.2 Déploiement Standardisé
Le déploiement est conçu pour être automatisable via Terraform ou Ansible.

1.  **Construction de l'image :**
    ```bash
    # Depuis la racine du projet (03-devsecops-pipeline/)
    docker build -t devsecops-pipeline-backend -f backend/Dockerfile .
    ```

2.  **Lancement du conteneur :**
    ```bash
    docker run -d -p 8000:8000 --name devsecops-api devsecops-pipeline-backend
    ```

3.  **Vérification :**
    Accessibilité sur `http://localhost:8000`.

## 4. Mesures et Observabilité
Le service est "Cloud-Native Ready".

### 4.1 Métriques (Prometheus)
Endpoint : `/metrics`
Expose les métriques RED (Rate, Errors, Duration) essentielles pour les SRE (Site Reliability Engineering).
- Suivi du taux d'erreur 5xx (Disponibilité).
- Suivi du temps de réponse (Latence).

### 4.2 Logging Structuré
Logs JSON (`structlog`) permettant l'ingestion facile par des outils SIEM (Security Information and Event Management) pour détecter des attaques potentielles (brute force, injection).

## 5. API et Fonctionnalités
Documentation OpenAPI sur `/docs`.

### Endpoints Principaux
1.  **GET `/api/items`** : Liste sécurisée des items.
2.  **POST `/api/items`** : Création d'item avec validation stricte du payload.
3.  **DELETE `/api/items/{id}`** : Suppression contrôlée.

---
**Version du Document :** 2.0.0
**Dernière Mise à jour :** Février 2026
