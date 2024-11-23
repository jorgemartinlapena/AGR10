#!/bin/bash

NUM_CONTAINERS="$1"

CONFIGURE_FRR="
echo 'zebra=yes' >> /etc/frr/daemons && \
echo 'zebra_options=\"-s 90000000 --daemon -A 127.0.0.1\"' >> /etc/frr/daemons && \
echo -e 'zebrasrv\t2600/tcp\t# zebra service' >> /etc/services && \
echo -e 'zebra\t\t2601/tcp\t# zebra vty' >> /etc/services && \
sysctl -w net.ipv4.ip_forward=1 && \
sysctl -p && \
/etc/init.d/frr start
"

for i in $(seq 1 "$NUM_CONTAINERS"); do
    CONTAINER_NAME="router$i"
    docker exec "$CONTAINER_NAME" bash -c "$CONFIGURE_FRR"
    echo "FRR configurado en $CONTAINER_NAME."
done

for i in $(seq 1 "$NUM_CONTAINERS"); do
    CONTAINER_NAME="router$i"

    case $i in
        1)
            ROUTES="
            vtysh -c 'configure' \
                  -c 'ip route 10.0.3.0/24 10.1.0.20' \
                  -c 'ip route 10.0.4.0/24 10.1.0.20' \
                  -c 'ip route 10.0.0.0/24 10.1.0.20' \
                  -c 'ip route 10.2.0.0/24 10.1.0.20' \
                  -c 'ip route 10.3.0.0/24 10.1.0.20' \
                  -c 'exit'
            "
            ;;
        2)
            ROUTES="
            vtysh -c 'configure' \
                  -c 'ip route 10.0.1.0/24 10.2.0.20' \
                  -c 'ip route 10.0.2.0/24 10.2.0.20' \
                  -c 'ip route 10.0.0.0/24 10.2.0.20' \
                  -c 'ip route 10.1.0.0/24 10.2.0.20' \
                  -c 'ip route 10.3.0.0/24 10.2.0.20' \
                  -c 'exit'
            "
            ;;
        3)
            ROUTES="
            vtysh -c 'configure' \
                  -c 'ip route 10.0.1.0/24 10.1.0.10' \
                  -c 'ip route 10.0.2.0/24 10.1.0.10' \
                  -c 'ip route 10.0.3.0/24 10.2.0.10' \
                  -c 'ip route 10.0.4.0/24 10.2.0.10' \
                  -c 'ip route 10.3.0.0/24 10.0.0.10' \
                  -c 'exit'
            "
            ;;
        4)
            ROUTES="
            vtysh -c 'configure' \
                  -c 'ip route 10.0.1.0/24 10.0.0.20' \
                  -c 'ip route 10.0.2.0/24 10.0.0.20' \
                  -c 'ip route 10.0.3.0/24 10.0.0.20' \
                  -c 'ip route 10.0.4.0/24 10.0.0.20' \
                  -c 'ip route 10.1.0.0/24 10.0.0.20' \
                  -c 'ip route 10.2.0.0/24 10.0.0.20' \
                  -c 'exit'
            "
            ;;
        *)
            ROUTES="
            vtysh -c 'configure' \
                  -c 'ip route 10.0.1.0/24 10.2.0.20' \
                  -c 'ip route 10.0.2.0/24 10.2.0.20' \
                  -c 'ip route 10.0.0.0/24 10.2.0.20' \
                  -c 'ip route 10.1.0.0/24 10.2.0.20' \
                  -c 'ip route 10.3.0.0/24 10.2.0.20' \
                  -c 'exit'
            "
            ;;
    esac

    docker exec "$CONTAINER_NAME" bash -c "$ROUTES"
    echo "Rutas configuradas en $CONTAINER_NAME."
done

echo "Configuración de FRR y rutas completada para todos los contenedores."


