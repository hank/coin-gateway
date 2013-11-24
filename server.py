import cherrypy
import json
import bitcoinrpc
from rpc_connections import rpc_connections
from root import Root

coin_auth = {"litecoind": {'type': 'local',
                           'file': '/home/hank/.litecoin/litecoin.conf'},
             "bitcoind" : {'type': 'local'},
             # "bitcoind" : 
             #     {'type': 'remote',
             #      'user': 'bitcoinrpc', 
             #      'pw'  : 'somepass',
             #      'host': 'localhost',
             #      'port': '8332',
             #     },
            }

if __name__ == "__main__":
    root = Root()
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
