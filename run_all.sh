#!/usr/bin/env bash
# Reproduces every number in the paper's empirical exhibits and all four figures. Runs in a few seconds.
set -e
cd "$(dirname "$0")/scripts"
for f in check_identities make_exhibits fig_theory; do
  echo "== $f"; python3 "$f.py"
done
