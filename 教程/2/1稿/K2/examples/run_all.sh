#!/bin/bash
# 运行全部 K2 示例并保存输出到 out/
# 08–24、26、27（数据结构与算法，纯标准库）用 CPython 3.15；其余（ML 库、数学、25 需 scipy）用 .k2venv（Python 3.13）
cd "$(dirname "$0")"; mkdir -p out
PY315=$(uv python find 3.15); VENV=/workspace/.k2venv/bin/python
for f in [0-9][0-9]_*.py; do
  n=$((10#${f%%_*}))
  if { [ $n -ge 8 ] && [ $n -le 24 ]; } || [ $n -eq 26 ] || [ $n -eq 27 ]; then py=$PY315; else py=$VENV; fi
  timeout 600 $py "$f" > "out/${f%.py}.txt" 2>&1; echo "$f exit=$?"
done
