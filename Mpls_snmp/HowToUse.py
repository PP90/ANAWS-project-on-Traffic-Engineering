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

