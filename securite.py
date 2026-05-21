from equipements import Firewall as FirewallBase
import datetime
import hashlib


# CLASSE REGLE
# Une règle dit si un paquet doit être AUTORISÉ ou BLOQUÉ
# selon certains critères 

class Regle:

    # Constructeur appelé quand on fait : Regle("BLOQUER", ...)
    def __init__(self, action, ip_source=None, protocole=None,
                 port_dst=None, plage_reseau=None, description=""):
        """
        action       : "AUTORISER" ou "BLOQUER"
        ip_source    : ex. "192.168.1.5"    (facultatif)
        protocole    : "TCP", "UDP", "ICMP" (facultatif)
        port_dst     : ex. 22, 80, 443      (facultatif)
        plage_reseau : ex. "192.168.1.0/24" (facultatif)
        description  : texte explicatif     (facultatif)
        """

        # Vérification que l'action est valide
        if action not in ("AUTORISER", "BLOQUER"):
            raise ValueError("L'action doit être 'AUTORISER' ou 'BLOQUER'")

        # Données membres (attributs) de la règle
        self.action       = action
        self.ip_source    = ip_source
        self.protocole    = protocole
        self.port_dst     = port_dst
        self.plage_reseau = plage_reseau
        self.description  = description


    # Vérifie si une adresse IP appartient à une plage réseau
    # Ex: "192.168.1.10" est-elle dans "192.168.1.0/24"?
    def __ip_dans_plage(self, ip, plage):

        # On sépare l'IP en 4 parties: "192.168.1.10" → [192, 168, 1, 10]
        ip_parts     = list(map(int, ip.split(".")))
        reseau, bits = plage.split("/")
        bits         = int(bits)
        reseau_parts = list(map(int, reseau.split(".")))

        # Conversion en nombre entier pour pouvoir comparer
        ip_int     = sum(ip_parts[i]     << (24 - 8 * i) for i in range(4))
        reseau_int = sum(reseau_parts[i] << (24 - 8 * i) for i in range(4))

        # Calcul du masque réseau et comparaison
        masque_int = ((1 << 32) - 1) ^ ((1 << (32 - bits)) - 1)
        return (ip_int & masque_int) == (reseau_int & masque_int)


    # Méthode : est-ce que le paquet correspond à cette règle ?
    # Retourne True si oui, False si non
    def correspond(self, paquet):

        # Si un critère est défini et ne correspond pas, retourner False
        if self.ip_source and paquet.ip_src != self.ip_source:
            return False

        if self.protocole and paquet.protocole != self.protocole:
            return False

        if self.port_dst and paquet.port_dst != self.port_dst:
            return False

        if self.plage_reseau and not self.__ip_dans_plage(paquet.ip_src, self.plage_reseau):
            return False

        # Tous les critères correspondent,retourner True
        return True


    # comment afficher une règle avec print()
    def __str__(self):
        criteres = []
        if self.ip_source:    criteres.append("IP="    + self.ip_source)
        if self.protocole:    criteres.append("PROTO=" + self.protocole)
        if self.port_dst:     criteres.append("PORT="  + str(self.port_dst))
        if self.plage_reseau: criteres.append("PLAGE=" + self.plage_reseau)

        return "[" + self.action + "] " + " | ".join(criteres) + " — " + self.description


# CLASSE FIREWALL
# Hérite de FirewallBase (défini dans equipement.py)
# On ajoute authentification admin, règles avancées, journal

class Firewall(FirewallBase):

    # Constructeur
    def __init__(self, nomE, marqueE, adresse_ip, nb_interfaces, login, mdp, statut=True):
        """
        nomE          : nom du firewall       ex. "FW-Principal"
        marqueE       : marque                ex. "Cisco"
        adresse_ip    : adresse IP            ex. "192.168.1.1"
        nb_interfaces : nombre de ports
        login         : identifiant admin     ex. "admin"
        mdp           : mot de passe admin
        """

        # On appelle le constructeur de la classe mère (FirewallBase)
        super().__init__(nomE, marqueE, adresse_ip, nb_interfaces, statut)

        # Données membres propres au Firewall sécurisé
        self.__login    = login
        self.__mdp_hash = self.__hasher(mdp)  #car on ne stocke JAMAIS le mdp en clair

        self.regles  = []   # liste des règles de filtrage
        self.journal = []   # historique des décisions


    # AUTHENTIFICATION

    # Méthode privée: transforme le mot de passe en code illisible
    def __hasher(self, mdp):
        return hashlib.sha256(mdp.encode()).hexdigest()

    # Méthode publique: vérifie si le login et mdp sont corrects
    def authentifier(self, login, mdp):
        return login == self.__login and self.__hasher(mdp) == self.__mdp_hash


    # GESTION DES RÈGLES
    # Toutes les modifications nécessitent d'être authentifié
 
    def ajouter_regle(self, regle, login, mdp):
        """Ajoute une règle si les identifiants sont corrects."""

        if not self.authentifier(login, mdp):
            print("Accès refusé : identifiants incorrects.")
            return False

        self.regles.append(regle)
        print("Règle ajoutée : " + str(regle))
        return True


    def supprimer_regle(self, index, login, mdp):
        """Supprime la règle numéro 'index' si les identifiants sont corrects."""

        if not self.authentifier(login, mdp):
            print("Accès refusé : identifiants incorrects.")
            return False

        if index < 0 or index >= len(self.regles):
            print("Index invalide.")
            return False

        regle_supprimee = self.regles.pop(index)
        print("Règle supprimée : " + str(regle_supprimee))
        return True


    def afficher_regles(self):
        """Affiche toutes les règles dans l'ordre."""

        if not self.regles:
            print("Aucune règle configurée.")
            return

        print("\n" + "─" * 45)
        print("  Règles du Firewall [" + self._nom + "]")
        print("─" * 45)
        for i in range(len(self.regles)):
            print("  [" + str(i) + "] " + str(self.regles[i]))
        print("─" * 45 + "\n")


    # INSPECTION DES PAQUETS

    def inspecter_paquet(self, paquet):
        """
        Parcourt les règles dans l'ordre.
        La 1ère règle qui correspond est appliquée.
        Si aucune règle ne correspond on retourne AUTORISÉ par défaut.
        Retourne True (autorisé) ou False (bloqué).
        """

        for regle in self.regles:
            if regle.correspond(paquet):
                # On vérifie si l'action est AUTORISER
                autorise = (regle.action == "AUTORISER")
                self.__journaliser(paquet, regle.action, regle)
                return autorise

        # Aucune règle trouvée alors on autorise par défaut
        self.__journaliser(paquet, "AUTORISER (défaut)", None)
        return True


    # JOURNAL DES DÉCISIONS

    # Méthode privée : enregistre une décision avec la date et l'heure
    def __journaliser(self, paquet, decision, regle):
        entree = {
            "horodatage" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_src"     : paquet.ip_src,
            "ip_dst"     : paquet.ip_dst,
            "protocole"  : paquet.protocole,
            "port_dst"   : paquet.port_dst,
            "decision"   : decision,
            "regle"      : str(regle) if regle else "Aucune règle (défaut)"
        }
        self.journal.append(entree)


    def afficher_journal(self):
        """Affiche tout l'historique des décisions du firewall."""

        if not self.journal:
            print("Journal vide.")
            return

        print("\n" + "─" * 60)
        print("  Journal du Firewall [" + self._nom + "]")
        print("─" * 60)

        for entree in self.journal:
            print("  [" + entree["horodatage"] + "] "
                  + entree["ip_src"] + " → " + entree["ip_dst"]
                  + " (" + str(entree["protocole"])
                  + ", port " + str(entree["port_dst"]) + ")"
                  + " → " + entree["decision"])
            print("    Règle : " + entree["regle"])

        print("─" * 60 + "\n")


    #Méthode abstraite obligatoire héritée de Equipement
    def description_du_materiel(self):
        return "Firewall sécurisé — " + str(len(self.regles)) + " règle(s) active(s)"


    #__str__ : affichage avec print()
    def __str__(self):
        return "Firewall [" + self._nom + "] — IP: " + str(self._adresse_ip)