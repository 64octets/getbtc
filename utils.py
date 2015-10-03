import ecdsa
import ecdsa.der
import ecdsa.util
from hashlib import sha256
from hashlib import new
from requests import get

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = sha256(sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1' * leadingZeros + base58encode(base256decode(result))

def base58CheckDecode(s):
    leadingOnes = countLeadingChars(s, '1')
    s = base256encode(base58decode(s))
    result = '\0' * leadingOnes + s[:-4]
    chk = s[-4:]
    checksum = sha256(sha256(result).digest()).digest()[0:4]
    assert(chk == checksum)
    version = result[0]
    return result[1:]

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

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

def privateKeyToWif(key_hex):    
    return base58CheckEncode(0x80, key_hex.decode('hex'))

def privateKeyToPublicKey(s):
    sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return ('\04' + sk.verifying_key.to_string()).encode('hex')

def wifToPrivateKey(s):
    b = base58CheckDecode(s)
    return b.encode('hex')

def pubKeyToAddr(s):
    ripemd160 = new('ripemd160')
    ripemd160.update(sha256(s.decode('hex')).digest())
    return base58CheckEncode(0, ripemd160.digest())

class getInfo(object):
	def __init__(self, addr):
		self.addr = addr
		self.data = get('https://blockchain.info/address/%s?format=json' % self.addr).json()
	def display(self):
		for i in self.data:
			if not i == 'address':
				print str(i) + " = " + str(self.data[i])
	def balance(self):
		return float(self.data[u'final_balance'])
