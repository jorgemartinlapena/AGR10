#!/bin/bash

# Verificar si se pasó el número de duplicados como parámetro
if [ -z "$1" ]; then
	echo "Uso: $0 <numero_de_duplicados>"
	exit 1
fi

NUM_DUPLICADOS="$1"
QCOW2_ORIGINAL="/home/alumno/AGR10/agr-vm-base.qcow2"
BASE_DIR="/home/alumno/AGR10"
PYTHON_SCRIPT="/home/alumno/AGR10/modify_xml.py" # Ruta completa al script de Python

# Función para ejecutar comandos en la VM usando virsh console y expect
run_commands_in_vm() {
	local vm_name=$1
	local commands=$2
	expect -c "
    spawn sudo virsh console $vm_name
    expect {
      \"agr login:\" { send \"root\r\"; exp_continue }
      \"Password:\" { send \"agr\r\"; exp_continue }
      \"root@agr:~/#\" { send \"zebra; vtysh\r\"; exp_continue }
	  \"agr#\" { send \"configure terminal\r\"; exp_continue }
	  \"agr(config)#\" { send \"$commands\r\"; exp_continue }
	  \"agr(config)#\" { send \"exit\r\"; exp_continue }
	  \"agr(config)#\" { send \"exit\r\"; send \"exit\r\" }
    }
    expect eof
  "
}

# Iterar el número de veces que se especificó
for ((i = 1; i <= NUM_DUPLICADOS; i++)); do
	# Generar un nuevo UUID
	NEW_UUID=$(uuidgen)

	# Crear un nuevo directorio con el UUID
	VM_DIR="$BASE_DIR/$NEW_UUID"
	sudo mkdir "$VM_DIR"

	# Copiar el archivo qcow2 original al nuevo directorio con el nuevo nombre
	QCOW2_NUEVO="$VM_DIR/$NEW_UUID.qcow2"
	sudo qemu-img create -f qcow2 -b "$QCOW2_ORIGINAL" -F qcow2 "$QCOW2_NUEVO"

	echo "Duplicación $i: Archivo qcow2 duplicado en $QCOW2_NUEVO con UUID $NEW_UUID"

	# Llamar al script de Python para modificar el XML y pasarle el nuevo UUID como nombre de la VM
	virtual_name="virtual$i"

	sudo ifconfig "$virtual_name" down
	sudo brctl delbr "$virtual_name"

	sudo brctl addbr "$virtual_name"

	echo $virtual_name

	sudo ifconfig "$virtual_name" up

	sudo python3 "$PYTHON_SCRIPT" "$NEW_UUID" "$virtual_name" >"$VM_DIR/$NEW_UUID.xml"

	echo "XML para VM $NEW_UUID generado en $VM_DIR/$NEW_UUID.xml"

	sudo chown 777 "$VM_DIR"

	sudo virsh define "$VM_DIR/$NEW_UUID.xml"
	# sudo "virsh start $VM_DIR/$NEW_UUID.xml"

	sudo virt-copy-in -a $QCOW2_NUEVO "$VM_DIR/interfaces" "/etc/network"

	sudo virsh start $NEW_UUID

	touch "$VM_DIR/$i"

	# Ejecutar comandos específicos según el valor de i
	if [ "$i" -eq 5 ]; then
		commands="ip route 10.0.3.0/24 10.1.0.2; ip route 10.0.4.0/24 10.1.0.2; ip route 10.0.0.0/30 10.1.0.2; ip route 10.1.0.0/30 10.1.0.2; ip route 10.2.0.0/30 10.1.0.2"
	elif [ "$i" -eq 6 ]; then
		commands="ip route 10.0.1.0/24 10.2.0.2; ip route 10.0.2.0/24 10.2.0.2; ip route 10.0.0.0/30 10.2.0.2; ip route 10.1.0.0/30 10.2.0.2; ip route 10.2.0.0/30 10.2.0.2"
	elif [ "$i" -eq 7 ]; then
		commands="ip route 10.0.1.0/24 10.1.0.1; ip route 10.0.2.0/24 10.1.0.1; ip route 10.0.3.0/24 10.2.0.1; ip route 10.0.4.0/24 10.2.0.1"
	elif [ "$i" -eq 8 ]; then
		commands="ip route 10.0.1.0/24 10.0.0.2; ip route 10.0.2.0/24 10.0.0.2; ip route 10.0.3.0/24 10.0.0.2; ip route 10.0.4.0/24 10.0.0.2; ip route 10.1.0.0/30 10.0.0.2; ip route 10.2.0.0/30 10.0.0.2"
	else
		commands=""
	fi

	# Ejecutar comandos si la variable no está vacía
	if [ -n "$commands" ]; then
		run_commands_in_vm "$NEW_UUID" "$commands"
	fi

done

echo "Proceso completado. Se duplicaron $NUM_DUPLICADOS máquinas virtuales."
