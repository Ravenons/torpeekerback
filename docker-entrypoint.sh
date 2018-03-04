#!/bin/sh
echo "Executing Docker entrypoint wrapper script"

# This should neither be run in this container nor this way, but...
tor &

# Run auxiliar deploy script and execute what's specified in Dockerfile's CMD
$DEPLOY_RESOURCES_DIR/deploy_aux.sh
exec $@
