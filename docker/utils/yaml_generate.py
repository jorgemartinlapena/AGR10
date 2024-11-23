import yaml

def generate_yaml():
    config = {
        'version': '3.9',
        'services': {},
        'networks': {}
    }

    # Definimos los PCs
    config['services']['pc1'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'pc1',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por PC1.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred1': {
                'ipv4_address': '10.0.1.10',
            }
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    config['services']['pc2'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'pc2',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por PC2.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred2': {
                'ipv4_address': '10.0.2.10'
            }
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    config['services']['pc3'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'pc3',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por PC3.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred3': {
                'ipv4_address': '10.0.3.10'
            }
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    config['services']['pc4'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'pc4',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por PC4.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred4': {
                'ipv4_address': '10.0.4.10'
            }
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    # Definimos los routers intermedios
    config['services']['router1'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'router1',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por ROUTER1.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred1': {'ipv4_address': '10.0.1.20'},
            'subred2': {'ipv4_address': '10.0.2.20'},
            'subred5': {'ipv4_address': '10.1.0.10'}
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    config['services']['router2'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'router2',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por ROUTER2.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred3': {'ipv4_address': '10.0.3.20'},
            'subred4': {'ipv4_address': '10.0.4.20'},
            'subred6': {'ipv4_address': '10.2.0.10'}
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    # Definimos el router superior
    config['services']['router3'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'router3',
        'command': 'sleep infinity',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por ROUTER3.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred5': {'ipv4_address': '10.1.0.20'},
            'subred6': {'ipv4_address': '10.2.0.20'},
            'subred7': {'ipv4_address': '10.0.0.20'}
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }

    # Definimos el router principal
    config['services']['router4'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile'},
        'container_name': 'router4',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'sh -c "echo \'Todo configurado por ROUTER4.\' && sleep infinity"',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred7': {'ipv4_address': '10.0.0.10'},
            'subred8': {'ipv4_address': '10.3.0.10'}
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
    }
    
    config['services']['servidor1'] = {
        'build': {'context': '.', 'dockerfile': 'Dockerfile_npm'},
        'container_name': 'servidor',
        'platform': 'linux/amd64',
        'privileged': 'true',
        'command': 'node SSR-master-server/app.js',
        'cap_add': ['NET_ADMIN'],
        'networks': {
            'subred8': {'ipv4_address': '10.3.0.20'}
        },
        'logging': {
            'driver': 'fluentd',
            'options': {
                'fluentd-address': 'localhost:24224',
            }
        }
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

