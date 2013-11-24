import cherrypy
import bitcoinrpc
from rpc_connections import rpc_connections
class SendCoins(object):
    exposed = True
    def POST(self, id=None, to_address=None, amount=None):
        if None in (id, to_address, amount):
            return make_error('Invalid parameters')
        if self._send_coins(rpc_connections[id], to_address, amount):
            return json.dumps({'result': 'Success'})
            
    def _send_coins(self, rpc, to_address, amount):
        return rpc.sendtoaddress(to_address, amount)
