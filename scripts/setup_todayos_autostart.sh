#!/usr/bin/env bash
set -euo pipefail

# Cria serviço systemd para iniciar TodayOS em sessão gráfica X11
SERVICE_PATH="$HOME/.config/systemd/user/todayos.service"
mkdir -p "$(dirname "$SERVICE_PATH")"
cat > "$SERVICE_PATH" <<EOF
[Unit]
Description=TodayOS Pseudo-OS Python Window
After=graphical-session.target

[Service]
Type=simple
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/$UID
ExecStart=$PWD/.venv/bin/python $PWD/main.py
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now todayos.service

echo "Serviço todayos.service criado e iniciado (User systemd)." 
