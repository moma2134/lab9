import openstack

def setup_networks(conn):
    # Define network parameters
    networks = [
        {
            "name": "vn1_python", 
            "subnet_name": "subnet1_python", 
            "subnet_cidr": "192.168.80.0/24"
        }
    ]
    public_network_name = "public"

    # Create networks and subnets
    for net in networks:
        network = conn.network.create_network(name=net["name"])
        subnet = conn.network.create_subnet(
            name=net["subnet_name"],
            network_id=network.id,
            cidr=net["subnet_cidr"],
            ip_version=4
        )
        print(f"Network '{net['name']}' and subnet '{net['subnet_name']}' created.")

    # Get public network ID
    public_network = conn.network.find_network(public_network_name)

    # Connect networks to the public network
    for net in networks:
        conn.network.add_gateway_to_router(
            router="R1",
            network_id=public_network.id
        )
        print(f"Network '{net['name']}' connected to the public network.")

    print("All networks connected to the public network.")
