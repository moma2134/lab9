import openstack

def setup_vms(conn):
    # Define VM parameters
    vms = [
        {"name": "vm1_python", "image": "cirros", "flavor": "m1.tiny", "network_name": "vn1_python"}
    ]

    # Get flavor and image IDs
    flavor = conn.compute.find_flavor("m1.tiny")
    image = conn.compute.find_image("cirros-0.6.2-x86_64-disk")

    # Create VMs
    for vm in vms:
        network = conn.network.find_network(vm["network_name"])
        server = conn.compute.create_server(
            name=vm["name"],
            flavor_id=flavor.id,
            image_id=image.id,
            networks=[{"uuid": network.id}]
        )
        print(f"VM '{vm['name']}' created.")

    # Wait for VMs to be active
    for vm in vms:
        server = conn.compute.find_server(vm["name"])
        conn.compute.wait_for_server(server=server)

    print("All VMs are active.")

    # Connect VN1 to R1 and then assing floating IP to that interface
    router = conn.network.find_router('lab9_router')

    # Retrieve network (VN1)
    network = conn.network.find_network('vn1_python')
   # print(type(network))

    # Add an interface to the router using the network
    conn.network.add_interface_to_router(router, subnet_id=network.subnet_ids[0])

    # Find the UUID of the public network
    public_network = conn.network.find_network(name_or_id='public')

    # Allocate a floating IP on the public network
    floating_ip = conn.network.create_ip(floating_network_id=public_network.id)

    # Associate the floating IP with the interface on the router
    conn.network.add_gateway_to_router(router, network_id=public_network.id)

    print(f"Interface added to router '{router.name}' from network '{network.name}'")
    print(f"Floating IP '{floating_ip['floating_ip_address']}' assigned to the interface")

    print("All VMs are accessible from the internet.")
