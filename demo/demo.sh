#!/usr/bin/env bash
# Records the README demo GIF (needs asciinema and agg):
#   asciinema rec --overwrite --window-size 100x36 -c demo/demo.sh demo/demo.cast
#   agg --idle-time-limit 1.5 --last-frame-duration 8 --font-size 15 demo/demo.cast demo/demo.gif
set -euo pipefail
cd "$(dirname "$0")/.."

type_cmd() {
  printf '\033[1;32m$\033[0m '
  for ((i = 0; i < ${#1}; i++)); do
    printf '%s' "${1:i:1}"
    sleep 0.012
  done
  sleep 0.4
  echo
}

question="What techniques reduce hallucination in large language models?"

type_cmd "python main.py \"$question\" --max-rounds 2"
python main.py "$question" --max-rounds 2
sleep 1
