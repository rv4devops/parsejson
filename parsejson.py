#!/usr/bin/env python

import json
import argparse
from collections import defaultdict

import dsfail

# call handler.main() for each JSON array element in given file path
def process(db, handler, path):
	fh = open(path)
	jsobj = json.load(fh)

	handler.init(jsobj)
	for el in jsobj:
		if "prb_id" not in el: continue
		if "result" not in el: continue

		pid = el['prb_id']
		res = el["result"]
		out = handler.each(pid, el, res)
		if out:
			db[pid] += "," + out

def main():
	prs = argparse.ArgumentParser(description='Parse the Atlas results')
	prs.add_argument('--dsfail', help='path to dnssec-failed.org results')
	args = prs.parse_args()

	# print file header
	print "@relation 'parsejson'"
	print "@attribute probe_id numeric"

	# process the input files
	db = defaultdict(str)
	if args.dsfail: process(db, dsfail, args.dsfail)

	# print the results
	for pid,out in db.iteritems():
		print "%d%s" % (pid, out)

if __name__ == "__main__": main()