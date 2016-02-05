modprobe tun
tunctl
ifconfig tap0 192.168.3.24 netmask 255.255.255.0 up
ifconfig
