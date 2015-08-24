## net-ansible

This is just a test bed of playing with ansible, as it pertains to network engineering. Currently, I have a simple playbook to generate a the necessary tunnel interface configurations for a DMVPN hub and spoke via IOS. 


As I continue to learn and play with ansible, my thought is that this will turn into a repository for generating all sorts of configurations and hopefully it will get to the point that it can push configurations to devices. 


in the 'hosts' file, you will see:

    localhost
    
    [all:vars]
    ansible_connection=local
    ansible_ssh_host=localhost
    
    [dmvpn_hub]
    vpn_hub1
    
    [dmvpn_spoke]
    vpn_spoke1
    
    [ipsec_enabled:children]

This specifies the device inventory. Devices 'vpn_hub1' and 'vpn_spoke1' are fictional devices. Their device variables are found in host_vars/vpn_spoke1 and host_vars/vpn_hub1.

vpn_spoke1:

    ---
    spoke_vars:
      - { hostname: vpn_spoke1,
          tunnel_int: 123,
          tunnel_ipv4: 10.0.0.2,
          network_mask: 255.255.255.0,
          tunnel_ipv6: '2001:10::2',
          v6_cidr: 64,
          source_ip: 222.222.222.222,
          hub_tunnel_ipv4: 10.0.0.1,
          hub_tunnel_ipv6: '2001:10::1',
          hub_nmba_ipv4: 111.111.111.111,
          isakmp_policy: 1,
          dh_group: 2,
          transform_set: DMVPN_TRANSFORM,
          ipsec_profile: DMVPN_IPSEC,
          preshared_key: O5DXCYSJRNipNnfZ2eVm6JJvEcr2OvksWWZ0hTk2hwcpe8mz1AulEveGSyeg2MET,
          peer_address: 0.0.0.0 }

vpn_hub1:

    ---
    hub_vars:
      - { hostname: vpn_hub1,
          tunnel_int: 123,
          tunnel_ipv4: 10.0.0.1,
          network_mask: 255.255.255.0,
          tunnel_ipv6: '2001:10::1',
          v6_cidr: 64,
          source_ip: 111.111.111.111,
          isakmp_policy: 1,
          dh_group: 2,
          transform_set: DMVPN_TRANSFORM,
          ipsec_profile: DMVPN_IPSEC,
          preshared_key: O5DXCYSJRNipNnfZ2eVm6JJvEcr2OvksWWZ0hTk2hwcpe8mz1AulEveGSyeg2MET,
          peer_address: 0.0.0.0 }

More later.
