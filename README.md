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

These variables are called when you run the 'test.yml' playbook.

test.yml:

    ---
    - hosts: vpn_hub1
      connection: local
      gather_facts: false
 
      tasks:
      - name: create dmvpn hub configuration
        template: src=roles/dmvpn_hub/templates/hub.j2  dest=output/{{ item.hostname }}.conf
        with_items: hub_vars
        delegate_to: 127.0.0.1
 
 
    - hosts: vpn_spoke1
      connection: local
      gather_facts: false
 
      tasks:
      - name: create dmvpn spoke configuration
        template: src=roles/dmvpn_spoke/templates/spoke.j2  dest=output/{{ item.hostname }}.conf
        with_items: spoke_vars
        delegate_to: 127.0.0.1

In the playbook, vpn_hub1 is called as a host. It's variables are read from the hosts_vars/vpn_hub1 file, then they are applied against the roles/dmvpn_hub/templates/hub.j2 template and create an output in output/vpn_hub1.conf. The same process is run for vpn_spoke1. In this playbook, ansible doesn't actually attempt to remotely access the devices, but rather processes everything locally. This is due to the 'delegate_to: 127.0.0.1' call. 

Here is the output:

    [semper@bastion net-ansible]$ rm -rf output/*
    [semper@bastion net-ansible]$ ansible-playbook -i hosts test.yml 
    
    PLAY [vpn_hub1] *************************************************************** 

    TASK: [create dmvpn hub configuration] **************************************** 
    changed: [vpn_hub1 -> 127.0.0.1] => (item={'transform_set': 'DMVPN_TRANSFORM', 'preshared_key': 'O5DXCYSJRNipNnfZ2eVm6JJvEcr2OvksWWZ0hTk2hwcpe8mz1AulEveGSyeg2MET', 'hostname': 'vpn_hub1', 'source_ip': '111.111.111.111', 'isakmp_policy': 1, 'dh_group': 2, 'v6_cidr': 64, 'ipsec_profile': 'DMVPN_IPSEC', 'network_mask': '255.255.255.0', 'tunnel_int': 123, 'peer_address': '0.0.0.0', 'tunnel_ipv6': '2001:10::1', 'tunnel_ipv4': '10.0.0.1'})
    
    PLAY [vpn_spoke1] ************************************************************* 
    
    TASK: [create dmvpn spoke configuration] ************************************** 
    changed: [vpn_spoke1 -> 127.0.0.1] => (item={'hostname': 'vpn_spoke1', 'hub_tunnel_ipv6': '2001:10::1', 'hub_tunnel_ipv4': '10.0.0.1', 'network_mask': '255.255.255.0', 'ipsec_profile': 'DMVPN_IPSEC', 'peer_address': '0.0.0.0', 'tunnel_ipv6': '2001:10::2', 'tunnel_ipv4': '10.0.0.2', 'dh_group': 2, 'preshared_key': 'O5DXCYSJRNipNnfZ2eVm6JJvEcr2OvksWWZ0hTk2hwcpe8mz1AulEveGSyeg2MET', 'hub_nmba_ipv4': '111.111.111.111', 'source_ip': '222.222.222.222', 'isakmp_policy': 1, 'transform_set': 'DMVPN_TRANSFORM', 'v6_cidr': 64, 'tunnel_int': 123})
    
    PLAY RECAP ******************************************************************** 
    vpn_hub1                   : ok=1    changed=1    unreachable=0    failed=0   
    vpn_spoke1                 : ok=1    changed=1    unreachable=0    failed=0   
    
    [semper@bastion net-ansible]$ cat output/vpn_hub1.conf 
    crypto isakmp policy 1 
     encr aes
     authentication pre-share
     group 2
    !
    crypto ipsec transform-set DMVPN_TRANSFORM esp-aes esp-sha-hmac 
     mode tunnel
    !
    crypto ipsec profile DMVPN_IPSEC
     set transform-set DMVPN_TRANSFORM 
    !
    crypto isakmp key O5DXCYSJRNipNnfZ2eVm6JJvEcr2OvksWWZ0hTk2hwcpe8mz1AulEveGSyeg2MET address 0.0.0.0
    !
    interface tunnel 123
     ip address 10.0.0.1 255.255.255.0
     ip mtu 1400
     ipv6 address 2001:10::1/64
     ipv6 mtu 1400
     tunnel source 111.111.111.111
     tunnel mode gre multipoint
     tunnel key 123
     ip nhrp network-id 123
     ip nhrp map multicast dynamic
     ipv6 nhrp network-id 123
     ipv6 nhrp map multicast dynamic
     tunnel protection ipsec profile DMVPN_IPSEC
     no shutdown
    [semper@bastion net-ansible]$
