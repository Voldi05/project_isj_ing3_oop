class Equipement:
    """Stub temporaire — sera remplacé par equipements.py"""
    def __init__(self, nom, ip, marque):
        self.nom = nom
        self.ip = ip
        self.marque = marque


# Stub temporaire (à remplacer quand equipements.py sera dispo)
class Equipement:
    def __init__(self, nom, ip, marque):
        self.nom = nom
        self.ip = ip
        self.marque = marque


class Regle:
    """
    Représente une règle de filtrage du firewall.
    Une règle définit une action (AUTORISER/BLOQUER) et des critères
    de correspondance sur les paquets réseau.
    """

    def __init__(self, action, ip_source=None, protocole=None, 
                 port_dst=None, plage_reseau=None, description=""):
        """
        action       : "AUTORISER" ou "BLOQUER"
        ip_source    : ex. "192.168.1.5"
        protocole    : "TCP", "UDP" ou "ICMP"
        port_dst     : ex. 22, 80, 443
        plage_reseau : ex. "10.0.0.0/24"
        description  : texte libre pour expliquer la règle
        """
        if action not in ("AUTORISER", "BLOQUER"):
            raise ValueError("L'action doit être 'AUTORISER' ou 'BLOQUER'")

        self.action = action
        self.ip_source = ip_source
        self.protocole = protocole
        self.port_dst = port_dst
        self.plage_reseau = plage_reseau
        self.description = description

    def _ip_dans_plage(self, ip, plage):
        """
        Vérifie si une IP appartient à une plage réseau
        """
        ip_parts = list(map(int, ip.split(".")))
        reseau, masque = plage.split("/")
        masque = int(masque)
        reseau_parts = list(map(int, reseau.split(".")))

        # Convertir IP et réseau en entiers 32 bits
        ip_int = sum(ip_parts[i] << (24 - 8 * i) for i in range(4))
        reseau_int = sum(reseau_parts[i] << (24 - 8 * i) for i in range(4))

        # Appliquer le masque et comparer
        masque_int = ((1 << 32) - 1) ^ ((1 << (32 - masque)) - 1)
        return (ip_int & masque_int) == (reseau_int & masque_int)

    def correspond(self, paquet):
        """
        Vérifie si un paquet correspond à cette règle :
        Retourne True si le paquet correspond, False sinon.
        """
        if self.ip_source and paquet.ip_src != self.ip_source:
            return False

        if self.protocole and paquet.protocole != self.protocole:
            return False

        if self.port_dst and paquet.port_dst != self.port_dst:
            return False

        if self.plage_reseau and not self._ip_dans_plage(paquet.ip_src, self.plage_reseau):
            return False

        return True

    def __str__(self):
        criteres = []
        if self.ip_source:
            criteres.append(f"IP={self.ip_source}")
        if self.protocole:
            criteres.append(f"PROTO={self.protocole}")
        if self.port_dst:
            criteres.append(f"PORT={self.port_dst}")
        if self.plage_reseau:
            criteres.append(f"PLAGE={self.plage_reseau}")

        return f"[{self.action}] {' | '.join(criteres)} — {self.description}"
    



import datetime
import hashlib

class Firewall(Equipement):
    """
    Représente un firewall réseau.
    Hérite de Equipement et ajoute des capacités de filtrage,
    de journalisation et d'authentification.
    """

    def __init__(self, nom, ip, marque, login, mdp):
        """
        login: identifiant administrateur
        mdp: mot de passe (sera stocké hashé)
        """
        super().__init__(nom, ip, marque)
        self._login = login
        self._mdp_hash = self._hasher(mdp)  #on ne stocke jamais le mdp en clair
        self.regles = []   #liste ordonnée de Regle
        self.journal = []  #historique de toutes les décisions

    #Authentification
    def _hasher(self, mdp):
        """Retourne le hash SHA-256 du mot de passe."""
        return hashlib.sha256(mdp.encode()).hexdigest()

    def authentifier(self, login, mdp):
        """
        Retourne True si login et mot de passe sont corrects.
        """
        return login == self._login and self._hasher(mdp) == self._mdp_hash

    #Gestion des règles (protégée par auth)
    def ajouter_regle(self, regle, login, mdp):
        """
        Ajoute une règle à la liste.
        Nécessite une authentification valide.
        """
        if not self.authentifier(login, mdp):
            print("Accès refusé : identifiants incorrects.")
            return False

        self.regles.append(regle)
        print(f"Règle ajoutée : {regle}")
        return True

    def supprimer_regle(self, index, login, mdp):
        """
        Supprime la règle à la position index.
        Nécessite une authentification valide.
        """
        if not self.authentifier(login, mdp):
            print("Accès refusé : identifiants incorrects.")
            return False

        if index < 0 or index >= len(self.regles):
            print("Index invalide.")
            return False

        regle_supprimee = self.regles.pop(index)
        print(f"Règle supprimee : {regle_supprimee}")
        return True

    def afficher_regles(self):
        """Affiche toutes les règles dans l'ordre."""
        if not self.regles:
            print("Aucune règle configurée.")
            return

        print(f"\n{'─'*40}")
        print(f"  Règles du Firewall [{self.nom}]")
        print(f"{'─'*40}")
        for i, regle in enumerate(self.regles):
            print(f"  [{i}] {regle}")
        print(f"{'─'*40}\n")

    #Inspection des paquets
    def inspecter_paquet(self, paquet):
        """
        Inspecte un paquet en parcourant les règles dans l'ordre.
        La première règle qui correspond est appliquée.
        Si aucune règle ne correspond, le paquet est AUTORISÉ par défaut.
        Retourne True si le paquet est autorisé, False s'il est bloqué.
        """
        for regle in self.regles:
            if regle.correspond(paquet):
                autorise = (regle.action == "AUTORISER")
                self._journaliser(paquet, regle.action, regle)
                return autorise

        #Aucune règle trouvée = on autorise par défaut
        self._journaliser(paquet, "AUTORISER (défaut)", None)
        return True

   #journal
    def _journaliser(self, paquet, decision, regle):
        """Enregistre une décision dans le journal avec horodatage."""
        entree = {
            "horodatage": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_src": paquet.ip_src,
            "ip_dst": paquet.ip_dst,
            "protocole": paquet.protocole,
            "port_dst": paquet.port_dst,
            "decision": decision,
            "regle": str(regle) if regle else "Aucune règle (défaut)"
        }
        self.journal.append(entree)

    def afficher_journal(self):
        """Affiche tout le journal des décisions."""
        if not self.journal:
            print("Journal vide.")
            return

        print(f"\n{'─'*60}")
        print(f"  Journal du Firewall [{self.nom}]")
        print(f"{'─'*60}")
        for entree in self.journal:
            print(f"  [{entree['horodatage']}] "
                  f"{entree['ip_src']} → {entree['ip_dst']} "
                  f"({entree['protocole']}, port {entree['port_dst']}) "
                  f"→ {entree['decision']}")
            print(f"    Règle : {entree['regle']}")
        print(f"{'─'*60}\n")
    