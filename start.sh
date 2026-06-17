#!/usr/bin/env bash

# 启动后台 worker
python worker.py &

# 启动 web
gunicorn app:app --bind 0.0.0.0:10000
