#!/bin/bash

# Script de build para Render
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up database..."
cd app
python -c "from db import engine, Base; from models import *; Base.metadata.create_all(bind=engine)"

echo "Build completed successfully!"