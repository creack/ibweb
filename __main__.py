#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""@package Main
Main application file
"""

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.ext.TickType import TickType
from ib.opt import ibConnection, message
from Strategy import Strategy
from Connect import Connect

from threading import Lock, Event
import sys

from time import sleep
import datetime
import pymongo

db = pymongo.MongoClient().ib

class AppIB():
    """IB API Implementation"""

    def __init__(self):
        """Ctor"""
        self.symbols = {}
        self.ticks = {}
        self.event = Event()

        self.con = Connect("172.20.0.11", port = 7496, verbose = True)

        handlers = {
            self.errorHandler: message.Error,
            self.tickPriceHandler: message.TickPrice,
            self.tickSizeHandler: message.TickSize,
            self.tickGenericHandler: message.TickGeneric,
            self.tickStringHandler: message.TickString,
            self.portfolioHandler: message.UpdatePortfolio,
            self.accountValueHandler: message.UpdateAccountValue
            }

        for func, msg in handlers.iteritems():
            self.con.register(func, msg)

    def run(self):
        """Run the main loop"""

        self.symbols["QQQ"] = self.createContract("QQQ")
        self.symbols["MNST"] = self.createContract("MNST")
        self.symbols["MSFT"] = self.createContract("MSFT")
        self.con.reqMktData(self.symbols)

        #    con.addOrder("MNST", minQty = 100, orderType="MKT", outsideRTH = True)
        #    con.placeOrder()

        try:
            while True:
                self.event.wait(30)
                self.event.clear()
                if 0:
                    continue
                for key, id in self.symbols.items():
                    try:
                        print key, ":", self.ticks[id.m_conId]
                    except KeyError:
                        print key, ": No data"
                print
        except KeyboardInterrupt:
            sys.exit(1)

    def createContract(self, symbol, secType="STK",
                       exchange="SMART", currency="USD"):
        """Create and store a contact from the given symbol"""
        c = Contract()
        c.m_symbol = symbol
        c.m_secType = secType
        c.m_exchange = exchange
        c.m_currency = currency
        return c

    def getSymbolFromId(self, id):
        """Return the string symbol for the given id.
        @param id Integer Id of the wanted symbol.
        @return String Symbol
        """
        try:
            return [v.m_symbol for v in self.symbols.values() if v.m_conId == id][0]
        except IndexError:
            return False

    def tickGenericHandler(self, msg):
        print "GENERIC--- [{2}] {0}: {1}.".format(
            TickType.getField(msg.tickType), msg.value,
            self.getSymbolFromId(msg.tickerId))

    def tickStringHandler(self, msg):
        print "STRING--- [{2}] {0}: {1}.".format(
            TickType.getField(msg.tickType), msg.value,
            self.getSymbolFromId(msg.tickerId))

    def tickPriceHandler(self, msg):
        """Handle TickPrice messages from IB.
        Remove the globals and implement a Producer/Consumer
        @param msg ib.opt.message.TickPrice Message sent by IB
        """
        self.ticks[msg.tickerId] = msg

        symb = self.getSymbolFromId(msg.tickerId)
        if symb:
            db.tickers.update({"symbol": symb},
                              {"$set": {TickType.getField(msg.field): msg.price}},
                              upsert = True)
        self.event.set()


    def portfolioHandler(self, msg):
        """Handle UpdatePortfolio messages from IB.
        @param msg ib.opt.message.UpdatePortfolio
        """
        print "----", type(msg), msg

    def accountValueHandler(self, msg):
        """Handle UpdateAccountValue messages from IB.
        Store accout data in db
        @param msg ib.opt.message.UpdateAccountValue Message sent by IB
        """
        db.account.update({"account": msg.accountName,
                           msg.key: {"$exists": True}},
                          {"$set": {msg.key: msg.value,
                                    "currency": msg.currency}},
                          upsert = True)
        print "account: {0}: {1} [{2}] ({3})".format(
            msg.key, msg.value, msg.currency, msg.accountName)

    def tickSizeHandler(self, msg):
        """Handle TickSize messages from IB.
        Store tick data in db
        @param msg ib.opt.message.TickSize Message sent by IB
        """
        symb = self.getSymbolFromId(msg.tickerId)
        if symb:
            #print "[{1}] {0}: {2}".format(symb, fieldType[msg.field], msg.size)
            db.tickers.update({"symbol": symb},
                              {"$set": {TickType.getField(msg.field): msg.size}},
                              upsert = True)

    def errorHandler(self, msg):
        """Error handler.
        @param msg ib.opt.message.Error Message sent by IB
        """
        print "ERROR:", msg

if __name__ == "__main__":

    appIb = AppIB()
    appIb.run()

    c = Strategy()

    tab = []

    def avg(l):
        total = 0
        for p in l:
            total += p
        return total / len(l)

    tmp = 0
    while 1:
        if lastprice and tmp != lastprice:
            print "lock"
            mlock.acquire()

#            tmp = lastprice
#            tab.append(lastprice)
#            c.addPrice(lastprice)
#            m = c.getMacd()
#            print lastprice, " ", m, " ", c.getScore()

