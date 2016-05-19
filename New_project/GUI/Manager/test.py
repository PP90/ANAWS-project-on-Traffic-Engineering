"""
Copyright (c) 2016, Pietro Piscione, Luigi De Bianchi, Giulio Micheloni
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL P. PISCIONE, L. DE BIANCHI, G. MICHELONI BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import manager as man
import pprint
import time

m1 = man.Manager("192.168.3.1", "public", 'T')

a = m1.getTopology()
print("\n\n matrix")
pprint.pprint(a)

#a = m1.getListIP()
#print("\n\n list")
#pprint.pprint(a)

#a = m1.listInfo
#print("\n\n listInfo")
#pprint.pprint(a)

#a = m1.getAllUtilization(["1.1.1.1", "2.2.2.2", "4.4.4.4"])
#print("\n\n result")
#pprint.pprint(a)
#a = m1.getAllUtilization(["1.1.1.1", "2.2.2.2", "4.4.4.4"], True)
#print("\n\n result")
#pprint.pprint(a)

#a = m1.listInfo
#print("\n\n listInfo")
#pprint.pprint(a)

#a = m1.getRoutersList(["1.1.1.1"])
#print("\n\n getRoutersList")
#pprint.pprint(a)

#t = m1.getTunnel("1.1.1.1")
#print("\n Tunnels")
#print(t)

m1.startThreads(5, "a")
m1.startThreads(3, "b")
time.sleep(10)
m1.stopThreads()