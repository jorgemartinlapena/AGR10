import yaml

def generate_yaml():
    config = {
        'version': '3.9',
        'services': {},
        'networks': {}
    }

    # Definimos los PCs
    config['services']['pc1'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'pc1',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred1': {
                'ipv4_address': '10.0.1.10'
            }
        },
    }

    config['services']['pc2'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'pc2',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred2': {
                'ipv4_address': '10.0.2.10'
            }
        },
    }

    config['services']['pc3'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'pc3',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred3': {
                'ipv4_address': '10.0.3.10'
            }
        },
    }

    config['services']['pc4'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'pc4',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred4': {
                'ipv4_address': '10.0.4.10'
            }
        },
    }

    # Definimos los routers intermedios
    config['services']['router1'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'router1',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred1': {'ipv4_address': '10.0.1.20'},
            'subred2': {'ipv4_address': '10.0.2.20'},
            'subred5': {'ipv4_address': '10.1.0.10'}
        },
    }

    config['services']['router2'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'router2',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred3': {'ipv4_address': '10.0.3.20'},
            'subred4': {'ipv4_address': '10.0.4.20'},
            'subred6': {'ipv4_address': '10.2.0.10'}
        },
    }

    # Definimos el router superior
    config['services']['router3'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'router3',
        'command': 'sleep infinity',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred5': {'ipv4_address': '10.1.0.20'},
            'subred6': {'ipv4_address': '10.2.0.20'},
            'subred7': {'ipv4_address': '10.0.0.20'}
        },
    }

    # Definimos el router principal
    config['services']['router4'] = {
        'image': 'ubuntu:20.04',
        'container_name': 'router4',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sleep infinity',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred7': {'ipv4_address': '10.0.0.10'},
            'subred8': {'ipv4_address': '10.3.0.10'}
        },
    }

    # Definimos las subredes
    config['networks']['subred1'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.0.1.0/24'}]
        }
    }
    config['networks']['subred2'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.0.2.0/24'}]
        }
    }
    config['networks']['subred3'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.0.3.0/24'}]
        }
    }
    config['networks']['subred4'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.0.4.0/24'}]
        }
    }
    config['networks']['subred5'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.1.0.0/24'}]
        }
    }
    config['networks']['subred6'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.2.0.0/24'}]
        }
    }
    config['networks']['subred7'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.0.0.0/24'}]
        }
    }
    config['networks']['subred8'] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': '10.3.0.0/24'}]
        }
    }
    # Guardar configuración en YAML
    with open('docker-compose.yml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == "__main__":
    generate_yaml()

