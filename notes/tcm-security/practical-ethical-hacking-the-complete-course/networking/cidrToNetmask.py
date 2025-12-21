from ipaddress import IPv4Network

def cidr_to_netmask(cidr):
    network = IPv4Network(cidr)
    return str(network.netmask)

print(cidr_to_netmask("192.168.0.0/24"))
