import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "percolation" in key:
        print(key)
        del sys.modules[key]

import percolation as P

