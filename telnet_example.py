import subprocess
import telnetlib

#output = subprocess.check_output('vtysh -c "show ip ospf database"', shell = True)
tn = telnetlib.Telnet('192.168.3.1')
tn.write('show ip ospf database router 1.1.1.1\n')
output = tn.read_until('>')
output = tn.read_until('>')
tn.close
#divide it in rows
#rows = output.split('\n')

#remove the empty rows


#print rows[6].split(' ')[0]
print output
