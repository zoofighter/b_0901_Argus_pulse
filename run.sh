#!/bin/bash
# Argus Pulse 간편 실행 스크립트
cd "$(dirname "$0")"

# 활성 파이썬 환경 탐색
if [ -n "$CONDA_PREFIX" ]; then
    PYTHON="$CONDA_PREFIX/bin/python"
elif [ -f "/opt/anaconda3/bin/python" ]; then
    PYTHON="/opt/anaconda3/bin/python"
else
    PYTHON="python3"
fi

$PYTHON argus.py "$@"
