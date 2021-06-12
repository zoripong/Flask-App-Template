#!/usr/bin/env bash
set -e

if ! hash poetry 2>/dev/null; then
  curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
  source $HOME/.poetry/env
fi

if [[ "$VIRTUAL_ENV" = "" ]]; then
  echo 'You seem not in any virtual environment.  Stopped.' >> /dev/stderr
  exit 1
fi

poetry install
