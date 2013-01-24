#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for Contract.
##

# Source file: Contract.java
# Target file: Contract.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded
from ib.lib import Cloneable
from ib.ext.Util import Util

class Contract(Cloneable):
    """ generated source for Contract

    """
    m_conId = 0
    m_symbol = ""
    m_secType = ""
    m_expiry = ""
    m_strike = float()
    m_right = ""
    m_multiplier = ""
    m_exchange = ""
    m_currency = ""
    m_localSymbol = ""
    m_primaryExch = ""
    m_includeExpired = bool()
    m_comboLegsDescrip = ""
    m_comboLegs = None
    m_underComp = None

    @overloaded
    def __init__(self):
        self.m_conId = 0
        self.m_strike = 0
        self.m_includeExpired = False

    def clone(self):
        retval = Cloneable.clone(self)
        retval.m_comboLegs = self.m_comboLegs[:]
        return retval

    @__init__.register(object, int, str, str, str, float, str, str, str, str, str, list, str, bool)
    def __init___0(self, p_conId,
                         p_symbol,
                         p_secType,
                         p_expiry,
                         p_strike,
                         p_right,
                         p_multiplier,
                         p_exchange,
                         p_currency,
                         p_localSymbol,
                         p_comboLegs,
                         p_primaryExch,
                         p_includeExpired):
        self.m_conId = p_conId
        self.m_symbol = p_symbol
        self.m_secType = p_secType
        self.m_expiry = p_expiry
        self.m_strike = p_strike
        self.m_right = p_right
        self.m_multiplier = p_multiplier
        self.m_exchange = p_exchange
        self.m_currency = p_currency
        self.m_includeExpired = p_includeExpired
        self.m_localSymbol = p_localSymbol
        self.m_comboLegs = p_comboLegs
        self.m_primaryExch = p_primaryExch

    def __eq__(self, p_other):
        if self is p_other:
            return True
        if p_other is None or not isinstance(p_other, (Contract)):
            return False
        l_theOther = p_other
        if (self.m_conId != l_theOther.m_conId):
            return False

        if self.m_comboLegs and l_theOther.comboLegsSize and len(self.m_comboLegs) != len(l_theOther.m_comboLegs):
            return False
        elif self.m_comboLegs or self.m_comboLegs:
            return False

        if (Util.StringCompare(self.m_secType, l_theOther.m_secType) != 0):
            return False
        if (Util.StringCompare(self.m_symbol, l_theOther.m_symbol) != 0) or (Util.StringCompare(self.m_exchange, l_theOther.m_exchange) != 0) or (Util.StringCompare(self.m_primaryExch, l_theOther.m_primaryExch) != 0) or (Util.StringCompare(self.m_currency, l_theOther.m_currency) != 0):
            return False
        if not Util.NormalizeString(self.m_secType) == "BOND":
            if (self.m_strike != l_theOther.m_strike):
                return False
            if (Util.StringCompare(self.m_expiry, l_theOther.m_expiry) != 0) or (Util.StringCompare(self.m_right, l_theOther.m_right) != 0) or (Util.StringCompare(self.m_multiplier, l_theOther.m_multiplier) != 0) or (Util.StringCompare(self.m_localSymbol, l_theOther.m_localSymbol) != 0):
                return False
        if self.m_comboLegs and len(self.m_comboLegs) > 0:
            comboLegsSize = len(self.m_comboLegs)
            alreadyMatchedSecondLeg = [bool() for __idx0 in range(comboLegsSize)]
            ## for-while
            ctr1 = 0
            while ctr1 < comboLegsSize:
                l_thisComboLeg = self.m_comboLegs[ctr1]
                ctr2 = 0
                ## for-while
                while ctr2 < comboLegsSize:
                    if alreadyMatchedSecondLeg[ctr2]:
                        continue
                    if l_thisComboLeg == l_theOther.m_comboLegs[ctr2]:
                        alreadyMatchedSecondLeg[ctr2] = True
                        break
                    ctr2 += 1
                if ctr2 >= comboLegsSize:
                    return False
                ctr1 += 1
        if (self.m_underComp != l_theOther.m_underComp):
            if self.m_underComp is None or l_theOther.m_underComp is None:
                return False
            if not self.m_underComp == l_theOther.m_underComp:
                return False
        return True


