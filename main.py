from network_setup import setup_networks
from vm_setup import setup_vms
from security_setup import setup_security_groups
import openstack

def main():
    # Initialize connection to the OpenStack cloud using password authentication
    conn = openstack.connect(
        auth=dict(
            auth_url = 'http://192.168.1.16/identity',
            username = 'lab9_admin',
            password = 'password',
            project_name = 'lab9',
            user_domain_name = 'default',
            project_domain_name = 'default'
        )
    )

    # Perform network setup
    print("Setting up networks...")
    setup_networks(conn=conn)

    # Perform VM setup
    print("Setting up VMs...")
    setup_vms(conn=conn)

    # Perform security setup
   # print("Setting up security groups...")
   # setup_security_groups(conn=conn)

if __name__ == "__main__":
    main()
