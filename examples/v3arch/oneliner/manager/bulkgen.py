# Various GETBULK Command Generator uses
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

# Send a series of SNMP GETBULK requests
#     with SNMPv2c, community 'public'
#     over IPv4/UDP
#     to an Agent at localhost:161
#     with values non-repeaters = 0, max-repetitions = 25
#     for two OIDs in string form
#     stop when response OIDs leave the scopes of initial OIDs
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(('localhost', 161)),
        0, 25,
        '1.3.6.1.2.1.2.2.1.2',
        '1.3.6.1.2.1.2.2.1.3',
    )

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


# Send a series of SNMP GETBULK requests
#     with SNMPv3 with user 'test-user', MD5 auth and DES privacy protocols
#     over IPv6/UDP
#     to an Agent at [::1]:161
#     with values non-repeaters = 1, max-repetitions = 25
#     for IP-MIB::ipAdEntAddr and all columns of the IF-MIB::ifEntry table
#     stop when response OIDs leave the scopes of the table OR maxRows == 20
#     perform response OIDs and values resolution at MIB
# make sure IF-MIB.py and IP-MIB.py are in search path

errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
        cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
        cmdgen.Udp6TransportTarget(('::1', 161)),
        1, 25,
        (('IP-MIB', 'ipAdEntAddr'),),
        (('IF-MIB', 'ifEntry'),),
        lookupNames=True, lookupValues=True,
        maxRows=20
    )

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                (modName, symName), indices = name
                indices = '.'.join([x.prettyPrint() for x in indices ])
                print('%s::%s.%s = %s' % (modName, symName, indices, val.prettyPrint()))


# Send a series of SNMP GETBULK requests
#     with SNMPv3, user 'test-user', no auth, no privacy
#     over Local Domain Sockets
#     to an Agent at localhost:161
#     for all OIDs past 1.3.6.1.2.1.1
#     run till end-of-mib condition is reported by Agent OR maxRows == 20
#     ignoring non-increasing OIDs whenever reported by Agent
# make sure IF-MIB.py is search path

errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
        cmdgen.UsmUserData('test-user'),
        cmdgen.UdpTransportTarget(('localhost', 161)),
        0, 50,
        '1.3.6.1.2.1.1',
        lexicographicMode=True, maxRows=100,
        ignoreNonIncreasingOid=True
    )

if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
            )
        )
    else:
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('%s = %s' % (name, val.prettyPrint()))

