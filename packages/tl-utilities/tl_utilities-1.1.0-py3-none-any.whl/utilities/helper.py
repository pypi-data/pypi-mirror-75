import re


def volume_convert_yaml_to_json(yaml_conf, version: str):
    """
    Convert yaml configuration to json used to create docker volume.
    Return array of dict, each dict is used in dcli.create_volume(...)
    :param yaml_conf: yaml configuration
    :param version: yaml version (support 2.x/3.x)
    """
    volume_conf_list = []
    # handle version 2
    #if re.match('^2\.(\d*)$', version):
    #    print("Convert volume yaml of version 2.x")
    # handle version 3
    if re.match('^3\.(\d*)$', version):
        for tup in yaml_conf.items():
            volume_conf = {'name': tup[0], 'driver_opts': {}, 'labels': {}}
            if not tup[1]:
                volume_conf['driver'] = 'local'

            if type(tup[1]) is dict:
                # check external
                try:
                    volume_conf['external'] = tup[1]['external']
                except KeyError:
                    pass

                # check driver
                try:
                    volume_conf['driver'] = tup[1]['driver']
                except KeyError:
                    volume_conf['driver'] = 'local'

                # check driver_opts
                try:
                    for dr_tup in tup[1]['driver_opts'].items():
                        volume_conf['driver_opts'][dr_tup[0]] = dr_tup[1]
                except KeyError:
                    pass

                # check labels
                try:
                    for l_tup in tup[1]['labels'].items():
                        volume_conf['labels'][l_tup[0]] = l_tup[1]
                except KeyError:
                    pass

            volume_conf_list.append(volume_conf)
        return volume_conf_list

    return {}


def network_convert_yaml_to_json(yaml_conf, version: str):
    """
    Convert yaml configuration to json used to create docker network.
    Return array of dict, each dict is used in dcli.create_network(...)
    :param yaml_conf: yaml configuration
    :param version: yaml version (support 2.x/3.x)
    """
    network_conf_list = []

    # handle version 2
    #if re.match('^2\.(\d*)$', version):
    #    print("Convert network yaml of version 2.x")

    # handle version 3
    if re.match('^3\.(\d*)$', version):
        for tup in yaml_conf.items():
            network_conf = {'name': tup[0], 'driver': None, 'options': None,
                            'ipam': None, 'check_duplicate': None, 'internal': False,
                            'labels': None, 'enable_ipv6': False, 'attachable': None,
                            'scope': None, 'ingress': None}

            if type(tup[1]) is dict:
                try:
                    network_conf['external'] = tup[1]['external']
                    network_conf_list.append(network_conf)
                    continue
                except KeyError:
                    pass

                # get driver of network
                try:
                    network_conf['driver'] = tup[1]['driver']
                except KeyError:
                    pass

                # get opts of driver
                try:
                    network_conf['options'] = {}
                    for dr_tup in tup[1]['driver_opts'].items():
                        network_conf['options'][dr_tup[0]] = dr_tup[1]
                except KeyError:
                    network_conf['options'] = None
                    pass

                # get ipam config
                try:
                    if tup[1]['ipam']:
                        ipam_conf = {'driver': 'default', 'pool_configs': [], 'options': None}
                        for ipam_tup in tup[1]['ipam'].items():
                            if ipam_tup[0] == 'driver':
                                ipam_conf['driver'] = ipam_tup[1]
                            if ipam_tup[0] == 'config':
                                for pool in ipam_tup[1]:
                                    pool_conf = {}
                                    if 'subnet' in pool:
                                        pool_conf['subnet'] = pool['subnet']
                                    if 'iprange' in pool:
                                        pool_conf['iprange'] = pool['iprange']
                                    if 'gateway' in pool:
                                        pool_conf['gateway'] = pool['gateway']
                                    if 'aux_addresses' in pool:
                                        pool_conf['aux_addresses'] = pool['aux_addresses']
                                    ipam_conf['pool_configs'].append(pool_conf)

                            if ipam_tup[0] == 'options':
                                ipam_conf['options'] = ipam_tup[1]
                        network_conf['ipam'] = ipam_conf

                except KeyError:
                    pass

                # get attachable
                try:
                    network_conf['attachable'] = tup[1]['attachable']
                except KeyError:
                    pass

                # get internal
                try:
                    network_conf['internal'] = tup[1]['internal']
                except KeyError:
                    pass

            network_conf_list.append(network_conf)
        return network_conf_list

    return {}


def container_convert_yaml_to_json(yaml_conf, version: str):
    """
    Convert yaml configuration to json used to create docker network.
    Return array of dict, each dict is used in dcli.create_container(...)
    :param yaml_conf: yaml configuration
    :param version: yaml version (support 2.x/3.x)
    """
    container_conf_list = []

    # handle version 2
    if re.match('^2\.(\d*)$', version):
        print("Convert container yaml of version 2.x")

    # handle version 3
    if re.match('^3\.(\d*)$', version):
        print("Convert container yaml of version 3.x")
        for tup in yaml_conf.items():
            container_conf = {
                'container_name': None,
                'image': None,
                'volumes': [],
                'command': [],
                'entrypoint': [],
                'network_mode': None,
                'networks': [],
                'labels': {},
                'expose': [],
                'extra_hosts': [],
                'dns': [],
                'dns_search': [],
                'environment': {},
                'ports': [],
                'restart': None,
                'sysctls': {},
                'tmpfs': [],
                'pid': None,
                'hostname': None,
                'privileged': False,
                'read_only': False
            }

            if type(tup[1]) is dict:
                # get container_name:
                try:
                    container_conf['container_name'] = tup[1]['container_name']
                except KeyError:
                    pass

                # get docker image
                try:
                    container_conf['image'] = tup[1]['image']
                except KeyError:
                    pass

                # get volumes:
                try:
                    for mount_cfg in tup[1]['volumes']:
                        container_conf['volumes'].append(mount_cfg)
                except KeyError:
                    pass

                # get docker commands
                try:
                    for cmd in tup[1]['command']:
                        container_conf['command'].append(cmd)
                except KeyError:
                    pass

                # get entrypoint
                try:
                    container_conf['entrypoint'] = tup[1]['entrypoint']
                except KeyError:
                    pass

                # get network_mode
                try:
                    container_conf['network_mode'] = tup[1]['network_mode']
                except KeyError:
                    pass

                # get networks
                try:
                    for network in tup[1]['networks']:
                        for net_tup in network.items():
                            net_conf = {'name': net_tup[0], 'config': {
                                'ipv4_address': None,
                                'ipv6_address': None,
                                'aliases': None
                            }}

                            if type(net_tup[1]) is dict:
                                try:
                                    net_conf['config']['ipv4_address'] = net_tup[1]['ipv4_address']
                                except KeyError:
                                    pass

                                try:
                                    net_conf['config']['ipv6_address'] = net_tup[1]['ipv6_address']
                                except KeyError:
                                    pass

                                try:
                                    net_conf['config']['aliases'] = net_tup[1]['aliases']
                                except KeyError:
                                    pass

                            container_conf['networks'].append(net_conf)
                except KeyError:
                    pass

                # get labels
                try:
                    for l_tup in tup[1]['labels'].items():
                        container_conf['labels'][l_tup[0]] = l_tup[1]
                except KeyError:
                    pass

                # get exposed ports
                try:
                    for port in tup[1]['expose']:
                        container_conf['expose'].append(int(port))
                except KeyError:
                    pass

                # get extra_hosts
                try:
                    for host in tup[1]['extra_hosts']:
                        container_conf['extra_hosts'].append(host)
                except KeyError:
                    pass

                # get dns
                try:
                    for ip in tup[1]['dns']:
                        container_conf['dns'].append(ip)
                except KeyError:
                    pass

                # get dns_search
                try:
                    for search in tup[1]['dns_search']:
                        container_conf['dns_search'].append(search)
                except KeyError:
                    pass

                # get environment
                try:
                    for env_tup in tup[1]['environment']:
                        container_conf['environment'][env_tup[0]] = env_tup[1]
                except KeyError:
                    pass

                # get ports
                try:
                    for port in tup[1]['ports']:
                        port_tup = tuple(part for part in port.split(':') if part)

                        # port bindings with specified host ip address
                        if len(port_tup) == 3:
                            # port bindings with protocol
                            if '/' in port_tup[2]:
                                proto_tup = tuple(part for part in port_tup[2].split(':') if part)
                                container_conf['ports'].append({
                                    'host_ip': port_tup[0],
                                    'host_port': int(port_tup[1]),
                                    'cont_port': int(proto_tup[0]),
                                    'proto': proto_tup[1]
                                })
                            else:
                                container_conf['ports'].append({
                                    'host_ip': port_tup[0],
                                    'host_port': int(port_tup[1]),
                                    'cont_port': int(port_tup[0])
                                })
                        # port bindings without specified host ip address
                        if len(port_tup) == 2:
                            # port bindings with protocol
                            if '/' in port_tup[1]:
                                proto_tup = tuple(part for part in port_tup[2].split(':') if part)
                                container_conf['ports'].append({
                                    'host_port': int(port_tup[0]),
                                    'cont_port': int(proto_tup[0]),
                                    'proto': proto_tup[1]
                                })
                            else:
                                container_conf['ports'].append({
                                    'host_port': int(port_tup[0]),
                                    'cont_port': int(port_tup[0])
                                })

                        # port exposed
                        if len(port_tup) == 1:
                            container_conf['ports'].append({
                                'host_port': None,
                                'cont_port': port_tup[0]
                            })

                except KeyError:
                    pass

                # get restart_policy
                try:
                    container_conf['restart'] = tup[1]['restart']
                except KeyError:
                    pass

                # get sysctls
                try:
                    for sys_tup in tup[1]['sysctls'].items():
                        container_conf['sysctls'][sys_tup[0]] = sys_tup[1]
                except KeyError:
                    pass

                # get tmpfs
                try:
                    container_conf['tmpfs'] = tup[1]['tmpfs']
                except KeyError:
                    pass

                # get pid
                try:
                    container_conf['pid'] = tup[1]['pid']
                except KeyError:
                    pass

                # get hostname
                try:
                    container_conf['hostname'] = tup[1]['hostname']
                except KeyError:
                    pass

                # get privileged
                try:
                    container_conf['privileged'] = tup[1]['privileged']
                except KeyError:
                    pass

                # get read_only
                try:
                    container_conf['read_only'] = tup[1]['read_only']
                except KeyError:
                    pass

                container_conf_list.append(container_conf)

    return container_conf_list
