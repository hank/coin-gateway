import cherrypy
import json
from rpc_connections import rpc_connections
import util
from unlock_wallet import UnlockWallet
from send_coins import SendCoins
class API(object):
    unlock = UnlockWallet()
    send   = SendCoins()
    exposed = True
    def GET(self, id=None, action=None):
        if id == None:
            return json.dumps(rpc_connections.keys())
        elif id in rpc_connections:
            # We have a connection
            if action in (None, 'balance',):
                return self._get_balance(rpc_connections[id])
            elif action == 'info':
                return self._get_info(rpc_connections[id])
            elif action == 'transactions':
                return self._get_transactions(rpc_connections[id])
            else:
                return util.make_error('API call not implemented')
        else:
            return util.make_error('RPC ID not found')


    def _get_balance(self, rpc):
        try:
            return json.dumps({'balance': rpc.getbalance()})
        except Exception as e:
            return util.make_error('Error getting balance: {}'.format(e))

    def _get_info(self, rpc):
        try:
            info = rpc.getinfo()
            return json.dumps({'info': info.get_dict()})
        except Exception as e:
            return util.make_error('Error getting info: {}'.format(e))

    def _get_transactions(self, rpc):
        try:
            transactions = [t.get_dict() for t in rpc.listtransactions()]
            return json.dumps({'transactions': transactions})
        except Exception as e:
            return util.make_error('Error getting trnasactions: {}'.format(e))
