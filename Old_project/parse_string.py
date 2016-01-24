import subprocess

output = subprocess.check_output('vtysh -c "show ip ospf database"', shell = True)

#divide it in rows
rows = output.split('\n')

#remove the empty rows


print rows[6].split(' ')[0]

