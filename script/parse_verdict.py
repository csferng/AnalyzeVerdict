#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import re
import sys

RE_HEADER = re.compile(ur"^.*?【(.*?)】,(.*?)$")
HEADER_END = u"【裁判全文】,"
PROLOGUE_END = u"    主  文"

def main():
    for filename in sys.argv[1:]:
        header = {}
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
                header[field] = value

        for k in sorted(header):
            print '\t'.join([filename, k, header[k]]).encode('utf-8')

if __name__ == "__main__":
    main()
