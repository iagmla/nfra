import libvirt

# Replace with qemu+ssh

def open_hyper_conn():
    conn = libvirt.open("qemu:///system")
    if not conn:
        raise print("Failed to open connection to qemu:///system")
    return conn

def close_hyper_conn(conn):
    conn.close()
