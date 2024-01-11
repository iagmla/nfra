import libvirt

# Replace with qemu+ssh

def open_hyper_conn():
    conn = libvirt.open("qemu:///system")
    if not conn:
        raise print("Failed to open connection to qemu:///system")
    return conn

vcpus = conn.getMaxVcpus(None)
print("Maximum support virtual CPUs: {}".format(vcpus))

conn.close()
