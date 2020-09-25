#!/bin/sh

set -e

# Initialize container
flask sid refresh /app/bytardag/static/js/autocomplete.js

exec "$@"
