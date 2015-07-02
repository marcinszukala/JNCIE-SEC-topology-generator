#!/usr/bin/python
from random import randint
from random import shuffle
from random import choice
from random import randrange
from netaddr import *
import random

class vsrx_cluster:

  def __init__(self, name, location):
    self.fxp0 = ""
    self.fxp1 = ""
    self.fab0 = "ge-0/0/2"
    self.fab1 = "ge-7/0/2"
    self.reth0 = {"node_0_interface": "ge-0/0/3", "node_1_interface": "ge-7/0/3", "vlan": "", "network": "", "ipaddr": ""}
    self.reth1 = {"node_0_interface": "ge-0/0/4", "node_1_interface": "ge-7/0/4", "vlan": "", "network": "", "ipaddr": ""}
    self.reth2 = {"node_0_interface": "ge-0/0/5", "node_1_interface": "ge-7/0/5", "vlan": "", "network": "", "ipaddr": ""}
    self.reth3 = {"node_0_interface": "ge-0/0/6", "node_1_interface": "ge-7/0/6", "vlan": "", "network": "", "ipaddr": ""}
    self.zone_untrust = "reth0"
    self.zone_trust = ""
    self.zone_dmz = ""
    self.hosts = []
    self.name = name
    self.location = location
    #print "%s %s" % (self.name, self.location)
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
    self.netmask = randint(24,26)
    self.octets = "%s.%s.%s.%s/%s" % (self.first_octet, self.second_octet, self.third_octet, self.fourth_octet, self.netmask)
    self.ip = IPNetwork(self.octets)
    self.vlan = self.third_octet
    self.network = self.ip.cidr
    self.ipaddr = self.ip[1]
    return self.vlan, self.network, self.ipaddr
    
class hosts:
  def __init__(self, ip, cluster):
    self.ip = ip
    self.cluster = cluster
    self.services = random.choice(services)

wan_network = "10.%s.%s.0/24" % (randint(150,254), randint(170,254))
wan_network = IPNetwork(wan_network)
cluster_class_holder = {"cluster_A": "", "cluster_B": "", "cluster_C": ""}
hosts_class_holder = {}
services = ["TCP/22", "TCP/23", "TCP/80", "TCP/443", "TCP/25", "TCP/110", "UDP/53"]
i = 1
for clustername in cluster_class_holder:
  #print clustername.split("_")[1]
  cluster_class_holder[clustername] = vsrx_cluster(clustername,clustername.split("_")[1])
  (cluster_class_holder[clustername].reth0["vlan"], cluster_class_holder[clustername].reth0["network"], cluster_class_holder[clustername].reth0["ipaddr"])  = ("0", wan_network.cidr, wan_network[i])
  (cluster_class_holder[clustername].reth1["vlan"], cluster_class_holder[clustername].reth1["network"], cluster_class_holder[clustername].reth1["ipaddr"]) = cluster_class_holder[clustername].generate_networks()
  (cluster_class_holder[clustername].reth2["vlan"], cluster_class_holder[clustername].reth2["network"], cluster_class_holder[clustername].reth2["ipaddr"]) = cluster_class_holder[clustername].generate_networks()
  (cluster_class_holder[clustername].reth3["vlan"], cluster_class_holder[clustername].reth3["network"], cluster_class_holder[clustername].reth3["ipaddr"]) = cluster_class_holder[clustername].generate_networks()
  i += 1

for clustername in cluster_class_holder:
  hosts_network_reth1 = IPNetwork(cluster_class_holder[clustername].reth1["network"])
  hosts_network_reth2 = IPNetwork(cluster_class_holder[clustername].reth2["network"])
  hosts_network_reth3 = IPNetwork(cluster_class_holder[clustername].reth3["network"])

  for i in range(1):
    key = "%s_reth1_%s" % (clustername, i)
    hostip = hosts_network_reth1[randint(10,30)]
    hosts_class_holder[key] = hosts(hostip, clustername)
    cluster_class_holder[clustername].hosts.append(key)
  for i in range(2):
    key = "%s_reth2_%s" % (clustername, i)
    hostip = hosts_network_reth2[randint(10,30)]
    hosts_class_holder[key] = hosts(hostip, clustername)
    cluster_class_holder[clustername].hosts.append(key)
  for i in range(1):
    key = "%s_reth3_%s" % (clustername, i)
    hostip = hosts_network_reth2[randint(10,30)]
    hosts_class_holder[key] = hosts(hostip, clustername)
    cluster_class_holder[clustername].hosts.append(key)


for clustername in cluster_class_holder:
  print "Please create a cluster with following attributes: %s" % clustername
  print "Hostname: %s" % cluster_class_holder[clustername].name
  print "Fabric interfaces: fab0 %s, fab1 %s" % (cluster_class_holder[clustername].fab0, cluster_class_holder[clustername].fab1)
  print "Reth interfaces:"
  print "reth0: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s, ipaddr: %s" % (cluster_class_holder[clustername].reth0["node_0_interface"], cluster_class_holder[clustername].reth0["node_1_interface"], cluster_class_holder[clustername].reth0["vlan"], cluster_class_holder[clustername].reth0["network"], cluster_class_holder[clustername].reth0["ipaddr"])
  print "reth1: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s, ipaddr: %s" % (cluster_class_holder[clustername].reth1["node_0_interface"], cluster_class_holder[clustername].reth1["node_1_interface"], cluster_class_holder[clustername].reth1["vlan"], cluster_class_holder[clustername].reth1["network"], cluster_class_holder[clustername].reth1["ipaddr"])
  print "reth2: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s, ipaddr: %s" % (cluster_class_holder[clustername].reth2["node_0_interface"], cluster_class_holder[clustername].reth2["node_1_interface"], cluster_class_holder[clustername].reth2["vlan"], cluster_class_holder[clustername].reth2["network"], cluster_class_holder[clustername].reth2["ipaddr"])
  print "reth3: node0 interface: %s, node1 interface: %s, vlan: %s, network: %s, ipaddr: %s" % (cluster_class_holder[clustername].reth3["node_0_interface"], cluster_class_holder[clustername].reth3["node_1_interface"], cluster_class_holder[clustername].reth3["vlan"], cluster_class_holder[clustername].reth3["network"], cluster_class_holder[clustername].reth3["ipaddr"])
  print "Interfaces in zone untrust: %s" % cluster_class_holder[clustername].zone_untrust
  print "Interfaces in zone trust: %s" % cluster_class_holder[clustername].zone_trust
  print "Interfaces in zone dmz: %s" % cluster_class_holder[clustername].zone_dmz

#for host in hosts_class_holder:
#  print "cluster: %s, host: %s, ip: %s, service: %s" % (hosts_class_holder[host].cluster, host, hosts_class_holder[host].ip, hosts_class_holder[host].services)

hostnames = hosts_class_holder.keys()
for host in hostnames:
  print "Create policy from %s, ip %s to %s, ip %s, service %s" % (host, hosts_class_holder[host].ip, hostnames[-1], hosts_class_holder[hostnames[-1]].ip, hosts_class_holder[hostnames[-1]].services)
  hostnames.pop()