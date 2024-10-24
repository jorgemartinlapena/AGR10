import os
import xml.etree.ElementTree as ET
import sys
import xml.dom.minidom

# Función para generar la configuración de red
def generate_network_config(vm_name, output_dir):
    # Extraer el número de la VM
    try:
        vm_num = int(vm_name.replace('virtual', ''))
    except ValueError:
        print(f"Nombre de VM inválido: {vm_name}")
        return

    config = """auto lo
iface lo inet loopback
"""

    # Configuración para PCs en las redes 1, 2, 3, 4
    if vm_num in [1, 2, 3, 4]:
        ip_address = f"10.0.{vm_num}.1"
        gateway = f"10.0.{vm_num}.2"  # El gateway es el router de la red correspondiente
        config += f"auto eth0\niface eth0 inet static\n\taddress {ip_address}\n\tnetmask 255.255.255.0\n\tgateway {gateway}\n"
    
    # Configuración para los routers
    elif vm_num == 5:
        config += """auto eth0
iface eth0 inet static
	address 10.1.0.1
	netmask 255.255.255.252
auto eth1
iface eth1 inet static
	address 10.0.1.2
	netmask 255.255.255.0
auto eth2
iface eth2 inet static
	address 10.0.2.2
	netmask 255.255.255.0
"""
    elif vm_num == 6:
        config += """auto eth0
iface eth0 inet static
	address 10.2.0.1
	netmask 255.255.255.252
auto eth1
iface eth1 inet static
	address 10.0.3.2
	netmask 255.255.255.0
auto eth2
iface eth2 inet static
	address 10.0.4.2
	netmask 255.255.255.0
"""
    elif vm_num == 7:
        config += """auto eth0
iface eth0 inet static
	address 10.0.0.2
	netmask 255.255.255.252
auto eth1
iface eth1 inet static
	address 10.1.0.2
	netmask 255.255.255.252
auto eth2 
iface eth2 inet static
	address 10.2.0.2
	netmask 255.255.255.252
"""
    elif vm_num == 8:
        config += """auto eth0
iface eth0 inet static
	address 10.0.0.1
	netmask 255.255.255.252
"""

    # Guardar la configuración en un archivo
    os.makedirs(output_dir, exist_ok=True)
    config_filename = f"{output_dir}/interfaces"

    with open(config_filename, 'w') as config_file:
        config_file.write(config)

    return config_filename

def modify_domain_xml(xml_string, vm_name, bridge_name):
    # Parsear el XML
    root = ET.fromstring(xml_string)
    
    # Modificar el nombre de la VM
    name_element = root.find('name')
    if name_element is not None:
        name_element.text = vm_name
    
    # Modificar la ruta del archivo QCOW2
    disk_element = root.find(".//disk/source")
    if disk_element is not None:
        disk_element.set('file', f'/home/alumno/AGR10/{vm_name}/{vm_name}.qcow2')
    
    # Eliminar interfaces existentes antes de agregar nuevas
    devices_element = root.find('devices')
    existing_interfaces = devices_element.findall('interface')
    for interface in existing_interfaces:
        devices_element.remove(interface)
    
    # Inicializar variable bridges con una lista vacía para evitar errores
    bridges = []

    # Agregar las interfaces adicionales dependiendo del número de la VM
    if bridge_name == "virtual1":
        bridges = ["virtual1"]
    elif bridge_name == "virtual2":
        bridges = ["virtual2"]
    elif bridge_name == "virtual3":
        bridges = ["virtual3"]
    elif bridge_name == "virtual4":
        bridges = ["virtual4"]
    elif bridge_name == "virtual5":
        bridges = ["virtual5", "virtual1", "virtual2"]
    elif bridge_name == "virtual6":
        bridges = ["virtual6", "virtual3", "virtual4"]
    elif bridge_name == "virtual7":
        bridges = ["virtual7", "virtual5", "virtual6"]
    elif bridge_name == "virtual8":
        bridges = ["virtual7"]

    # Agregar las nuevas interfaces basadas en los bridges
    for bridge in bridges:
        interface = ET.Element('interface', {'type': 'bridge'})
        source = ET.SubElement(interface, 'source', {'bridge': bridge})
        model = ET.SubElement(interface, 'model', {'type': 'virtio'})
        devices_element.append(interface)
    
    # Convertir el árbol a cadena de XML sin formato
    rough_string = ET.tostring(root, encoding='unicode')
    
    # Usar xml.dom.minidom para formatear el XML
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="")
    
    return pretty_xml
    

# XML de ejemplo
xml_string = """<domain type='kvm'>
  <name>XXX</name>
  <memory>1048576</memory>
  <currentMemory>1048576</currentMemory>
  <vcpu>2</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <emulator>/usr/bin/kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/mnt/tmp/XXX/XXX.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <source bridge='XXX'/>
      <model type='virtio'/>
    </interface>
    <serial type='pty'>
      <target port='0'/>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='-1' autoport='yes'/>
  </devices>
</domain>"""

if __name__ == "__main__":
    # Verificar si se proporcionaron los parámetros necesarios
    if len(sys.argv) < 3:
        print("Uso: python script.py <vm_name> <bridge_name>")
        sys.exit(1)
    
    vm_name = sys.argv[1]  # Obtener el nombre de la VM desde los argumentos
    bridge_name = sys.argv[2]  # Obtener el nombre del bridge
    
    # Modificar el XML con los parámetros dados
    modified_xml = modify_domain_xml(xml_string, vm_name, bridge_name)
    
    # Generar la configuración de red
    config_filename = generate_network_config(bridge_name, f'/home/alumno/AGR10/{vm_name}')

    
    # Mostrar el XML modificado
    print(modified_xml)


