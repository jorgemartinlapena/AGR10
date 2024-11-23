# Primero borrar Docker
echo "========Eliminando configuraciones de Docker previas para un arranque limpio========"
bash ./utils/borrar_docker.sh
# Generamos Python
echo "Generamos YAML personalizado"
python3 ./utils/yaml_generate.py
echo "========Configuramos FLUENTD==========="
bash fluentd.sh
echo "========Docker-compose========"
docker-compose up -d
echo "========Configuramos PCs========"
bash pcs.sh 4
echo "========Configuramos ROUTERS========"
bash routers.sh 4
echo "========Configuramos SERVER========"
bash server.sh

