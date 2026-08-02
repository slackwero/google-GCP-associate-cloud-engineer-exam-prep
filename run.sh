#!/usr/bin/env bash
#
# Start the practice app. On the first run it also sets everything up.
#
#   ./run.sh              install if needed, then start
#   ./run.sh --restart    same, but first free ports 3000/8000
#   ./run.sh --reinstall  rebuild the virtual environment from scratch
#
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$RAIZ/quiz-app"
VENV="$APP/.venv"
REQUISITOS="$APP/requirements.txt"
# Records which requirements.txt the virtual environment was built from, so a
# dependency bump reinstalls by itself instead of failing at import time.
SELLO="$VENV/.requirements-sha"

rojo() { printf '\033[31m%s\033[0m\n' "$*" >&2; }
paso() { printf '\033[34m▸\033[0m %s\n' "$*"; }

reiniciar=false
reinstalar=false
for arg in "$@"; do
  case "$arg" in
    --restart|-r) reiniciar=true ;;
    --reinstall) reinstalar=true ;;
    --help|-h) sed -n '3,8p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) rojo "Unknown option: $arg (try --help)"; exit 2 ;;
  esac
done

# --- Python ------------------------------------------------------------------
# python3.12 first: Reflex pins versions and the newest interpreter on the box
# is not always the one it supports best.
interprete=""
for candidato in python3.12 python3.11 python3.10 python3; do
  if command -v "$candidato" >/dev/null 2>&1 &&
     "$candidato" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    interprete="$candidato"
    break
  fi
done

if [ -z "$interprete" ]; then
  rojo "Python 3.10 or newer is required and was not found."
  rojo "Install it from https://www.python.org/downloads/ and run this script again."
  exit 1
fi

# --- Ports -------------------------------------------------------------------
ocupados="$(lsof -ti:3000,8000 -sTCP:LISTEN 2>/dev/null || true)"
if [ -n "$ocupados" ]; then
  if [ "$reiniciar" = true ]; then
    paso "Freeing ports 3000 and 8000"
    # shellcheck disable=SC2086
    kill -9 $ocupados 2>/dev/null || true
    sleep 1
  else
    rojo "Ports 3000/8000 are already in use — the app may be running already."
    rojo "Open http://localhost:3000, or run './run.sh --restart' to replace it."
    exit 1
  fi
fi

# --- Virtual environment -----------------------------------------------------
if [ "$reinstalar" = true ]; then
  paso "Removing the existing virtual environment"
  rm -rf "$VENV"
fi

huella() {
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$REQUISITOS" | cut -d' ' -f1
  elif command -v sha256sum >/dev/null 2>&1; then sha256sum "$REQUISITOS" | cut -d' ' -f1
  else cksum "$REQUISITOS" | cut -d' ' -f1
  fi
}

# uv is an order of magnitude faster, but it stays optional: plain venv + pip
# works everywhere and needs nothing extra installed.
if command -v uv >/dev/null 2>&1; then
  crear_entorno() { uv venv --python "$interprete" "$VENV" >/dev/null; }
  instalar() { uv pip install --quiet --python "$VENV/bin/python" -r "$REQUISITOS"; }
else
  crear_entorno() { "$interprete" -m venv "$VENV"; }
  instalar() {
    "$VENV/bin/python" -m pip install --quiet --upgrade pip
    "$VENV/bin/python" -m pip install --quiet -r "$REQUISITOS"
  }
fi

# Creating the environment and filling it are separate steps: a dependency bump
# only reinstalls packages instead of rebuilding the whole environment.
if [ ! -x "$VENV/bin/python" ]; then
  paso "Creating the virtual environment"
  crear_entorno
fi

if [ ! -x "$VENV/bin/reflex" ] || [ ! -f "$SELLO" ] || [ "$(cat "$SELLO")" != "$(huella)" ]; then
  paso "Installing dependencies (only needed the first time, takes a minute)"
  instalar
  huella > "$SELLO"
  paso "Dependencies ready"
fi

# --- Run ---------------------------------------------------------------------
paso "Starting the app at http://localhost:3000  (Ctrl+C to stop)"
echo
cd "$APP"
exec "$VENV/bin/reflex" run
