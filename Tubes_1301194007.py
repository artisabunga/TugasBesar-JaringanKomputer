#nama: Artisa bunga Syahputri
#NIM: 1301194007
#kelas: IF-43-03

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Link, TCLink
from mininet.node import CPULimitedHost
from mininet.node import Node
import os

class NetworkTopo(Topo) : 
	def __init__(self, **opts):
		Topo.__init__(self,**opts)

		#tambahin host 
		h1 = self.addHost("h1" )
		h2 = self.addHost("h2")
		#tambahkan router 
		r1 = self.addHost("r1")
		r2 = self.addHost("r2")
		r3 = self.addHost("r3")
		r4 = self.addHost("r4")
		#buat tipe bandwitch 
		bw1k ={"bw": 1}
		bw500= {"bw": 0.5}		
		#sambungkan
		buff = 100

		self.addLink(h1,r1, intfName1 = 'h1-eth0', intfName2 = 'r1-eth0', cls = TCLink, **bw1k	, max_queue_size=buff,use_htb=True)
		self.addLink(h1,r2, intfName1 = 'h1-eth1', intfName2 = 'r2-eth0', cls = TCLink, **bw1k	, max_queue_size=buff,use_htb=True)
		self.addLink(r1,r3, intfName1 = 'r1-eth1', intfName2 = 'r3-eth0', cls = TCLink, **bw500	, max_queue_size=buff,use_htb=True)
		self.addLink(r2,r4, intfName1 = 'r2-eth1', intfName2 = 'r4-eth0', cls = TCLink, **bw500	, max_queue_size=buff,use_htb=True)
		self.addLink(r4,h2, intfName1 = 'r4-eth1', intfName2 = 'h2-eth1', cls = TCLink, **bw1k	, max_queue_size=buff,use_htb=True)
		self.addLink(r3,h2, intfName1 = 'r3-eth1', intfName2 = 'h2-eth0', cls = TCLink, **bw1k	, max_queue_size=buff,use_htb=True)
		self.addLink(r1,r4, intfName1 = 'r1-eth2', intfName2 = 'r4-eth2', cls = TCLink, **bw1k	, max_queue_size=buff,use_htb=True)
		self.addLink(r2,r3, intfName1 = 'r2-eth2', intfName2 = 'r3-eth2', cls = TCLink, **bw1k	, max_queue_size=buff,use_htb=True)
	

def tubesBunga():
	os.system("mn -c")

	#mulai Network 

	net = Mininet(topo = NetworkTopo(), link=TCLink, host = CPULimitedHost)
	net.start()

	#simpan node topologi pada variabel 
	h1,h2 = net.get("h1", "h2")
	r1,r2,r3,r4 = net.get("r1", "r2", "r3", "r4")
	r1.cmd("sysctl net.ipv4.ip_forward=1") 
	r2.cmd("sysctl net.ipv4.ip_forward=1")
	r3.cmd("sysctl net.ipv4.ip_forward=1")
	r4.cmd("sysctl net.ipv4.ip_forward=1")

	h1.cmd("ifconfig h1-eth0 192.168.0.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.1.1 netmask 255.255.255.0")

	h1.cmd("ip rule add from 192.168.0.1 table 1")
	h1.cmd("ip rule add from 192.168.1.1 table 2")
	h1.cmd("ip route add 192.168.0.0 netmask 255.255.255.0 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.0.2 dev h1-eth0 ")
	h1.cmd("ip route add 192.168.1.0 netmask 255.255.255.0 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.1.2 dev h1-eth1")
	h1.cmd("ip route add default scope global nexthop via 192.168.0.2 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 192.168.1.2 dev h1-eth1")

	h2.cmd("ifconfig h2-eth0 192.168.4.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.5.1 netmask 255.255.255.0")
	#routing

	h2.cmd("ip rule add from 192.168.4.2 table 1")
	h2.cmd("ip rule add from 192.168.5.1 table 2")
	h2.cmd("ip route add 192.168.4.0 netmask 255.255.255.0 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 192.168.4.1 dev h2-eth0 ")
	h2.cmd("ip route add 192.168.5.0 netmask 255.255.255.0 dev h2-eth1 link table 2")
	h2.cmd("ip route add default via 192.168.5.2 dev h2-eth1 ")
	h2.cmd("ip route add default scope global nexthop via 192.168.4.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 192.168.5.2 dev h2-eth1")
	
	r1.cmd("ifconfig r1-eth0 192.168.0.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.2.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.6.1 netmask 255.255.255.0")
	
	r1.cmd("route add -net 192.168.1.0/24 gw 192.168.0.1")
	r1.cmd("route add -net 192.168.1.0/24 gw 192.168.6.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.6.2")
	r1.cmd("route add -net 192.168.7.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.6.2")

	r2.cmd("ifconfig r2-eth0 192.168.1.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.3.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.7.2 netmask 255.255.255.0")
	
	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.1.1")
	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.7.1")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.7.1")
	r2.cmd("route add -net 192.168.6.0/24 gw 192.168.3.2")
	r2.cmd("route add -net 192.168.5.0/24 gw 192.168.3.2")
	r2.cmd("route add -net 192.168.4.0/24 gw 192.168.7.1")

	r3.cmd("ifconfig r3-eth0 192.168.2.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.4.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.7.1 netmask 255.255.255.0")
	
	
	r3.cmd("route add -net 192.168.0.0/24 gw 192.168.2.1")
	r3.cmd("route add -net 192.168.1.0/24 gw 192.168.7.2")
	r3.cmd("route add -net 192.168.3.0/24 gw 192.168.7.2")
	r3.cmd("route add -net 192.168.5.0/24 gw 192.168.4.2")
	r3.cmd("route add -net 192.168.6.0/24 gw 192.168.2.1")
	
	r4.cmd("ifconfig r4-eth0 192.168.3.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.5.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.6.2 netmask 255.255.255.0")
	

	r4.cmd("route add -net 192.168.0.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.3.1")
	r4.cmd("route add -net 192.168.7.0/24 gw 192.168.3.1")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.4.0/24 gw 192.168.5.1")
	
	h2.cmdPrint("iperf -s &")
	h1.cmdPrint("iperf -t 60 -c 192.168.4.2 &")


	
	#start mininet CLI

	CLI(net)
	#stop network 
	net.stop()


if "__main__"== __name__ :
    setLogLevel("info")
    tubesBunga()
