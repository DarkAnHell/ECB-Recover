#!/usr/bin/env python2.7

#
#		(AES) ECB Recover utility
#		By: DarkAnHell @ 9/2015
#	-----------------------------
#		Use at your own risk
#
#   NOTE: The script pairs files as they come up in the folder.
#		  Always align the pairs [encrypted file] - [plain file] in the same order in both folders

import argparse
import os
import sys

def loadFiles(e,p,pairs,res):
	with open(res.enc+"/"+e,"rb") as e_file:
		with open(res.plain+"/"+p,"rb") as p_file:
			while True:
				be = e_file.read(16)
				bp = p_file.read(16)
				if not be and not bp:
					break
				if not be:
					print "[-] Encrypted file ["+e+"] is smaller than plain text pair ["+p+"]. Aborting"
					sys.Exit(1)
				if not bp:
					print "[-] Plain file ["+p+"] is smaller than encrypted pair ["+e+"]. Aborting"
					sys.Exit(1)

				pairs[be.encode('hex')] = bp

def attack(pairs,f,res):
	matches = 0
	rounds = 0
	with open(res.target+"/"+f,"rb") as a_file:
		if res.dest == None:
			dest = ""
		else:
			dest = res.dest
		with open(dest+"dec_"+f,"wb") as w_file:
			while True:
				b = a_file.read(16)

				if not b:
					break

				bh = b.encode("hex")

				if bh in pairs:
					w_file.write(pairs[bh])
					matches += 1

				else:
					w_file.write(b)

				rounds += 1

	return (float(matches)/float(rounds)) * 100

def main(res):
	print "[i] Loading data"

	### Error checking and data loading
	if os.path.isdir(res.enc) != True:
		print "[-] ["+res.enc+"] is not a directory"
		return

	if os.path.isdir(res.plain) != True:
		print "[-] ["+res.plain+"] is not a directory"
		return

	if os.path.isdir(res.target) != True:
		print "[-] ["+res.target+"] is not a directory"
		return

	enc = os.listdir(res.enc)
	plain = os.listdir(res.plain)
	target = os.listdir(res.target)

	if len(enc) != len(plain):
		print "[-] There aren't the same number of encrypted ["+str(len(enc))+"] and plain files ["+str(len(plain))+"]"
		return

	if len(target) == 0:
		print "[-] No target files found in ["+res.target+"]"
		return

	## END CHECKS

	## Pair data
	pairs = dict()

	for e,p in zip(enc,plain):
		print "\t[+] Reading data from [" + e +"] and pairing with [" + p + "]"
		loadFiles(e,p,pairs,res)

	print "[+] Finished loading data. N of blocks loaded: "+str(len(pairs))

	print "[i] Attacking files..."
	for a in target:
		print "\t[+] Attacking ["+a+"]"
		percenteage = attack(pairs,a,res)
		print "\t\t[+] "+str(percenteage)+"% of file was recovered (saved as 'dec_"+a+"')"

if __name__ == "__main__":

	p = argparse.ArgumentParser(description="Tries to defeat AES ECB encryption using known plain-text / plain-bytes")

	p.add_argument("enc",help="Directory containing the encrypted files.",action="store")

	p.add_argument("plain",help="Directory containing the plain-text files",action="store")

	p.add_argument("target",help="Directory containing the encrypted files to attack",action="store")

	p.add_argument("dest",help="(Optional) Directory that will contain the output files",nargs="?",action="store",const=".")

	res = p.parse_args()
	main(res)
