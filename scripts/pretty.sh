#!/bin/bash
set -euo pipefail

echo "Running pre-commit checks..."

DIRS=("src" "apps")

run() {
  echo "→ $*"
  "$@"
}

fail() {
  echo "Error: $1"
  exit 1
}

# 1. Format code
echo "Formatting code with Ruff..."
run uv run ruff format "${DIRS[@]}"

# 2. Sort imports
echo "Sorting imports with isort..."
for d in "${DIRS[@]}"; do
  run uv run isort "$d" || fail "isort failed in $d"
done

# 3. Lint checks (Ruff)
echo "Running Ruff lint checks..."
for d in "${DIRS[@]}"; do
  run uv run ruff check "$d" || fail "Ruff check failed in $d"
done

# 4. Type checks (ty)
echo "Running type checks..."
for d in "${DIRS[@]}"; do
  run uv run ty check "$d" || fail "Type check failed in $d"
done

echo "All checks passed."