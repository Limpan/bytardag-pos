#!/bin/sh

set -e

# Make sure auto complete for seller ids are current.
flask sid refresh

exec "$@"
