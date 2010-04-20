"""Abstract I/O dispatcher. Defines standard dispatcher API"""
from pysnmp.carrier import error

class TimerCallable:
    def __init__(self, cbFun, callInterval):
        self.__cbFun = cbFun
        self.__callInterval = callInterval
        self.__nextCall = 0
        
    def __call__(self, timeNow):
        if self.__nextCall <= timeNow:
            self.__cbFun(timeNow)
            self.__nextCall = timeNow + self.__callInterval

    def __cmp__(self, cbFun):
        return cmp(self.__cbFun, cbFun)
    
class AbstractTransportDispatcher:
    def __init__(self):
        self.__transports = {}
        self.__jobs = {}
        self.__recvCbFun = None
        self.__timerCallables = []

    def _cbFun(self, incomingTransport, transportAddress, incomingMessage):
        for name, transport in self.__transports.items():
            if transport is incomingTransport:
                transportDomain = name
                break
        else:
            raise error.CarrierError(
                'Unregistered transport %s' % (incomingTransport,)
                )
        if self.__recvCbFun is None:
            raise error.CarrierError(
                'Receive callback not registered -- loosing incoming event'
                )
        self.__recvCbFun(
            self, transportDomain, transportAddress, incomingMessage
            )

    # Dispatcher API
    
    def registerRecvCbFun(self, recvCbFun):
        if self.__recvCbFun is not None:
            raise error.CarrierError(
                'Receive callback already registered: %s' % self.__recvCbFun
                )
        self.__recvCbFun = recvCbFun

    def unregisterRecvCbFun(self):
        self.__recvCbFun = None

    def registerTimerCbFun(self, timerCbFun, tickInterval=1.0):
        self.__timerCallables.append(TimerCallable(timerCbFun, tickInterval))

    def unregisterTimerCbFun(self, timerCbFun=None):
        if timerCbFun is None:
            self.__timerCallables = []
        else:
            self.__timerCallables.remove(timerCbFun)

    def registerTransport(self, tDomain, transport):
        if self.__transports.has_key(tDomain):
            raise error.CarrierError(
                'Transport %s already registered' % (tDomain,)
                )
        transport.registerCbFun(self._cbFun)
        self.__transports[tDomain] = transport

    def unregisterTransport(self, tDomain):
        if not self.__transports.has_key(tDomain):
            raise error.CarrierError(
                'Transport %s not registered' % (tDomain,)
                )
        self.__transports[tDomain].unregisterCbFun()
        del self.__transports[tDomain]

    def getTransport(self, transportDomain):
        return self.__transports.get(transportDomain)

    def sendMessage(
        self, outgoingMessage, transportDomain, transportAddress
        ):
        transport = self.__transports.get(transportDomain)
        if transport is None:
            raise error.CarrierError(
                'No suitable transport domain for %s' % (transportDomain,)
                )
        transport.sendMessage(outgoingMessage, transportAddress)

    def handleTimerTick(self, timeNow):
        for timerCallable in self.__timerCallables:
            timerCallable(timeNow)

    def jobStarted(self, jobId):
        self.__jobs[jobId] = self.__jobs.get(jobId, 0) + 1

    def jobFinished(self, jobId):
        self.__jobs[jobId] = self.__jobs[jobId] - 1
        if self.__jobs[jobId] == 0:
            del self.__jobs[jobId]

    def jobsArePending(self):
        if self.__jobs:
            return 1
        else:
            return 0

    def runDispatcher(self, timeout=0.0):
        raise error.CarrierError('Method not implemented')
        
    def closeDispatcher(self):
        for tDomain in self.__transports.keys():
            self.__transports[tDomain].closeTransport()
            self.unregisterTransport(tDomain)
        self.unregisterRecvCbFun()
        self.unregisterTimerCbFun()
