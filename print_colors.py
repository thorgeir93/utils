#!/usr/bin/env python
import sys
terse = "-t" in sys.argv[1:] or "--terse" in sys.argv[1:]
write = sys.stdout.write

for i in range(2 if terse else 10):
    i = 38
    for j in range(38, 39):
        j = 5
        for k in range(0, 50):
            if terse:
                write("\33[%d;%d;%dm%d;%d;%d\33[m " % (i, j, k, i, j, k))
            else:
                write("%d;%d;%d: \33[%d;%d;%dm Hello, World! \33[m \n" %
                      (i, j, k, i, j, k,))
        write("\n")
