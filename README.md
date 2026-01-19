# Portfolio Cybersécurité — ESIEA

## Badges CI (projet 03)
![security-pipeline](https://github.com/Lkb-2905/cyber-portfolio-esiea/actions/workflows/security.yml/badge.svg)
![dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen)

Ce dossier regroupe 5 projets démonstrateurs conçus pour un profil étudiant
en cybersécurité (ESIEA), alignés avec des attentes de type DevSecOps,
confidential computing et privacy.

## Projets

### 01 — MPC Sandbox (Shamir)
Partage de secret + reconstruction + signature HMAC démonstrative.  
➡️ Dossier: `01-mpc-sandbox`

### 02 — Confidential Computing (TEE simulée)
Chiffrement “in‑use” avec master key isolée (simulée).  
➡️ Dossier: `02-confidential-computing`

### 03 — DevSecOps Pipeline Demo
App FastAPI + UI + pipeline sécurité complet (SAST, SBOM, signature, DAST).  
➡️ Dossier: `03-devsecops-pipeline`

### 04 — Exfiltration Detection
Génération de flux + détection d’anomalies (Isolation Forest) + dashboard.  
➡️ Dossier: `04-exfiltration-detection`

### 05 — Privacy Proxy (PII Shield)
Détection & masquage de PII via regex, API simple.  
➡️ Dossier: `05-privacy-proxy`

## Compétences démontrées
- Cryptographie appliquée : Shamir, clés, HMAC
- Confidential computing : séparation data key / master key
- DevSecOps : SAST, DAST, SBOM, signature, dépendances
- Détection d’anomalies : données réseau, ML léger
- Privacy engineering : détection PII, redaction
- API & livraison : FastAPI, tests, documentation

## Vue d’ensemble
| Projet | Stack principale | Objectif | Temps estimé |
| --- | --- | --- | --- |
| 01 — MPC Sandbox | Python, FastAPI | Partage de secret + reconstruction | 1-2 semaines |
| 02 — Confidential Computing | Python, FastAPI | Scellage + déchiffrement en TEE simulée | 1-2 semaines |
| 03 — DevSecOps Pipeline | FastAPI, GitHub Actions | SAST/DAST/SBOM/Signature | 1-2 semaines |
| 04 — Exfiltration Detection | Python, sklearn | Détection anomalies flux réseau | 1-2 semaines |
| 05 — Privacy Proxy | Python, FastAPI | Détection & masquage PII | 1 semaine |

## Comment utiliser
Chaque dossier contient un `README.md` avec :
- les prérequis,
- la procédure d’installation,
- et les commandes pour lancer/tests.
