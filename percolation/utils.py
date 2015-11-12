import time
TT=time.time()
# check
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
import builtins as B
