# MPC Sandbox (Shamir Secret Sharing)

Projet démonstrateur de MPC basé sur le partage de secret de Shamir, avec une
interface web simple et une API FastAPI.

## Fonctionnalités
- Split d’un secret en `n` parts avec un seuil `t`.
- Combine pour reconstruire le secret.
- Endpoint de signature HMAC **démonstratif** (reconstruction + signature).
- UI minimale pour tester rapidement.

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

## API (extraits)
- `POST /api/split`
- `POST /api/combine`
- `POST /api/sign`

## Notes de sécurité
La signature `/api/sign` reconstruit le secret côté serveur pour signer un
message (HMAC). C’est une **démo pédagogique** et non un vrai protocole
de signature distribuée (TSS).
