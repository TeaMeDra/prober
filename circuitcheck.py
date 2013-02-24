from build_graph import *
from collapse_graph import *
from testutils import *

# Arduino interconnectivity
import serial

f = open('sample.upv')
obj = json.load(f)
f.close()

nodes = build_graph(obj)
# print_graph(nodes)

test_pairs = get_test_pairs(nodes)

print "Begin debugging? [y/n]"
a = raw_input()
if a.lower().strip() != 'y' :
    exit()
    

# initialize Arduino connection
try:
    ser = serial.Serial('/dev/tty.usbserial', 9600)
except:
    print 'USB connection failed!'
    exit()
line = 0

while line < len(test_pairs):
    print_test_pair(nodes, test_pairs, line)
    a = ser.readline()
    a = float(a.strip())
    line += 1
    