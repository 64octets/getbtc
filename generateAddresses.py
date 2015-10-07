import utils
import argparse
import threading
from random import randrange
from sys import exit

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="number of addresses to generate.")
args = parser.parse_args()

def main():
	counter = 0
	try:
		if args.n:
			fp = open("ga1", 'a+')
			for i in xrange(args.n):
				print counter
				private_key = ''.join(['%x' % randrange(16) for x in range(0, 64)])
				wif = utils.base58CheckEncode(0x80, private_key.decode('hex'))
				address = utils.pubKeyToAddr(utils.privateKeyToPublicKey(utils.wifToPrivateKey(wif)))
				fp.write("PK: " + private_key + '\n' + "WIF: " +wif + '\n' + "ADDR: " +address+'\n')
				counter = counter + 1
			fp.close()
			print "File successfully closed."
	except KeyboardInterrupt:
		print "[!] User Keyboard Interrupt"
		fp.close()
		print "File successfully closed."

	print "Exiting."
	exit()

if __name__ == "__main__":
	threads = []
	for i in range(4):
	    t = threading.Thread(target=main, args=())
	    threads.append(t)
	    t.start()
