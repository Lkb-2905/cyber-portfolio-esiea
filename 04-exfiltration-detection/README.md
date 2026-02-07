# Dossier de Consultation des Entreprises (DCE) - Technique : 04-Exfiltration-Detection

## 1. Contexte et Objectifs
Le projet **Exfiltration Detection** implémente un système de détection d'anomalies réseau basé sur le Machine Learning (ML) pour identifier des tentatives d'exfiltration de données.

**Objectif Principal :** Analyser les flux de données sortants (egress traffic) et détecter les comportements déviants (volume, fréquence, destination) pouvant signaler une fuite de données.

**Cas d'Usage :**
- Surveillance des postes de travail (Endpoint Detection & Response).
- Analyse de trafic réseau (Network Traffic Analysis).
- Détection de malwares communiquant avec des C2 (Command & Control).

## 2. Spécifications Techniques

### 2.1 Architecture Logicielle
L'application combine une API REST pour l'ingestion des flux et un moteur d'inférence ML.

- **Ingestion :** API FastAPI recevant des métadonnées de flux (IP source/dest, port, volume).
- **Moteur ML :** Utilisation de `scikit-learn` et de l'algorithme **Isolation Forest** (apprentissage non supervisé) pour détecter les outliers.
- **Stockage :** Persistance locale (JSON) des modèles et des historiques de détection pour l'audit.

### 2.2 Stack Technologique
| Composant | Technologie | Version | Description |
| :--- | :--- | :--- | :--- |
| **Langage** | Python | 3.11 | Idéal pour le ML et le Backend. |
| **API** | FastAPI | 0.115.6 | Interface performante. |
| **Machine Learning** | Scikit-learn | 1.5.2 | Librairie standard pour l'algo Isolation Forest. |
| **Calcul Numérique** | Numpy | 2.1.3 | Optimisation des calculs matriciels. |
| **Observabilité** | Prometheus | 7.0.0 | Monitoring de la performance du modèle. |

## 3. Installation et Déploiement

### 3.1 Prérequis
- Docker (v20.10+) avec support AVX (pour ML)

### 3.2 Déploiement via Docker
L'image inclut les dépendances ML lourdes tout en restant optimisée.

1.  **Construction de l'image :**
    ```bash
    # Depuis la racine du projet (04-exfiltration-detection/)
    docker build -t exfiltration-backend -f backend/Dockerfile .
    ```

2.  **Lancement du conteneur :**
    ```bash
    docker run -d -p 8000:8000 --name exfiltration-detector exfiltration-backend
    ```

3.  **Vérification :**
    Valider que le modèle se charge correctement via `http://localhost:8000/api/health`.

## 4. Mesures et Observabilité
Le monitoring est étendu aux performances du modèle ML.

### 4.1 Métriques (Prometheus)
Endpoint : `/metrics`
- **Indicateurs Système :** CPU/RAM (l'inférence ML est coûteuse).
- **Indicateurs Métier :**
    - Nombre de flux analysés.
    - Ratio d'anomalies détectées (permet de tuner la sensibilité du modèle).
    - Latence d'inférence (`predict_duration_seconds`).

### 4.2 Logging Structuré
Logs JSON enrichis avec les scores d'anomalie (`anomaly_score`) pour permettre l'analyse post-mortem des faux positifs/négatifs.

## 5. API et Fonctionnalités
Documentation sur `/docs`.

### Endpoints Principaux
1.  **POST `/api/generate`** : Génère un dataset synthétique de trafic et entraîne/teste le modèle à la volée. Retourne le rapport de détection.
2.  **GET `/api/detections`** : Récupère l'historique des dernières analyses.

---
**Version du Document :** 2.0.0
**Dernière Mise à jour :** Février 2026
