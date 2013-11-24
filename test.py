import bitcoinrpc
conn = bitcoinrpc.connect_to_local()
acc_l = conn.listaccounts()
for i in acc_l:
    print conn.getaddressesbyaccount(i)
print conn.walletpassphrase("", 30)
