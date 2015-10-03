import utils

print

q = int(raw_input("1:\tPrivate Key\n2:\tWallet Import Format Private Key\n3:\tPublic Key\n\n[ ] Enter selection: "))

print 

if q == 1:
    priv_key = raw_input("[ ] Enter Private Key: ")
    address = utils.pubKeyToAddr(utils.privateKeyToPublicKey(priv_key))
    print
    print "Address: " + address
    print "Private Key: " + priv_key
    print "Wallet Import Format Private Key: " + utils.privateKeyToWif(priv_key)
    print "Public Key: " + utils.privateKeyToPublicKey(priv_key)
    info = utils.getInfo(address)
    if info.balance() > 0:
        info.display()

elif q == 2:
    wif_priv_key = raw_input("[ ] Enter Wallet Import Format Private Key: ")
    address = utils.pubKeyToAddr(utils.privateKeyToPublicKey(utils.wifToPrivateKey(wif_priv_key)))
    print
    print "Address: " + address
    print "Private key: " + utils.wifToPrivateKey(wif_priv_key)
    print "Wallet Import Format Private Key: " + wif_priv_key
    print "Public Key: " + utils.privateKeyToPublicKey(utils.wifToPrivateKey(wif_priv_key))
    info = utils.getInfo(address)
    if info.balance() > 0:
        info.display()

elif q == 3:	
    pub_key = raw_input("[ ] Enter Public Key: ")
