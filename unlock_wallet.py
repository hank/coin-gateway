import cherrypy
import bitcoinrpc
from rpc_connections import rpc_connections
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
