import utils
import argparse
from random import randrange
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="number of addresses to generate.")
args = parser.parse_args()

def main():
	if args.n:
		fp = open("generatedAddresses", 'a+')
		for i in xrange(args.n):
			private_key = ''.join(['%x' % randrange(16) for x in range(0, 64)])
			wif = utils.base58CheckEncode(0x80, private_key.decode('hex'))
			address = utils.pubKeyToAddr(utils.privateKeyToPublicKey(utils.wifToPrivateKey(wif)))
			fp.write("PK: " + private_key + '\n' + "WIF: " +wif + '\n' + "ADDR: " +address+'\n')
		fp.close()
		print "File successfully closed."

	print "Exiting."
	exit()

if __name__ == "__main__":
	main()
