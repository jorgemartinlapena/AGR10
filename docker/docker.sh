bash borrar_docker.sh
python3 yaml_generate.py
docker-compose up -d
bash pcs.sh 4
bash routers.sh 4
