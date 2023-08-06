
        return self._instance_start(instance_uuid, instance, network, namespace, placed_on)

    def _instance_start(self, instance_uuid, instance, network, namespace, placed_on):
        

        # Nodes we have attempted to start on
        attempts = []

        while len(attempts) < 3:
            
            attempts.append(placement)

            # Have we been placed on a different node?
            if not placement == config.parsed.get('NODE_NAME'):
                resp = self._instance_start_remote(
                    placement, instance_uuid, namespace)
                if placed_on or resp.status_code != 507:
                    return resp
                placement = None
            else:
                return self._instance_start_local(instance_uuid, instance, network, namespace)

        # Give up for real
        db.add_event('instance', instance_uuid,
                     'schedule', 'failed', None, 'insufficient resources after retries')
        db.update_instance_state(instance_uuid, 'error', 'insufficient capacity after retries')
        return error(507, 'insufficient capacity after retries')

    def _instance_start_remote(self, placed_on, instance_uuid, namespace):
        body = flask_get_post_body()
        body['placed_on'] = placed_on
        body['instance_uuid'] = instance_uuid
        body['namespace'] = namespace

        # NOTE(mikal): the user of the system namespace is deliberate here. The
        # namespace to create the instance in is specified above, but we need to
        # make this call as system because we have specified an instance UUID.
        token = util.get_api_token(
            'http://%s:%d' % (placed_on, config.parsed.get('API_PORT')),
            namespace='system')
        r = requests.request('POST',
                             'http://%s:%d/instances'
                             % (placed_on,
                                config.parsed.get('API_PORT')),
                             data=json.dumps(body),
                             headers={'Authorization': token,
                                      'User-Agent': util.get_user_agent()})

        LOG.info('Returning proxied request: %d, %s'
                 % (r.status_code, r.text))
        resp = flask.Response(r.text,
                              mimetype='application/json')
        resp.status_code = r.status_code
        return resp

    def _instance_start_local(self, instance_uuid, instance, network, namespace):
        # Check we can get the required IPs
        nets = {}
        allocations = {}

        def error_with_cleanup(status_code, message):
            for network_uuid in allocations:
                n = net.from_db(network_uuid)
                for addr, _ in allocations[network_uuid]:
                    with db.get_lock('sf/ipmanager/%s' % n.uuid, ttl=120) as _:
                        ipm = db.get_ipmanager(n.uuid)
                        ipm.release(addr)
                        db.persist_ipmanager(n.uuid, ipm.save())
            return error(status_code, message)

        order = 0
        if network:
            for netdesc in network:
                if 'network_uuid' not in netdesc or not netdesc['network_uuid']:
                    return error_with_cleanup(404, 'network not specified')

                if netdesc['network_uuid'] not in nets:
                    n = net.from_db(netdesc['network_uuid'])
                    if not n:
                        return error_with_cleanup(
                            404, 'network %s not found' % netdesc['network_uuid'])
                    nets[netdesc['network_uuid']] = n
                    n.create()

                with db.get_lock('sf/ipmanager/%s' % netdesc['network_uuid'],
                                 ttl=120) as _:
                    db.add_event('network', netdesc['network_uuid'], 'allocate address',
                                 None, None, instance_uuid)
                    allocations.setdefault(netdesc['network_uuid'], [])
                    ipm = db.get_ipmanager(netdesc['network_uuid'])
                    if 'address' not in netdesc or not netdesc['address']:
                        netdesc['address'] = ipm.get_random_free_address()
                    else:
                        if not ipm.reserve(netdesc['address']):
                            return error_with_cleanup(409, 'address %s in use' %
                                                      netdesc['address'])
                    db.persist_ipmanager(netdesc['network_uuid'], ipm.save())
                    allocations[netdesc['network_uuid']].append(
                        (netdesc['address'], order))

                if 'model' not in netdesc or not netdesc['model']:
                    netdesc['model'] = 'virtio'

                db.create_network_interface(
                    str(uuid.uuid4()), netdesc, instance_uuid, order)

                order += 1

        # Initialise metadata
        db.persist_metadata('instance', instance_uuid, {})

        # Now we can start the instance
        with db.get_lock('sf/instance/%s' % instance.db_entry['uuid'], ttl=900) as lock:
            with util.RecordedOperation('ensure networks exist', instance) as _:
                for network_uuid in nets:
                    n = nets[network_uuid]
                    n.ensure_mesh()
                    n.update_dhcp()

            libvirt = util.get_libvirt()
            try:
                with util.RecordedOperation('instance creation',
                                            instance) as _:
                    instance.create(lock=lock)

            except libvirt.libvirtError as e:
                code = e.get_error_code()
                if code in (libvirt.VIR_ERR_CONFIG_UNSUPPORTED,
                            libvirt.VIR_ERR_XML_ERROR):
                    return error_with_cleanup(400, e.get_error_message())
                raise e

            for iface in db.get_instance_interfaces(instance.db_entry['uuid']):
                db.update_network_interface_state(iface['uuid'], 'created')

            return db.get_instance(instance_uuid)
