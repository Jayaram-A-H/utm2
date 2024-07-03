#!/bin/bash
BLENDER_ROOT=.
chmod +x $BLENDER_ROOT/entrypoints/with-database/entrypoint.sh
STATUS="$(systemctl is-active postgresql)"
if [ "${STATUS}" = "active" ]; then
    echo "stop local instance of postgresql"
    sudo systemctl stop postgresql
fi
docker-compose down
docker --volumes rm $(docker volume ls -q)
cd $BLENDER_ROOT
docker compose up
docker network connect dss_sandbox-default worker
