#!/bin/bash

NUM_CONTAINERS="$1"

CONFIGURE_FRR="
apt update && apt install -y iproute2 && apt install -y procps && apt install -y iputils-ping &&\
ip route del default
"

for i in $(seq 1 "$NUM_CONTAINERS"); do
    CONTAINER_NAME="pc$i"
    docker exec "$CONTAINER_NAME" bash -c "$CONFIGURE_FRR"
    echo "COMANDOS BASICOS configurados en $CONTAINER_NAME."
done

for i in $(seq 1 "$NUM_CONTAINERS"); do
    CONTAINER_NAME="pc$i"

    case $i in
        1)
            ROUTES="
                ip route add default via 10.0.1.20
            "
            ;;
        2)
            ROUTES="
                ip route add default via 10.0.2.20
            "
            ;;
        3)
            ROUTES="
                ip route add default via 10.0.3.20
            "
            ;;
        4)
            ROUTES="
                ip route add default via 10.0.4.20
            "
            ;;
        *)
            ROUTES="
                ip route add default via 10.0.1.1
            "
            ;;
    esac

    docker exec "$CONTAINER_NAME" bash -c "$ROUTES"
    echo "Rutas configuradas en $CONTAINER_NAME."
done

echo "Configuración de comandos basicos y rutas completada para todos los contenedores."
