# DevSecOps Pipeline Demo

Mini application (FastAPI + UI statique) conçue pour démontrer un pipeline
sécurité complet : SAST, scan dépendances, SBOM, signature et DAST.

## Fonctionnalités
- API FastAPI: `GET /api/health`, `GET/POST/DELETE /api/items`
- UI légère pour gérer des items
- Pipeline GitHub Actions avec Semgrep, Trivy, Syft, Cosign et ZAP

## Démarrage rapide

### Prérequis
- Python 3.10+

### Installation
```bash
cd backend
python -m pip install -r requirements.txt
```

### Lancer l’API + UI
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Ouvrir: `http://127.0.0.1:8000`

## Tests
```bash
cd backend
python -m pytest
```

## Pipeline CI (résumé)
- **SAST**: Semgrep (`p/ci`)
- **Dependency scan**: Trivy (filesystem)
- **SBOM**: Syft (SPDX JSON)
- **Signature**: Cosign (keyless, signature d’un SBOM)
- **DAST**: OWASP ZAP (baseline)

## Notes
- Le job ZAP démarre l’API localement avant le scan.
- Le job Cosign utilise OIDC GitHub pour signer le SBOM.
