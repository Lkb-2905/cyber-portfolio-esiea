# Dossier de Consultation des Entreprises (DCE) - Technique : 02-Confidential-Computing

## 1. Contexte et Objectifs
Le projet **Confidential Computing** simule un environnement d'exécution de confiance (Trusted Execution Environment - TEE) pour le traitement de données sensibles.

**Objectif Principal :** Garantir que les données ne sont jamais exposées en clair, même lors de leur traitement ou de leur stockage, en utilisant une simulation d'enclave sécurisée.

**Cas d'Usage :**
- Traitement de données médicales ou financières.
- Cloud Computing sécurisé.
- Protection de la propriété intellectuelle (modèles IA).

## 2. Spécifications Techniques

### 2.1 Architecture Logicielle
L'architecture repose sur le principe de "Sealing" (Scellement) des données.

- **TEE Simulator :** Un module Python simulant une enclave matérielle (type Intel SGX) qui chiffre/déchiffre les données à la volée.
- **Storage :** Stockage persistant chiffré (Envelope Encryption). Seule l'enclave possède la clé maîtresse (`tee_master_key.bin`).
- **API :** Interface REST pour interagir avec l'enclave simulée.

### 2.2 Stack Technologique
| Composant | Technologie | Version | Description |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.11 | Cryptographie et simulation logicielle. |
| **Framework API** | FastAPI | 0.115.6 | Interface HTTP performante et typée. |
| **Sécurité** | AES-GCM | Standard | Chiffrement authentifié pour le scellement des données. |
| **Conteneurisation** | Docker | Multi-stage | Image optimisée avec gestion des droits utilisateur (non-root). |

## 3. Installation et Déploiement

### 3.1 Prérequis
- Moteur de conteneur : Docker (v20.10+)

### 3.2 Déploiement via Docker (Recommandé)
Le déploiement inclut la persistance des données via le dossier `data/`.

1.  **Construction de l'image :**
    ```bash
    # Depuis la racine du projet (02-confidential-computing/)
    docker build -t confidential-computing-backend -f backend/Dockerfile .
    ```

2.  **Lancement du conteneur :**
    ```bash
    docker run -d -p 8000:8000 --name confidential-computing confidential-computing-backend
    ```

3.  **Vérification :**
    L'application est accessible sur `http://localhost:8000`.

## 4. Mesures et Observabilité
L'observabilité est cruciale pour détecter les accès non autorisés ou les anomalies de performance.

### 4.1 Métriques (Prometheus)
Endpoint : `/metrics`
- **Indicateurs Clés :**
    - `http_requests_total` : Suivi des appels API.
    - `tee_operations_count` (Custom) : Nombre d'opérations de scellement/descellement.
    - `p99_latency` : Latence des opérations cryptographiques.

### 4.2 Logging Structuré (JSON)
Logs formatés en JSON via `structlog` pour audit de sécurité.
- **Audit :** Chaque accès à une donnée "scellée" est logué avec un timestamp précis et l'ID de la requête, sans révéler le contenu déchiffré.

## 5. API et Fonctionnalités
Documentation interactive sur `/docs`.

### Endpoints Principaux
1.  **POST `/api/records`** (Seal) : Envoie une donnée brute à l'enclave. L'enclave la chiffre et retourne un ID de registre.
2.  **GET `/api/records/{id}`** (Unseal) : Demande à l'enclave de déchiffrer et restituer la donnée originale.
3.  **GET `/api/records`** : Liste les identifiants des données stockées (métadonnées uniquement).

---
**Version du Document :** 2.0.0
**Dernière Mise à jour :** Février 2026
