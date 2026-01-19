# Privacy Proxy (PII Shield)

Service simple pour détecter et masquer des PII (email, téléphone FR, IBAN)
avant de laisser transiter des données sensibles.

## Fonctionnalités
- Détection PII via regex (email, téléphone FR, IBAN).
- Redaction automatique.
- API FastAPI.

## Démarrage rapide
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Exemple d’utilisation
```bash
curl -X POST http://127.0.0.1:8000/api/inspect \
  -H "Content-Type: application/json" \
  -d "{\"payload\":\"Email: jean.dupont@example.com\"}"
```

## Tests
```bash
cd backend
python -m pytest
```

## Améliorations possibles
- Ajout de patterns (CB, NIR, passeports).
- Mode “block” si PII détectée.
- Intégration en reverse-proxy (middleware).
