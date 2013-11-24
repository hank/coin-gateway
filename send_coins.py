import cherrypy
import json
import bitcoinrpc
from decimal import Decimal, getcontext
from rpc_connections import rpc_connections
import util
from bitcoinrpc.exceptions import *

class SendCoins(object):
    exposed = True
    def POST(self, rpc=None, address=None, amount=None):
        if None in (rpc, address, amount):
            return util.make_error('Invalid parameters')
        # Parse amount into float
        try:
            amount = Decimal(amount)
            amount = float(amount)
        except Exception as e:
            return util.make_error('Failed to convert amount: {}'.format(e))
        return self._send_coins(rpc_connections[rpc], address, amount)
            
    def _send_coins(self, rpc, address, amount):
        try:
            return rpc.sendtoaddress(address, amount)
        except InvalidAddressOrKey:
            return util.make_error('Invalid address')
        except BitcoinException as e:
            return util.make_error('Validation failed: {}'.format(e))
            
