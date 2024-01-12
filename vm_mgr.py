# Creates a libvirt VM configuration and disk

from subprocess import run
import os
import xml.etree.ElementTree as ET
import libvirt
from nfra_config import *
from libvirt_common import open_hyper_conn
import uuid

# Create a random disk image name (length of 16 preferred)

def create_uuid_disk_name() -> str:
    u = uuid.uuid4()
    return str(u)

# Create a qemu disk image for the VM (size in MB)

def create_disk(
    size : int,
    format_type : str,
    name_length : int
 ) -> str:
    name = create_uuid_disk_name()
    create_command = ("qemu-img create -f " +
        format_type +
        " " +
        os.path.join(NFRA_VM_PATH, name+"."+format_type) +
        " " +
        str(size)+
        "M")
    output = run(create_command, shell=True)
    return name

# Set libvirt xml name
def set_xml_name(
    template_file : str,
    dest_file : str,
    name : str
) -> None:
    tree = ET.parse(template_file)
    root = tree.getroot()
    root[0].text = name
    tree.write(dest_file)
    return None

def set_xml_uuid(
    template_file : str,
    dest_file : str,
    uuid : str
) -> None:
    tree = ET.parse(template_file)
    root = tree.getroot()
    root[1].text = uuid
    tree.write(dest_file)
    return None

def set_xml_memory(
    template_file : str,
    dest_file : str,
    size : int
) -> None:
    tree = ET.parse(template_file)
    root = tree.getroot()
    root[2].text = str(size)
    root[3].text = str(size)
    tree.write(dest_file)
    return None

def set_xml_vcpu(
    template_file : str,
    dest_file : str,
    vcpus : int
) -> None:
    tree = ET.parse(template_file)
    root = tree.getroot()
    root[4].text = str(vcpus)
    tree.write(dest_file)
    return None

def set_xml_disk(
    template_file : str,
    dest_file : str,
    file : str
) -> None:
    tree = ET.parse(template_file)
    root = tree.getroot()
    root[6][1][0].set("file", file)
    tree.write(dest_file)
    return None

def set_xml_cdrom(
    template_file : str,
    dest_file : str,
    file : str
) -> None:
    tree = ET.parse(template_file)
    root = tree.getroot()
    root[6][2][0].set("file", file)
    tree.write(dest_file)
    return None

def get_vm_name_xml(file : str):
    tree = ET.parse(template_file)
    root = tree.getroot()
    return root[0].text

# Create the VM libvirt xml, disk

def create_vm(
    template_file : str,
    name : str,
    memory_size : int,
    vcpus : int,
    disk_size : int,
    disk_format : str,
) -> str:
    print("Creating VM", name)
    dest_file = os.path.join(NFRA_VM_XML_PATH, name+".xml")
    disk_uuid = create_disk(size=disk_size, format_type=disk_format, name_length=16)

    set_xml_name(template_file=template_file, dest_file=dest_file, name=name)
    set_xml_uuid(template_file=dest_file, dest_file=dest_file, uuid=disk_uuid)
    set_xml_memory(template_file=dest_file, dest_file=dest_file, size=memory_size)
    set_xml_vcpu(template_file=dest_file, dest_file=dest_file, vcpus=vcpus)
    set_xml_disk(template_file=dest_file, dest_file=dest_file, file=os.path.join(NFRA_VM_XML_PATH, disk_uuid+"."+disk_format))
    return dest_file

def start_vm(
    file : str
) -> bool:

    name = get_vm_name_xml(file)
    conn = open_hyper_conn
    
    dom0 = conn.lookupByName(name)
    if dom0:
        print("%s: id %d already running %s" % (name, dom0.ID(), dom0.OSType()))
        print(dom0.info())
    else:
        output = conn.createxml(file)
    dom0 = conn.lookupByName(name)
    if dom0:
        print("%s: id %d successfully started %s" % (name, dom0.ID(), dom0.OSType()))
        print(dom0.info())
    else:
        output = conn.createxml(file)
    close_hyper_conn(conn)
    return True

vm_xml_file = create_vm(
    template_file=os.path.join(NFRA_TEMPLATES, "vm_template.xml"),
    name="debian0",
    memory_size=1024,
    vcpus=1,
    disk_size=5120,
    disk_format="raw")
print(vm_xml_file)
