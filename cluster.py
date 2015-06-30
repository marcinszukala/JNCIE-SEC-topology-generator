#!/usr/bin/python
from random import randint
from random import shuffle
from netaddr import *

class vsrx_cluster:
  fxp0 = ""
  fxp1 = ""
  fab0 = "ge-0/0/2"
  fab1 = "ge-7/0/2"
  reth0 = {"node_0_interface": "ge-0/0/3", "node_1_interface": "ge-7/0/3", "vlan": "", "network": ""}
  reth1 = {"node_0_interface": "ge-0/0/4", "node_1_interface": "ge-7/0/4", "vlan": "", "network": ""}
  reth2 = {"node_0_interface": "ge-0/0/5", "node_1_interface": "ge-7/0/5", "vlan": "", "network": ""}
  reth3 = {"node_0_interface": "ge-0/0/6", "node_1_interface": "ge-7/0/6", "vlan": "", "network": ""}
  zone_untrust = "reth0"
  zone_trust = ""
  zone_dmz = ""
  
  def __init__(self, name, location):
    self.name = name
    self.location = location
    ifaces = ["reth1", "reth2", "reth3"]
    rand = randint(0,2)
    self.zone_trust += ifaces[rand]
    self.zone_trust += " "
    ifaces.remove(ifaces[rand])
    rand = randint(0,1)
    self.zone_trust += ifaces[rand]
    ifaces.remove(ifaces[rand])
    
    rand = randint(0,0)
    self.zone_dmz += ifaces[rand]
    ifaces.remove(ifaces[rand])
    
  def generate_networks(self):
    self.first_octet = "10"
    self.second_octet = ord(self.location)
    self.third_octet = randint(0,254)
    self.fourth_octet = "0"
    self.netmask = randint(24,28)
    self.octets = "%s.%s.%s.%s/%s" % (self.first_octet, self.second_octet, self.third_octet, self.fourth_octet, self.netmask)
    self.ip = IPNetwork(self.octets)
    self.vlan = self.third_octet
    self.network = self.ip.cidr
    return self.vlan, self.network
    

 
    
cluster_A = vsrx_cluster("vsrx-1","A")
#cluster_B = vsrx_cluster("vsrx-2","B")

(cluster_A.reth0["vlan"], cluster_A.reth0["network"])  = cluster_A.generate_networks()
(cluster_A.reth1["vlan"], cluster_A.reth1["network"]) = cluster_A.generate_networks()
(cluster_A.reth2["vlan"], cluster_A.reth2["network"]) = cluster_A.generate_networks()
(cluster_A.reth3["vlan"], cluster_A.reth3["network"]) = cluster_A.generate_networks()
print "Please create a cluster with following attributes:"
print "Hostname: %s" % cluster_A.name
print "Fabric interfaces: fab0 %s, fab1 %s" % (cluster_A.fab0, cluster_A.fab1)
print "Reth interfaces:"
print "reth0: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s" % (cluster_A.reth0["node_0_interface"], cluster_A.reth0["node_1_interface"], cluster_A.reth0["vlan"], cluster_A.reth0["network"])
print "reth1: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s" % (cluster_A.reth1["node_0_interface"], cluster_A.reth1["node_1_interface"], cluster_A.reth1["vlan"], cluster_A.reth1["network"])
print "reth2: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s" % (cluster_A.reth2["node_0_interface"], cluster_A.reth2["node_1_interface"], cluster_A.reth2["vlan"], cluster_A.reth2["network"])
print "reth3: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s" % (cluster_A.reth3["node_0_interface"], cluster_A.reth3["node_1_interface"], cluster_A.reth3["vlan"], cluster_A.reth3["network"])
print "Interfaces in zone untrust: %s" % cluster_A.zone_untrust
print "Interfaces in zone trust: %s" % cluster_A.zone_trust
print "Interfaces in zone dmz: %s" % cluster_A.zone_dmz

'''
print "%s, %s" % (cluster_A.reth0["vlan"], cluster_A.reth0["network"])
print "%s, %s" % (cluster_A.reth1["vlan"], cluster_A.reth1["network"])
print "%s, %s" % (cluster_A.reth2["vlan"], cluster_A.reth2["network"])
print "%s, %s" % (cluster_A.reth3["vlan"], cluster_A.reth3["network"])
print cluster_A.fab0
print cluster_A.fab1
'''