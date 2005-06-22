from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen, error

snmpEngine = engine.SnmpEngine()

# v1/2 setup
config.addV1System(snmpEngine, 'test-agent', 'public')

# v3 setup
config.addV3User(snmpEngine, 'test-user', 'authkey1', 'md5', 'privkey1', 'des')

# Transport params
#config.addTargetParams(snmpEngine, 'myParams', 'test-user', 'authPriv')
config.addTargetParams(snmpEngine, 'myParams', 'test-agent', 'noAuthNoPriv', 1)

# Transport addresses
config.addTargetAddr(
    snmpEngine, 'myRouter', config.snmpUDPDomain,
    ('127.0.0.1', 161), 'myParams'
    )

# Setup transport endpoint
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpSocketTransport().openClientMode()
    )

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBinds, cbCtx):
    raise error.ApplicationReturn(
        errorIndication=errorIndication,
        errorStatus=errorStatus,
        errorIndex=errorIndex,
        varBinds=varBinds
        )
    
cmdgen.GetCmdGen().sendReq(
    snmpEngine, 'myRouter', (((1,3,6,1,2,1,1,1,0), None),), cbFun
    )

try:
    snmpEngine.transportDispatcher.runDispatcher()
except error.ApplicationReturn, applicationReturn:
    if applicationReturn['errorIndication']:
        print applicationReturn['errorIndication']
    elif applicationReturn['errorStatus']:
        print repr(applicationReturn['errorStatus'])
    else:
        for oid, val in applicationReturn['varBinds']:
            print '%s = %s' % (oid, val)    
