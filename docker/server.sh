#!/bin/bash

CONFIGURE_BASIC="
ip route del default
"

CONTAINER_NAME="servidor"
docker exec "$CONTAINER_NAME" bash -c "$CONFIGURE_BASIC"
echo "COMANDOS BASICOS configurados en $CONTAINER_NAME."

ROUTES="ip route add default via 10.3.0.10"

docker exec "$CONTAINER_NAME" bash -c "$ROUTES"
echo "Rutas configuradas en $CONTAINER_NAME."

echo "Configuración de comandos basicos y rutas completada para todos los servidores."
