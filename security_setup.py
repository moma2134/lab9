def setup_security_groups(conn):
    # Define security group rules
    intra_vn_rule = {
        'direction': 'ingress',
        'ethertype': 'IPv4',
        'protocol': 'tcp',
        'port_range_max': 80,
        'port_range_min': 80,
        'remote_ip_prefix': '0.0.0.0/0',
        'security_group_id': '',
    }
    inter_vn_rule = {
        'direction': 'ingress',
        'ethertype': 'IPv4',
        'protocol': 'icmp',
        'remote_ip_prefix': '',
        'security_group_id': '',
    }

    # Get all security groups
    sec_groups = list(conn.network.security_groups())

    for sec_group in sec_groups:
        # Apply rules for intra-VN communication
        if sec_group.name == 'intra_vn_group':
            intra_vn_rule['security_group_id'] = sec_group.id
            conn.network.create_security_group_rule(**intra_vn_rule)

        # Apply rules for inter-VN communication
        if sec_group.name == 'inter_vn_group':
            inter_vn_rule['security_group_id'] = sec_group.id
            conn.network.create_security_group_rule(**inter_vn_rule)

    print("Security groups and rules configured successfully.")
