#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Defines Sender class to handle outbound requests.
#
# Sender instances defer failed attribute lookup to their
# EClientSocket member objects.
#
##
from ib.ext.EClientSocket import EClientSocket


class Sender(object):
    """ Encapsulates an EClientSocket instance, and proxies attribute
        lookup to it.

    """
    client = None

    def connect(self, host, port, clientId, handler, clientType=EClientSocket):
        """ Creates a TWS client socket and connects it.

        @param host name of host for connection; default is localhost
        @param port port number for connection; default is 7496
        @param clientId client identifier to send when connected
        @param handler object to receive reader messages
        @keyparam clientType=EClientSocket callable producing socket client
        @return True if connected, False otherwise
        """
        self.client = client = clientType(handler)
        client.eConnect(host, port, clientId)
        return client.isConnected()

    def disconnect(self):
        """ Disconnects the client.

        @return True if disconnected, False otherwise
        """
        client = self.client
        if client and client.isConnected():
            client.eDisconnect()
            return not client.isConnected()
        return False

    def __getattr__(self, name):
        """ x.__getattr__('name') <==> x.name

        @return named attribute from EClientSocket object
        """
        return getattr(self.client, name)
