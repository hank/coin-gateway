import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))
import cherrypy
import json
import bitcoinrpc
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

coin_auth = {"litecoind": {'type': 'local',
                           'file': '/home/hank/.litecoin/litecoin.conf'},
             "bitcoind" : {'type': 'local'},
             #"bitcoind" : 
             #    {'type': 'remote',
             #     'user': 'bitcoinrpc', 
             #     'pw'  : 'somepass',
             #     'host': 'localhost',
             #     'port': '8332',
             #    },
            }
rpc_connections = {}

def make_error(msg):
    cherrypy.response.status = 500
    return json.dumps({"error": msg})

class Root(object):
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('/balance')

    @cherrypy.expose
    def balance(self):
        tmpl = lookup.get_template("balance.html")
        out = tmpl.render()
        return out

    @cherrypy.expose
    def info(self):
        tmpl = lookup.get_template("info.html")
        out = tmpl.render()
        return out

    @cherrypy.expose
    def send(self):
        tmpl = lookup.get_template("send.html")
        out = tmpl.render()
        return out
        
class API(object):
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
            else:
                return make_error('API call not implemented')
        else:
            return make_error('RPC ID not found')


    def _get_balance(self, rpc):
        try:
            return json.dumps({'balance': rpc.getbalance()})
        except Exception as e:
            return make_error('Error getting balance: {}'.format(e))

    def _get_info(self, rpc):
        try:
            info = rpc.getinfo()
            return json.dumps({'info': info.get_dict()})
        except Exception as e:
            return make_error('Error getting balance: {}'.format(e))


class UnlockWallet(object):
    exposed = True
    def POST(self, id=None, passphrase=None, timeout=600):
        if None in (id, passphrase):
            return make_error('Invalid parameters')
        if self._unlock_wallet(rpc_connections[id], passphrase, timeout):
            return json.dumps({'result': 'Success'})
            
    def _unlock_wallet(self, rpc, passphrase, timeout):
        try:
            # Don't throw, just return False if we fail
            return rpc.walletpassphrase(passphrase, timeout, True)
        except bitcoinrpc.exceptions.WalletWrongEncState:
            # We don't have to unlock.
            return True

class SendCoins(object):
    exposed = True
    def POST(self, id=None, to_address=None, amount=None):
        if None in (id, to_address, amount):
            return make_error('Invalid parameters')
        if self._send_coins(rpc_connections[id], to_address, amount):
            return json.dumps({'result': 'Success'})
            
    def _send_coins(self, rpc, to_address, amount):
        return rpc.sendtoaddress(to_address, amount)

if __name__ == "__main__":
    root = Root()
    root.api = API()
    root.api.unlock = UnlockWallet()
    root.api.send = SendCoins()

    for coin, vals in coin_auth.items():
        try:
            if vals['type'] == "local":
                if 'file' in vals:
                    rpc_connection = bitcoinrpc.connect_to_local(
                        filename=vals['file'])
                else:
                    rpc_connection = bitcoinrpc.connect_to_local()
            else:
                rpc_connection = bitcoinrpc.connect_to_remote(
                    vals['user'], vals['pw'], vals['host'], vals['port'])
        except KeyError as e:
            print 'Failed to parse coin_auth for {}'.format(coin)
        rpc_connections[coin] = rpc_connection
    cherrypy.config.update('app.conf')
    cherrypy.tree.mount(root, '/', config="app.conf")
    cherrypy.engine.start()
    cherrypy.engine.block()
