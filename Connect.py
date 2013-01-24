"""@package Connect
Connection wrapper for the ib.opt.ibConnection
"""

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep
from tools import daemonize
from threading import Event
import sys

def needConnection(func):
    """Connection check
    Maybe in the future implement a pool and add func
    to the pool instead of waiting for the connection
    """
    def wrapper(self, *args, **kwargs):
        self._connected.wait()
        return func(self, *args, **kwargs)
    return wrapper

class Connect():
    """Main connection class"""

    def __init__(self, host="127.0.0.1", port=4001, verbose=False):
        """ Ctor
        Default port:
        - Gateway: 4001
        - TWS: 7496
        """
        self.host = host
        self.port = port
        self.verbose = verbose

        self._errHandlers = []
        self._next_valid_id = 1
        self._con = ibConnection(self.host, self.port)

        self._reconnect = Event()
        self._connected = Event()

        self.initRegister()
        self.connect()
        self.stayConnected()

    def setNextValidId(self, msg):
        """nextValidId handler"""
        if self.verbose:
            print >> sys.stderr, msg
        self._next_valid_id = msg.orderId

    def initRegister(self):
        """Init the default handlers"""
        self._con.registerAll(self.watcher)
        self._con.unregister(self.watcher, message.Error,
                             message.ConnectionClosed,
                             message.NextValidId)

        self._con.register(self.setNextValidId, message.NextValidId)
        self._con.register(self.errorHandler, message.Error)
        self._con.register(self.disconnected, message.ConnectionClosed)

    @daemonize
    def stayConnected(self):
        """Daemon thread which try to reconnect upon connection loss"""
        while True:
            """Just in case, let unblock every 30 seconds"""
            self._reconnect.wait(30)
            self._reconnect.clear()
            self.connect()

    def connect(self):
        """Connect method which make sure we are always connected"""
        if self.isConnected():
            return self._con

        try:
            """If the connection fail, keep trying"""
            while not self.isConnected():
                print >> sys.stderr, "Trying to connect..."
                self._con.connect()
                sleep(1)
        except KeyboardInterrupt:
            """In case of CTRL-C, simply exit"""
            sys.exit(1)

        """Flag the connected Event"""
        self._connected.set()


    def register(self, func, *args):
        """Register a message to a func handler"""

        """First unregister the messages from the global watcher"""
        for a in args:
            if isinstance(a, message.Error):
                self._errHandlers.append(func)
            else:
                self._con.unregister(self.watcher, a)

        self._con.register(func, *args)

    def unregister(self, func, *args):
        """Unregister a message from the func handler"""
        raise Exception("Method unregiter not implemented")

        self._con.unregister(func, *args)

        for a in args:
            if isinstance(a, message.Error):
                self._con.register(self.errorHandler, a)
            else:
                self._con.register(self.watcher, a)

    def isConnected(self):
        """Check if the connection is active"""
        try:
            return self._con.isConnected()
        except AttributeError:
            return False

    def disconnected(self, msg):
        """Disconnection handler, called on connection loss"""
        if self.verbose:
            print "diconnection detected", type(msg), msg
        self._reconnect.set()
        self._connected.clear()

    def errorHandler(self, msg):
        """Error handler"""

        """Call the registered custom error handlers if any"""
        for f in self._errHandlers:
            f(msg)

        """Error code 1100 is the connection lost message"""
        if msg.errorCode == 1100:
            self._reconnect.set()
            self._connected.clear()
            if self.verbose:
                print "Connection lost!"
        elif msg.errorCode == 502:
            print "Impoosible to connect to TWS."
        elif msg.errorCode == 503:
            print "Fatal error: Outdated TWS, please upgrade it."
        elif len(self._errHandlers) == 0:
            """If the error is not a "System" one and no handler
            have been set, then display the error
            """
            print "Unhandled Error: [{0}] - {1}".format(msg.errorCode,
                                                        msg.errorMsg)

    @needConnection
    def reqMktData(self, c):
        """reqMktData wrapper, request the given Contract data.

        @param c ib.ext.Contract.Contract Contract to request

        Send the request to server with the next available Id and
        associate the id to the contract.
        Increment the next available Id
        """

        def newContract(contract):
            """Send the request for the given contract.
            @param contract ib.ext.Contract.Contract requested contract
            """
            if not isinstance(contract, Contract):
                raise Exception("reqMktDta expect ib.ext.Contract.Contract.")
            contract.m_conId = self._next_valid_id
            self._con.reqMktData(contract.m_conId, contract, '', False)
            self._next_valid_id += 1

        if isinstance(c, list):
            for e in c:
                newContract(e)
        elif isinstance(c, dict):
            for e in c.values():
                newContract(e)
        else:
            newContract(c)


    @needConnection
    def reqAccountUpdates(self, reg=True):
        """reqAccountUpdates wrapper
        @param reg Boolean Flag to register/unregister
        """
        self._con.reqAccountUpdates(reg, '')

    @needConnection
    def placeOrder(self):
        """placeOrder wrapper"""

        for symbol, o in self._orders.items():
            self._con.placeOrder(o[0], self._contracts[symbol][1], o[1])

    def addOrder(self, symbol, lmtPrice=0, minQty=100, action="BUY",
                 orderType="LMT", tif="DAY", outsideRTH=False,
                 totalQuantity=False):
        """Generate and store an order for the given symbol"""

        validAction = ["BUY", "SELL", "SSHORT"]
        if action not in validAction:
            raise Exception("{0} is not a valid order action. " +
                            "Valid actions are: {1}.".
                            format(action, ", ".join(validAction)))

        validType = ["LMT", "MKT", "MKTCLS", "LMTCLS",
                     "PEGMKT", "SCALE", "STP", "STPLMT",
                     "TRAIL", "REL", "VWAP", "TRAILLIMIT"]
        if orderType not in validType:
            raise Exception("{0} is not a valid order type. " +
                            "Valid types are: {1}.".
                            format(orderType, ", ".join(validType)))

        validTIF = ["DAY", "GTC", "IOC", "GTD"]
        if tif not in validTIF:
            raise Exception("{0} is not a valid TIF." +
                            "Valid TIFs are: {1}.".
                            format(tif, ", ".join(validTIF)))

        o = Order()
        o.m_minQty = minQty
        o.m_totalQuantity = totalQuantity if totalQuantity else minQty
        o.m_lmtPrice = lmtPrice
        o.m_action = action
        o.m_tif = tif
        o.m_orderType = orderType
        o.m_outsideRth = outsideRTH

        self._orders[symbol] = self._next_valid_id, o

        self._next_valid_id += 1
        return self._next_valid_id - 1

    def addSymbol(self, symbol, secType="STK", exchange="SMART"):
        """Create and store a contact from the given symbol"""
        c = Contract()
        c.m_symbol = symbol
        c.m_secType = secType
        c.m_exchange = exchange
        c.m_currency = self.currency
        self._contracts[symbol] = self._next_valid_id, c
        self._next_valid_id += 1
        return self._next_valid_id - 1

    def watcher(self, msg):
        """Global handler"""
        if self.verbose:
            print >> sys.stderr, type(msg), msg
