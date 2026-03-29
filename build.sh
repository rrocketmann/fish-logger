#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements-render.txt

# Initialize database
cd app
python -c "from app import app, db; app.app_context().push(); db.create_all()"
cd ..
