#!/bin/bash
tmux kill-server
python3 -m venv venv

cd /root/AriannaRPortfolio

git fetch && git reset origin/main --hard


source venv/bin/activate




tmux new-session -d -s flask_server

source python3-virtualvenv/bin/activate 
 docker compose -f docker-compose.prod.yml down
  docker compose -f docker-compose.prod.yml up -d --build
python3 run.py
