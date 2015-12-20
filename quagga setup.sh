#!/bin/sh
#script to setup quagga environment

#	install quagga with
#	sudo apt-get install quagga quagga-doc

clear 

echo "Create .conf files"
touch /etc/quagga/zebra.conf
touch /etc/quagga/ospfd.conf

echo "Populate configuration files"
echo "hostname Router" >> /etc/quagga/zebra.conf
echo "password zebra" >> /etc/quagga/zebra.conf
echo "enable password zebra" >> /etc/quagga/zebra.conf
echo "hostname ospfd" >> /etc/quagga/ospfd.conf
echo "password zebra" >> /etc/quagga/ospfd.conf

echo "Set owner"
chown quagga:quagga /etc/quagga/zebra.conf
chown quagga:quagga /etc/quagga/ospfd.conf

echo "Set permits"
#	user = rw
#	group = r
#	other = -
chmod 640 /etc/quagga/zebra.conf
chmod 640 /etc/quagga/ospfd.conf

# manual configuration of conf files 
#	Enter /etc/quagga/daemons and set yes for both "zebra" and "ospfd"
#	Enter /etc/quagga/debian.conf and set the tun0 ip on "zebra_options" and "ospfd_options"

# to run the service 
#	/etc/init.d/quagga [start, restart, stop]

# to obtain topology
#	vtysh -c "show ip ospf database"




