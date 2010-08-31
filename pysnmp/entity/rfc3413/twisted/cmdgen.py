from twisted.internet import reactor, defer
from pysnmp.entity.rfc3413 import cmdgen

def _cbFun(sendRequestHandle, errorIndication,
           errorStatus, errorIndex, varBinds, cbCtx):
    cbCtx.callback((errorIndication, errorStatus, errorIndex, varBinds))

class GetCommandGenerator(cmdgen.GetCommandGenerator):
    def sendReq(
        self,
        snmpEngine,
        addrName,
        varBinds,
        contextEngineId=None,
        contextName=''
        ):
        df = defer.Deferred()
        cmdgen.GetCommandGenerator.sendReq(
            self,
            snmpEngine,
            addrName,
            varBinds,
            _cbFun,
            df,
            contextEngineId,
            contextName
            )
        return df

class SetCommandGenerator(cmdgen.SetCommandGenerator):
    def sendReq(
        self,
        snmpEngine,
        addrName,
        varBinds,
        contextEngineId=None,
        contextName=''
        ):
        df = defer.Deferred()
        cmdgen.SetCommandGenerator.sendReq(
            self,
            snmpEngine,
            addrName,
            varBinds,
            _cbFun,
            df,
            contextEngineId,
            contextName
            )
        return df

class NextCommandGenerator(cmdgen.NextCommandGenerator):
    def sendReq(
        self,
        snmpEngine,
        addrName,
        varBinds,
        contextEngineId=None,
        contextName=''
        ):
        df = defer.Deferred()
        cmdgen.NextCommandGenerator.sendReq(
            self,
            snmpEngine,
            addrName,
            varBinds,
            _cbFun,
            df,
            contextEngineId,
            contextName
            )
        return df

class BulkCommandGenerator(cmdgen.BulkCommandGenerator):
    def sendReq(
        self,
        snmpEngine,
        addrName,
        nonRepeaters,
        maxRepetitions,
        varBinds,
        contextEngineId=None,
        contextName=''
        ):
        df = defer.Deferred()
        cmdgen.BulkCommandGenerator.sendReq(
            self,
            snmpEngine,
            addrName,
            nonRepeaters,
            maxRepetitions,
            varBinds,
            _cbFun,
            df,
            contextEngineId=None,
            contextName=''
            )
        return df

