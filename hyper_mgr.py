import libvirt

conn = libvirt.open("qemu:///system")
if not conn:
    raise SystemExit("Failed to open connection to qemu:///system")

vcpus = conn.getMaxVcpus(None)
print("Maximum support virtual CPUs: {}".format(vcpus))

conn.close()
