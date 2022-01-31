#!/usr/bin/python
from pyroute2 import IPRoute
import socket
ip = IPRoute()
for x in ip.get_addr(label='eth0',family=socket.AF_INET):
  ipa =x.get_attr('IFA_ADDRESS')+"/"+str(x['prefixlen'])

print "My IP:", ipa
import subprocess
process = subprocess.Popen(['sudo','nmap','-oX', '/tmp/nmap.xml','-sn',ipa],
stdout=subprocess.PIPE)
process.wait()

import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/nmap.xml')
for node in tree.iter('address'):
  try:
    if node.attrib['addrtype'] == "ipv4":
      ip = node.attrib['addr']
  except:
    pass
  try:
    if node.attrib['vendor'] == "Raspberry Pi Foundation":
      print "Other Raspberry IP:", ip
  except:
    pass