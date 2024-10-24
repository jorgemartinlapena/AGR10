import xml.etree.ElementTree as ET
import sys

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
    
    # Modificar el bridge por defecto de virsh
    interface_element = root.find(".//interface/source")
    if interface_element is not None:
        interface_element.set('bridge', bridge_name)
    
    # Convertir el árbol de nuevo a cadena de XML
    modified_xml = ET.tostring(root, encoding='unicode')
    return modified_xml

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
    # Verificar si se proporcionó el parámetro name
    if len(sys.argv) < 3:
        print("Uso: python script.py <vm_name>")
        sys.exit(1)
    
    vm_name = sys.argv[1]  # Obtener el nombre de la VM desde los argumentos
    bridge_name = sys.argv[2]
    modified_xml = modify_domain_xml(xml_string, vm_name, bridge_name)
    
    # Mostrar el XML modificado
    print(modified_xml)

