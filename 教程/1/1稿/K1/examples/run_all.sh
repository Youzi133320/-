#!/bin/bash
# 运行全部示例并保存输出到 out/
cd "$(dirname "$0")"; mkdir -p out
PY315=$(uv python find 3.15); PY315T=$(uv python find 3.15t); VENV=/workspace/.k1venv/bin/python
for f in [0-9][0-9]_*.py; do
  n=${f%%_*}
  if [ "$n" -le 27 ]; then py=$PY315; else py=$VENV; fi
  timeout 120 $py "$f" > "out/${f%.py}.txt" 2>&1; echo "$f exit=$?"
done
timeout 120 $PY315T 27_threading.py > out/27_threading_ft.txt 2>&1; echo "27 ft exit=$?"
timeout 60 $VENV -m mypy 24b_type_errors.py > out/24b_mypy.txt 2>&1; echo "mypy exit=$? (期望非0)"
