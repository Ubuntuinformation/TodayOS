#!/usr/bin/env bash
set -euo pipefail

# Atualiza pacote e instala runtime
sudo apt update || true
sudo apt install -y python3 python3-venv python3-pip libgl1-mesa-dev libgles2-mesa-dev || true

# Cria venv local
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Bootstrap concluído. Ative com: source .venv/bin/activate"
