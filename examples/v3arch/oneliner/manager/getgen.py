# Various uses of GET Command Generator uses
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp import debug

#debug.setLogger(debug.Debug('secmod'))

cmdGen = cmdgen.CommandGenerator()

# Send SNMP GET request
#     with SNMPv2c, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for two OIDs: one in string form while another is in tuple form
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(('localhost', 161)),
        (1,3,6,1,2,1,1,1,0),
        '1.3.6.1.2.1.1.6.0'
    )

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

#from pysnmp import debug

#debug.setLogger(debug.Debug('all'))

# Send SNMP GET request
#     with SNMPv1, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for two instances of SNMPv2-MIB::sysDescr.0 MIB object
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('public', mpModel=0),
        cmdgen.UdpTransportTarget(('localhost', 161)),
        ('iso', 'org', 'dod', 'internet', 'mgmt', 'mib-2', 'system', 'sysDescr', 0),
        (('SNMPv2-MIB', 'sysDescr'), 0)
    )

#debug.setLogger(debug.Debug())

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send SNMP GET request
#     with SNMPv3 with user 'test-user', MD5 auth and DES privacy protocols
#     over IPv6/UDP
#     to an Agent at [::1]:161
#     for three OIDs in string form
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
        cmdgen.Udp6TransportTarget(('::1', 161)),
        '1.3.6.1.2.1.1.1.0',
        '1.3.6.1.2.1.1.2.0',
        '1.3.6.1.2.1.1.3.0'
    )

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send SNMP GET request
#     with SNMPv3, user 'test-user', no authentication, no privacy
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for IP-MIB::ipAdEntAddr.127.0.0.1 MIB object
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.UsmUserData('test-user'),
        cmdgen.UdpTransportTarget(('localhost', 161)),
        (('IP-MIB', 'ipAdEntAddr'), '127.0.0.1')
    )

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send SNMP GET request
#     with SNMPv3, user 'test-user', no authentication, no privacy
#     over IPv4/UDP
#     to an Agent at localhost:161
#     for IP-MIB::ipAdEntAddr.127.0.0.1 MIB object
#     perform response OIDs and values resolution at MIB

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.UsmUserData('test-user'),
        cmdgen.UdpTransportTarget(('localhost', 161)),
        (('IP-MIB', 'ipAdEntAddr'), '127.0.0.1'),
        lookupNames=True, lookupValues=True
    )

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            (modName, symName), indices = name
            indices = '.'.join([x.prettyPrint() for x in indices ])
            print('%s::%s.%s = %s' % (modName, symName, indices, val.prettyPrint()))


# Send SNMP GET request
#     with SNMPv3, user 'test-user', SHA auth, AES128 privacy
#     over Local Domain Sockets
#     to an Agent at /tmp/snmp-agent
#     for TCP-MIB::tcpConnLocalAddress."0.0.0.0".22."0.0.0.0".0 MIB object
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1',
                           authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                           privProtocol=cmdgen.usmAesCfb128Protocol ),
        cmdgen.UnixTransportTarget('/tmp/snmp-agent'),
        (('TCP-MIB', 'tcpConnLocalAddress'), '0.0.0.0', 22, '0.0.0.0', 0)
    )

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

