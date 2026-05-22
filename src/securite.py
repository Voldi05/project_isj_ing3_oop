"""
securite.py — Règles de filtrage et sécurité Firewall pour SIMNet.
"""

import datetime

PROTOCOLES_VALIDES = ("TCP", "UDP", "ICMP")

class Regle:
    """Modélise une règle de filtrage pour le Firewall"""

    def __init__(self, action, ip_source=None, protocole=None,
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

    def __ip_dans_plage(self, ip, plage):
        """Vérifie si une adresse IP appartient à une plage réseau (ex: /8, /16, /24)"""
        try:
            ip_parts = ip.split(".")
            reseau, masque = plage.split("/")
            reseau_parts = reseau.split(".")
            masque = int(masque)

            if masque == 8:
                return ip_parts[0] == reseau_parts[0]
            elif masque == 16:
                return ip_parts[0] == reseau_parts[0] and ip_parts[1] == reseau_parts[1]
            elif masque == 24:
                return ip_parts[0] == reseau_parts[0] and ip_parts[1] == reseau_parts[1] and ip_parts[2] == reseau_parts[2]
        except Exception:
            return False
        return False

    def correspond(self, paquet):
        """Vérifie si un paquet réseau correspond aux critères de cette règle."""
        ip_src_paquet = getattr(paquet, 'ip_src', getattr(paquet, 'source', None))
        
        if self.ip_source is not None and ip_src_paquet != self.ip_source:
            return False

        if self.protocole is not None and paquet.protocole != self.protocole:
            return False

        port_dst_paquet = getattr(paquet, 'port_dst', None)
        if self.port_dst is not None and port_dst_paquet != self.port_dst:
            return False

        if self.plage_reseau is not None:
            if not self.__ip_dans_plage(ip_src_paquet, self.plage_reseau):
                return False

        return True

    def __str__(self):
        criteres = []
        if self.ip_source:    criteres.append("IP=" + self.ip_source)
        if self.protocole:    criteres.append("PROTO=" + self.protocole)
        if self.port_dst:     criteres.append("PORT=" + str(self.port_dst))
        if self.plage_reseau: criteres.append("PLAGE=" + self.plage_reseau)

        if criteres:
            return "[" + self.action + "] " + " | ".join(criteres) + " — " + self.description
        else:
            return "[" + self.action + "] TOUT — " + self.description


class GESTION_FIREWALL:
    """Classe de gestion pour étendre ou administrer les fonctionnalités de sécurité du Firewall"""
    
    def __init__(self, login, mdp):
        self.login = login
        self.mdp = mdp
        self.regles = []
        self.journal = []

    def authentifier(self, login, mdp):
        return login == self.login and mdp == self.mdp
    
    def ajouter_regle(self, regle, login, mdp):
        if not self.authentifier(login, mdp):
            print("Accès refusé : Authentification échouée.")
            return False
        self.regles.append(regle)
        print("Règle ajoutée avec succès.")
        return True
    
    def inspecter_paquet(self, paquet):
        """Inspecte le paquet par rapport aux règles de filtrage enregistrées."""
        for regle in self.regles:
            if regle.correspond(paquet):
                decision = (regle.action == "AUTORISER")
                self._journaliser(paquet, regle, decision)
                return decision
            
        # Si aucune règle ne correspond, comportement par défaut : on BLOQUE
        self._journaliser(paquet, None, False)
        return False
        
    def _journaliser(self, paquet, regle, decision):
        """Enregistre l'événement d'inspection dans l'historique."""
        ip_src_paquet = getattr(paquet, 'ip_src', getattr(paquet, 'source', None))
        ip_dst_paquet = getattr(paquet, 'ip_dst', getattr(paquet, 'destination', None))
        port_dst_paquet = getattr(paquet, 'port_dst', "N/A")

        entree = (
            f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{paquet.protocole} de {ip_src_paquet} -> {ip_dst_paquet} | "
            f"Port: {port_dst_paquet} | Décision: {'AUTORISÉ' if decision else 'BLOQUÉ'} | "
            f"Règle: {str(regle) if regle else 'Aucune (Bloqué par défaut)'}"
        )
        self.journal.append(entree)

    def afficher_journal(self):
        """Affiche les logs stockés."""
        if not self.journal:
            print("Aucun événement dans le journal du pare-feu.")
        for entree in self.journal:
            print(entree)