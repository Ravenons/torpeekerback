#!/bin/sh
echo "Executing Docker entrypoint wrapper script"

# Run auxiliar deploy script and execute what's specified in Dockerfile's CMD
$DEPLOY_RESOURCES_DIR/deploy_aux.sh
exec $@
