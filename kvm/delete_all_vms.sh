#!/bin/bash

# Obtener la lista de todas las máquinas virtuales (incluidas las apagadas)
vms=$(virsh list --all --name)

# Verificar si hay máquinas virtuales
if [ -z "$vms" ]; then
    echo "No hay máquinas virtuales para eliminar."
    exit 0
fi

# Iterar sobre cada máquina virtual
for vm in $vms; do
    echo "Procesando máquina virtual: $vm"

    # Apagar la máquina si está corriendo
    if virsh domstate "$vm" | grep -q "running"; then
        echo "Apagando máquina virtual: $vm"
        virsh destroy "$vm"
    fi

    # Eliminar la máquina virtual
    echo "Eliminando máquina virtual: $vm"
    virsh undefine "$vm" --remove-all-storage
done

echo "Todas las máquinas virtuales han sido eliminadas."
