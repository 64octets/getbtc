import ecdsa
from sys import exit
from random import randrange
from hashlib import sha256
from hashlib import new
from requests import get 

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
logging = 1

def balance(addr):
	data = get('https://blockchain.info/address/%s?format=json' % addr).json()
	return data[u'final_balance']

def base58CheckDecode(s):
    leadingOnes = countLeadingChars(s, '1')
    s = base256encode(base58decode(s))
    result = '\0' * leadingOnes + s[:-4]
    chk = s[-4:]
    checksum = sha256(sha256(result).digest()).digest()[0:4]
    assert(chk == checksum)
    version = result[0]
    return result[1:]

def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = sha256(sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1' * leadingZeros + base58encode(base256decode(result))

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n /= 58
    return result

def base58decode(s):
    result = 0
    for i in range(0, len(s)):
        result = result * 58 + b58.index(s[i])
    return result
def base256encode(n):
    result = ''
    while n > 0:
        result = chr(n % 256) + result
        n /= 256
    return result

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

def pubKeyToAddr(s):
    ripemd160 = new('ripemd160')
    ripemd160.update(sha256(s.decode('hex')).digest())
    return base58CheckEncode(0, ripemd160.digest())

def privateKeyToPublicKey(s):
    sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return ('\04' + sk.verifying_key.to_string()).encode('hex')

def wifToPrivateKey(s):
    b = base58CheckDecode(s)
    return b.encode('hex')

if logging:
	log_file = open('btc.log', 'a+')

done = False
found = 0
attempts = 0
while not done:
	try:
		private_key = ''.join(['%x' % randrange(16) for x in range(0, 64)])
		wif = base58CheckEncode(0x80, private_key.decode('hex'))
		address = pubKeyToAddr(privateKeyToPublicKey(wifToPrivateKey(wif)))
		try:
			bal = balance(address)
		except:
			bal = 00
			pass
		if logging:
			log_file.write('\n' + "PK: " + private_key + '\n' + "WIF: " +wif + '\n' + "ADDR: " +address + '\n' + "BAL: " + str(bal) + '\n')
		print "PK: " + private_key
		print "WIF: " + wif
		print "ADDR: " + address
		print "BAL: " + str(bal)
		print "A: " + str(attempts)
		print "F: " + str(found)
		print
		if bal > 0:
			print "[$$$$$$$$$$$$$$$]"
			with open('btc.list', 'a+') as btclist:
				btclist.write('\n' + "PK: " + private_key + '\n' + "WIF: " +wif + '\n' + "ADDR: " +address + '\n' + "BAL: " + str(bal) + '\n')
				found = found + 1
		attempts = attempts + 1
	except KeyboardInterrupt:
		print "[!] USER EXITED [!]"
		done = True

exit()
