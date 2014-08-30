#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import json
import re
import sys

RE_HEADER = re.compile(ur"^.*?【(.*?)】,(.*?)$")
HEADER_END = u"【裁判全文】,"
KEY_ACCUSED = u'被　　　告'
KEY_CONTINUE = u'　　　　　'
PROLOGUE_END = u"    主  文"

def main():
    for filename in sys.argv[1:]:
        data = {}
        with open(filename) as f:
            for line in f:
                line = line.decode('utf-8').strip()
                if line == HEADER_END: break

                m = RE_HEADER.match(line)
                if m is None: continue
                g = m.groups()
                field, value = g[0], g[1]
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                data[field] = value
	
	    state = 0	# 0: none; 1: in accused list
	    accused = []
	    for line in f:
                line = line.decode('utf-8').strip()
	    	if line.startswith(PROLOGUE_END):
		    break
	    	if state == 0:
		    if line.startswith(KEY_ACCUSED):
			accused.append(line[6:])
			state = 1
		elif state == 1:
		    if line.startswith(KEY_CONTINUE):
			accused.append(line[6:])
		    else:
			state = 0
	    data[u'被告'] = accused

        for k in sorted(data):
	    val = json.dumps(data[k], ensure_ascii=False)
            print '\t'.join([filename, k, val]).encode('utf-8')

if __name__ == "__main__":
    main()
