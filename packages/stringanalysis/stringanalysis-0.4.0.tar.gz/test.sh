#!/usr/bin/env bash
set -e

time maturin develop
time MYPYPATH=. python -m mypy stringanalysis
time python -m pytest -vv