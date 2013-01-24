#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Translated source for ContractDetails.
##

# Source file: ContractDetails.java
# Target file: ContractDetails.py
#
# Original file copyright original author(s).
# This file copyright Troy Melhase, troy@gci.net.
#
# WARNING: all changes to this file will be lost.

from ib.lib.overloading import overloaded
from ib.ext.Contract import Contract

class ContractDetails(object):
    """ generated source for ContractDetails

    """
    m_summary = None
    m_marketName = ""
    m_tradingClass = ""
    m_minTick = float()
    m_priceMagnifier = 0
    m_orderTypes = ""
    m_validExchanges = ""
    m_cusip = ""
    m_ratings = ""
    m_descAppend = ""
    m_bondType = ""
    m_couponType = ""
    m_callable = False
    m_putable = False
    m_coupon = 0
    m_convertible = False
    m_maturity = ""
    m_issueDate = ""
    m_nextOptionDate = ""
    m_nextOptionType = ""
    m_nextOptionPartial = False
    m_notes = ""

    @overloaded
    def __init__(self):
        self.m_summary = Contract()
        self.m_minTick = 0

    @__init__.register(object, Contract, str, str, float, str, str)
    def __init___0(self, p_summary,
                         p_marketName,
                         p_tradingClass,
                         p_minTick,
                         p_orderTypes,
                         p_validExchanges):
        self.m_summary = p_summary
        self.m_marketName = p_marketName
        self.m_tradingClass = p_tradingClass
        self.m_minTick = p_minTick
        self.m_orderTypes = p_orderTypes
        self.m_validExchanges = p_validExchanges


