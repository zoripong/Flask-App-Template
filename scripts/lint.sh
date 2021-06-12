#!/usr/bin/env bash
set -e

if [[ "$VIRTUAL_ENV" = "" ]]; then
  echo 'You seem not in any virtual environment.  Stopped.' >> /dev/stderr
  exit 1
fi

flake8

exit 0
