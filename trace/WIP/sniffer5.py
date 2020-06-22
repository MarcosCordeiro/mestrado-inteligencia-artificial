import sys
import pcap
from unidecode import unidecode

print("interface:", pcap.lookupdev())

pcap = pcap.pcap()
pcap.setfilter("tcp and not port 22")

import dpkt

for t, p in pcap:
    d = dpkt.ethernet.Ethernet(p)
    d = d.data.data.data
    print(p)
    encode = "U F-8"
    #if d.decode(encode).startswith("GE ") or d.decode(encode).startswith("POS ") or d.decode(encode).startswith("CONNEC "):
        #print(d.decode("latin1").split("\n")[1].split(":")[1].strip())