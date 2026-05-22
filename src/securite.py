import datetime
import paquets

# Une règle dit si un paquet doit être AUTORISÉ ou BLOQUÉ selon certains critères 

class Regle:
    """Modélise une règle de filtrage pour le Firewall"""

    # Crée une règle avec une action obligatoire et des critères
    # facultatifs (on peut en mettre un, plusieurs, ou aucun)
    def _init_(self, action, ip_source=None, protocole=None,
                 port_dst=None, plage_reseau=None, description=""):
        """
        action       : "AUTORISER" ou "BLOQUER"         (obligatoire)
        ip_source    : ex. "192.168.1.5"                (facultatif)
        protocole    : "TCP", "UDP" ou "ICMP"           (facultatif)
        port_dst     : ex. 22, 80, 443                  (facultatif)
        plage_reseau : ex. "192.168.1.0/24"             (facultatif)
        description  : texte explicatif de la règle     (facultatif)
        """

        if action not in ("AUTORISER", "BLOQUER"):
            raise ValueError("L'action doit être 'AUTORISER' ou 'BLOQUER'")

        self.action       = action
        self.ip_source    = ip_source
        self.protocole    = protocole
        self.port_dst     = port_dst
        self.plage_reseau = plage_reseau
        self.description  = description


    # Méthode privée 
    # Vérifie si une adresse IP appartient à une plage réseau 
    def __ip_dans_plage(self, ip, plage):

        ip_parts= ip.split(".")
        reseau, masque= plage.split("/")
        reseau_parts= reseau.split(".")
        masque= int(masque)

        # Selon la taille du masque, on compare une partie de l'adresse :
        # /8: on compare seulement le 1er octet  (ex: réseau 10.x.x.x)
        # /16: on compare les 2 premiers octets   (ex: réseau 172.16.x.x)
        # /24: on compare les 3 premiers octets   (ex: réseau 192.168.1.x)
        if masque == 8:
            return ip_parts[0] == reseau_parts[0]

        elif masque == 16:
            return ip_parts[0] == reseau_parts[0] and \
                   ip_parts[1] == reseau_parts[1]

        elif masque == 24:
            return ip_parts[0] == reseau_parts[0] and \
                   ip_parts[1] == reseau_parts[1] and \
                   ip_parts[2] == reseau_parts[2]
        return False # Masque non supporté


    #Méthode qui vérifie si un paquet réseau correspond aux critères de cette règle
    def correspond(self, paquet):
        """Vérifie si un paquet réseau correspond à cette règle."""

        # Vérification de l'IP source
        if self.ip_source is not None and paquet.ip_src != self.ip_source:
            return False

        # Vérification du protocole 
        if self.protocole is not None and paquet.protocole != self.protocole:
            return False

        # Vérification du port de destination
        if self.port_dst is not None and paquet.port_dst != self.port_dst:
            return False
        
        # Vérification de la plage réseau
        if self.plage_reseau is not None:
            if not self.__ip_dans_plage(paquet.ip_src, self.plage_reseau):
                return False
        return True

    #Définit comment afficher une règle avec print()
    def _str_(self):

        #liste des critères définis dans cette règle
        criteres = []
        if self.ip_source:    criteres.append("IP="    + self.ip_source)
        if self.protocole:    criteres.append("PROTO=" + self.protocole)
        if self.port_dst:     criteres.append("PORT="  + str(self.port_dst))
        if self.plage_reseau: criteres.append("PLAGE=" + self.plage_reseau)

        #Si les critère existent, on les joint avec " | " sinon on affiche "TOUT" (la règle s'applique à tous les paquets)
        if criteres:
            entete = "[" + self.action + "] " + " | ".join(criteres)
        else:
            entete = "[" + self.action + "] TOUT"
        return entete + " — " + self.description







    # Constructeur appelé quand on fait : Regle("BLOQUER", ...)
    def __init__(self, action, ip_source=None, protocole=None,
                 port_dst=None, plage_reseau=None, description=""):
        
        # Vérification que l'action est valide
        if action not in ("AUTORISER", "BLOQUER"):
            raise ValueError("action non valide")

        self.action       = action
        self.ip_source    = ip_source
        self.protocole    = protocole
        self.port_dst     = port_dst
        self.plage_reseau = plage_reseau
        self.description  = description


    # Vérifie si une adresse IP appartient à une plage réseau
    # Ex: "192.168.1.10" est-elle dans "192.168.1.0/24"?
    def __ip_dans_plage(self, ip, plage):

        ip_parts = ip.split(".")
        reseau, masque = plage.split("/")
        reseau_parts = reseau.split(".")
        masque = int(masque)

        # Cas pour /8, /16, /24
        if masque == 8:
            return ip_parts[0] == reseau_parts[0]

        elif masque == 16:
            return (ip_parts[0] == reseau_parts[0] and ip_parts[1] == reseau_parts[1])
                    
        elif masque == 24:
            return (ip_parts[0] == reseau_parts[0] and ip_parts[1] == reseau_parts[1] and ip_parts[2] == reseau_parts[2])
        
        else:
            return False


    # Est-ce que le paquet correspond à cette règle?
    # Retourne True si oui, False si non
    def correspond(self, paquet):

        if self.ip_source is not None:
            if paquet.ip_src != self.ip_source:
                return False

        if self.protocole is not None:
            if paquet.protocole != self.protocole:
                return False


        if self.port_dst is not None:
            if paquet.port_dst != self.port_dst:
                return False

        if self.plage_reseau is not None:
            if not self.__ip_dans_plage(paquet.ip_src, self.plage_reseau):
                return False

        # si tous les critères correspondent
        return True


    # comment afficher une règle avec print()
    def __str__(self):

        criteres = []

        if self.ip_source is not None:
            criteres.append("IP=" + self.ip_source)

        if self.protocole is not None:
            criteres.append("PROTO=" + self.protocole)

        if self.port_dst is not None:
            criteres.append("PORT=" + str(self.port_dst))

        if self.plage_reseau is not None:
            criteres.append("PLAGE=" + self.plage_reseau)

        if criteres:
            return "[" + self.action + "] " + " | ".join(criteres) + " — " + self.description
        else:
            return "[" + self.action + "] — " + self.description




    def __init__(self, login, mdp):
        self.login = login
        self.mdp = mdp
        self.regles = []
        self.journal = []

        #Authentification
    def authentifier(self, login, mdp):
        if login == self.login and mdp == self.mdp:
            return True
        return False    
    
    #Ajout d'une regle
    def ajouter_regle(self, regle, login, mdp):

        if not self.authentifier(login, mdp):
            print("Accès refusé")
            return False

        self.regles.append(regle)
        print("Règle ajoutée")
        return True
    
# #inspection d'un paquet
# def inspecter_paquet(self, paquet):

#         for regle in self.regles:

#             if regle.correspond(paquet):

#                 if regle.action == "AUTORISER":
#                     decision = True
#                 else:
#                     decision = False

#                 self._journaliser(paquet, regle, decision)
#                 return decision
            
#             # si aucune règle trouvée, bloquer
#         self._journaliser(paquet, None, False)
#         return False
        

# # Journalisation
# def _journaliser(self, paquet, regle, decision):

#         entree = {
#             "heure": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "source": paquet.ip_src,
#             "destination": paquet.ip_dst,
#             "protocole": paquet.protocole,
#             "port": paquet.port_dst,
#             "decision": "AUTORISE" if decision else "BLOQUE",
#             "regle": str(regle) if regle else "Aucune règle"
#         }

#         self.journal.append(entree)

# # Affichage journal
# def afficher_journal(self):

        for entree in self.journal:
            print(entree)