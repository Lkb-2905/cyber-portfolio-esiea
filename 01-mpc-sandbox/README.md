# Dossier de Consultation des Entreprises (DCE) - Technique : 01-MPC-Sandbox

## 1. Contexte et Objectifs
Le projet **MPC Sandbox** (Secure Multi-Party Computation) est une démonstration technique de l'implémentation du partage de secret de Shamir (Shamir's Secret Sharing).

**Objectif Principal :** Fournir une API sécurisée et performante permettant de diviser un secret en plusieurs parts (shares) et de le reconstruire uniquement si un seuil (threshold) de parts est atteint.

**Cas d'Usage :**
- Gestion sécurisée de clés cryptographiques.
- Vote électronique décentralisé.
- Calcul distribué sur données confidentielles.

## 2. Spécifications Techniques

### 2.1 Architecture Logicielle
L'application repose sur une architecture micro-service moderne, conteneurisée et observable.

- **Backend :** Python 3.11 avec FastAPI (Asynchrone, Haute Performance).
- **Frontend :** HTML/JS statique servi par le backend (pour la démonstration).
- **Sécurité :**
    - Utilisation de grands nombres premiers pour le corps fini (Finite Field Arithmetic).
    - Aucun stockage persistant du secret reconstruit.

### 2.2 Stack Technologique
| Composant | Technologie | Version | Description |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.11 | Typage fort, performance et écosystème sécurité. |
| **Framework API** | FastAPI | 0.115.6 | Validation automatique des données (Pydantic) et documentation OpenAPI. |
| **Serveur App** | Uvicorn | 0.30.6 | Serveur ASGI haute performance. |
| **Conteneurisation** | Docker | Multi-stage | Build optimisé (<200MB), rootless (sécurité). |
| **Linting/Qualité** | Ruff | 0.x | Respect des standards PEP8 et analyse statique. |

## 3. Installation et Déploiement

### 3.1 Prérequis
- Moteur de conteneur : Docker (v20.10+)
- Optionnel : Git, Python 3.11+

### 3.2 Déploiement via Docker (Recommandé)
L'image Docker est construite en multi-stage pour garantir légèreté et sécurité.

1.  **Construction de l'image :**
    ```bash
    # Depuis la racine du projet (01-mpc-sandbox/)
    docker build -t mpc-sandbox-backend -f backend/Dockerfile .
    ```

2.  **Lancement du conteneur :**
    ```bash
    docker run -d -p 8000:8000 --name mpc-sandbox mpc-sandbox-backend
    ```

3.  **Vérification :**
    L'application est accessible sur `http://localhost:8000`.

## 4. Mesures et Observabilité
Pour garantir la maintenabilité en production, le service expose des métriques et des logs structurés.

### 4.1 Métriques (Prometheus)
Un endpoint `/metrics` est disponible pour le scraping par Prometheus.
- **URL :** `http://localhost:8000/metrics`
- **Indicateurs Clés :**
    - `http_requests_total` : Volume de trafic.
    - `http_request_duration_seconds` : Latence des opérations cryptographiques (Split/Combine).
    - `process_cpu_seconds_total` : Consommation CPU (critique pour les calculs mathématiques).

### 4.2 Logging Structuré (JSON)
Les logs sont émis au format JSON via `structlog` pour une intégration facile dans ELK/Splunk.
- **Format :** `{"event": "request_received", "level": "info", "timestamp": "...", "path": "/api/split"}`
- **Avantage :** Traçabilité complète des actions sans exposer les secrets.

## 5. API et Fonctionnalités
Documentation interactive (Swagger UI) disponible sur `/docs`.

### Endpoints Principaux
1.  **POST `/api/split`** : Divise un secret en `n` parts avec un seuil `k`.
2.  **POST `/api/combine`** : Reconstruit le secret à partir des parts fournies.
3.  **POST `/api/sign`** : Signe un message avec le secret reconstruit (sans le révéler).

---
**Version du Document :** 2.0.0
**Dernière Mise à jour :** Février 2026
