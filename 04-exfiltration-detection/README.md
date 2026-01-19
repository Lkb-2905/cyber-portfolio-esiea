# Exfiltration Detection (simulation + ML)

POC de détection d’exfiltration : génération de flux réseau synthétiques,
entraîner un détecteur d’anomalies, puis afficher les résultats dans un
dashboard web.

## Fonctionnalités
- Génération de flux simulés (normal vs anomalie).
- Détection via **Isolation Forest**.
- API FastAPI + UI statique.

## Démarrage rapide
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Ouvrir: `http://127.0.0.1:8000`

## API
- `POST /api/generate` : génère + détecte
- `GET /api/detections` : récupère le dernier run

## Tests
```bash
cd backend
python -m pytest
```

## Notes
Les flux sont simulés pour la démo. Le même pipeline peut être adapté à Zeek
ou des logs réels.
