# Confidential Computing Sandbox (TEE simulée)

Ce projet simule un service “confidential computing” en séparant :
- **chiffrement des données** (data key),
- **protection du data key** (master key conservée dans une TEE simulée).

⚠️ La TEE est **simulée** pour un POC local (pas un vrai SGX/Nitro).

## Fonctionnalités
- `POST /api/records` : chiffre et scelle un enregistrement.
- `GET /api/records/{id}` : déchiffre côté “TEE”.
- `GET /api/records` : liste des IDs.

## Démarrage rapide

### Prérequis
- Python 3.10+

### Installation
```bash
cd backend
python -m pip install -r requirements.txt
```

### Lancer l’API
```bash
cd backend
python -m uvicorn app.main:app --reload
```

## Exemple de requêtes
```bash
curl -X POST http://127.0.0.1:8000/api/records \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"secret\", \"encoding\":\"utf-8\"}"

curl http://127.0.0.1:8000/api/records/{record_id}?encoding=utf-8
```

## Notes de sécurité
Ce POC utilise un chiffrement XOR pour simplifier la démo. Dans un vrai
environnement, on utiliserait AES-GCM et un TEE réel (Nitro/SGX).
