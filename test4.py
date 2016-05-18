from __future__ import print_function
import time
import sys
print('start')
sys.stdout.write("Download progress: %d%%" % (0) )
for progress in range(10):
    time.sleep(1)    
    sys.stdout.write("\b\b%d%%" % (progress) )
    sys.stdout.flush()
