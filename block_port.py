 
from pox.core import core
from collections import namedtuple
import os
 
# A set of ports to block

list_ports = "%s/pox/pox/misc/port.csv" % os.environ['HOME']  

#read policy file and save it as a dictionary

fp = open(list_ports)
line = fp.readline()
while line:
    list = (line)
    #print ports
    line = fp.readline()
fp.close()
print list

#arquivo em linha 

drop_ports = set()

def block_ports (event):
  

# Handles packet events and kills the ones with a blocked port number
 
  tcpp = event.parsed.find('tcp')
  if not tcpp: return # Not TCP
  if tcpp.srcport in drop_ports or tcpp.dstport in drop_ports:
    core.getLogger("blocker").debug("Blocked TCP %s <-> %s",
                                    tcpp.srcport, tcpp.dstport)
    event.halt = True
 
def unblock (*ports):
  drop_ports.difference_update(ports)
 
def block (*ports):
  drop_ports.update(ports)
 
def launch (ports = list):
 
  
  # Add ports from commandline to list of ports to block
  drop_ports.update(int(x) for x in ports.replace(",", " ").split())
  
 
  # Listen to packet events
core.openflow.addListenerByName("PacketIn", block_ports)
