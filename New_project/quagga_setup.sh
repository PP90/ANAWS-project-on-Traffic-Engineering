
#!/bin/sh

#sudo request
if [ $UID != 0 ]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

read -p "Need to install? (y/n)" yn
case $yn in
	[Yy]*) sudo apt-get install quagga quagga-doc
esac

echo "Create .conf files"
echo "\tCreate zebra.conf"
touch /etc/quagga/zebra.conf
echo "\tCreate ospfd.conf"
touch /etc/quagga/ospfd.conf

echo "Populate configuration files"
#zebra.conf
echo "hostname Router" >> /etc/quagga/zebra.conf
echo "password zebra" >> /etc/quagga/zebra.conf
echo "enable password zebra" >> /etc/quagga/zebra.conf
#ospfd.conf
echo "hostname ospfd" >> /etc/quagga/ospfd.conf
echo "password zebra" >> /etc/quagga/ospfd.conf
echo "router ospf" >> /etc/quagga/ospfd.conf
#ask user data
echo "\tPlease enter needed data (double check since no control is implemented)"
read -p "\taddress of the local router? " addr
read -p "\t# of netmask bit? " num
read -p "\tospf area? " area
echo "  network "$addr"/"$num" area "$area >> /etc/quagga/ospfd.conf

echo "Set owner"
chown quagga:quagga /etc/quagga/zebra.conf
chown quagga:quagga /etc/quagga/ospfd.conf
echo "\t done"

echo "Set permits"
#	user = rw
#	group = r
#	other = -
chmod 640 /etc/quagga/zebra.conf
chmod 640 /etc/quagga/ospfd.conf
echo "\t done"

echo "manual configuration of conf files "
echo "\tEnter /etc/quagga/daemons and set yes for both \"zebra\" and \"ospfd\""
echo "\tEnter /etc/quagga/debian.conf and set the tun0 ip on \"zebra_options\" and \"ospfd_options\""

echo "to run the service "
echo "sudo /etc/init.d/quagga [start, restart, stop]"

echo "to obtain topology"
echo "\tsudo vtysh -c \"show ip ospf database\""

exit
