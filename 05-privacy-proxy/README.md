# Dossier de Consultation des Entreprises (DCE) - Technique : 05-Privacy-Proxy

## 1. Contexte et Objectifs
Le projet **Privacy Proxy** est une solution de prévention de fuite de données (DLP - Data Loss Prevention) agissant comme un middleware ou une passerelle API.

**Objectif Principal :** Analyser les flux de données textuels pour détecter et masquer (redact) automatiquement les Informations Personnelles Identifiables (PII) avant qu'elles ne soient stockées ou transmises à des tiers.

**Cas d'Usage :**
- Anonymisation de logs.
- Protection RGPD avant envoi vers un LLM (ChatGPT, etc.).
- Sécurisation des environnements de pré-production.

## 2. Spécifications Techniques

### 2.1 Architecture Logicielle
L'application fonctionne comme un service stateless d'inspection de payload.

- **Moteur de Détection :** Utilisation d'expressions régulières (Regex) optimisées et de patterns contextuels pour identifier :
    - Emails
    - Numéros de téléphone
    - Cartes bancaires (Luhn check si activé)
    - Numéros de sécurité sociale (SSN)
- **Moteur de Rédaction :** Remplacement des données sensibles par des tokens neutres (ex: `[EMAIL_REDACTED]`).

### 2.2 Stack Technologique
| Composant | Technologie | Version | Description |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.11 | Richesse des librairies de traitement de texte. |
| **Framework** | FastAPI | 0.115.6 | Haute performance pour minimiser la latence ajoutée (overhead). |
| **Performance** | AsyncIO | Natif | Traitement non-bloquant des requêtes d'inspection. |
| **Qualité** | Pytest | 8.3.4 | Tests unitaires couvrant les patterns de regex critiques. |

## 3. Installation et Déploiement

### 3.1 Prérequis
- Docker (v20.10+)

### 3.2 Déploiement via Docker
Conçu pour être déployé en "Sidecar" dans un pod Kubernetes ou comme service autonome.

1.  **Construction de l'image :**
    ```bash
    # Depuis la racine du projet (05-privacy-proxy/)
    docker build -t privacy-proxy-backend -f backend/Dockerfile .
    ```

2.  **Lancement du conteneur :**
    ```bash
    docker run -d -p 8000:8000 --name privacy-proxy privacy-proxy-backend
    ```

3.  **Vérification :**
    Endpoint de santé sur `http://localhost:8000/api/health`.

## 4. Mesures et Observabilité
Le proxy ne doit pas devenir un goulot d'étranglement.

### 4.1 Métriques (Prometheus)
Endpoint : `/metrics`
- **Performance :** Latence ajoutée par l'inspection (`proxy_processing_seconds`).
- **Efficacité :** Nombre de PII détectées (`pii_detected_total`), classées par type (email, phone, etc.).

### 4.2 Logging Structuré
Logs JSON indiquant QUEL type de donnée a été trouvé, SANS jamais logger la donnée sensible elle-même (Privacy by Design).

## 5. API et Fonctionnalités
Documentation sur `/docs`.

### Endpoints Principaux
1.  **POST `/api/inspect`** : Analyse un texte brut, retourne la version censurée et la liste des types de données trouvés.

---
**Version du Document :** 2.0.0
**Dernière Mise à jour :** Février 2026
