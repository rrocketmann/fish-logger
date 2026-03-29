# Render Setup

This project is configured for Render using `render.yaml`.

## Option 1: Blueprint (Recommended)
1. Push this repo to GitHub.
2. In Render: New -> Blueprint.
3. Select this repo.
4. Render reads `render.yaml` and creates the service automatically.

## Option 2: Manual Web Service
Use these values:

- Environment: `Python`
- Build Command: `pip install -r requirements_web.txt`
- Start Command: `cd app && gunicorn --bind 0.0.0.0:$PORT app:app`

Environment variables:
- `PYTHON_VERSION=3.10.0`
- `SECRET_KEY=<any long random value>`

## Notes
- `requirements_web.txt` intentionally excludes heavy AI training dependencies.
- Uploaded images are stored under `app/static/uploads`.
- Database uses SQLite by default. On Render free instances, filesystem is ephemeral, so DB/uploads reset on redeploy/restart.
