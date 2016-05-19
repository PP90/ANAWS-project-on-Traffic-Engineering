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

"""---------------------------
Come usare la classe TeTunnels:
---------------------------"""
from TeTunnels import *
from Container import * 

"""Istanziare la classe passandogli l'indirizzo IP del router da interrogare e la stringa community di SNMP"""
t = TeTunnels("5.5.5.5", "public")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Lanciare la funzione start() per far generare all'algoritmo le strutture dati contenenti le informazioni sui tunnel TE"""
t.start()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Prendere le due tabelle che descrivono le configurazioni dei tunnel sul router (la prima)"""
"""e gli LSP istanziati (cioe' quelli che effettivamente passano di li) sul router (la seconda)"""
confTunnels = t.getConfTunnels()

Lsp = t.getLspTable()

"""Queste due sono implementate come un dizionario di coppie <Nome : Oggetto Container>, il nome di puo' riferire al nome di una configurazione o di un LSP"""
"""L'oggetto Container a sua volta non e' altro che un dizionario composto da coppie <Attributo : valore>"""

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Per ogni oggetto Container, con la funzione 'getAttribute(<sting>)' si puo' ottenere il valore di un attributo in particolare se si conosce il suo nome"""
#For each tunnel configuration:
for name in Lsp.keys():
	print name, Lsp[name].getAttribute("Computed Path")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Altrimenti con la funzione getAttributeDict() e' possibile prendersi l'intero dizionario formato dalle entry <'Attributo' : valore>"""
#For each tunnel configuration:
for name in confTunnels.keys():
	print name, confTunnels[name].getAttributeDict()

#For each LSP instance:	
for name in Lsp.keys():
	print name, Lsp[name].getAttributeDict()

