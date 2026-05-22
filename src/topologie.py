from equipements import Equipement, Routeur, Switch, Serveur, Firewall, PointAccesWiFi, TerminalClient


class Lien:
    """Représente une connexion entre deux équipements."""
    
    def __init__(self, equipement1, equipement2, bande_passante, latence):
        """
        Crée un lien entre deux équipements.
        
        Args:
            equipement1: Premier équipement
            equipement2: Deuxième équipement
            bande_passante: Bande passante en Mbps
            latence: Latence en ms
        """
        self.__equipement1 = equipement1
        self.__equipement2 = equipement2
        self.__bande_passante = bande_passante
        self.__latence = latence
    
    @property
    def equipement1(self):
        return self.__equipement1
    
    @property
    def equipement2(self):
        return self.__equipement2
    
    @property
    def bande_passante(self):
        return self.__bande_passante
    
    @property
    def latence(self):
        return self.__latence
    
    def autre_extremite(self, equipement):
        """Retourne l'autre équipement du lien."""
        if equipement == self.__equipement1:
            return self.__equipement2
        elif equipement == self.__equipement2:
            return self.__equipement1
        return None
    
    def contains(self, equipement): # Pour compatibilité au cas où
        return self.contient(equipement)

    def contient(self, equipement):
        """Vérifie si l'équipement fait partie du lien."""
        return equipement == self.__equipement1 or equipement == self.__equipement2
    
    def __str__(self):
        return f"{self.__equipement1.nom} <--[{self.__bande_passante} Mbps, {self.__latence} ms]--> {self.__equipement2.nom}"


class Topologie:
    """Gère l'ensemble des équipements et liens du réseau."""
    
    def __init__(self):
        self.__equipements = []
        self.__liens = []
    
    # ========== Gestion des équipements ==========
    
    def ajouter_equipement(self, equipement):
        """Ajoute un équipement à la topologie."""
        if equipement not in self.__equipements:
            self.__equipements.append(equipement)
            print(f" Équipement '{equipement.nom}' ajouté à la topologie")
            return True
        print(f" Équipement '{equipement.nom}' existe déjà")
        return False
    
    def supprimer_equipement(self, equipement):
        """Supprime un équipement et tous ses liens."""
        if equipement in self.__equipements:
            # Supprimer tous les liens impliquant cet équipement
            liens_a_supprimer = [l for l in self.__liens if l.contient(equipement)]
            for lien in liens_a_supprimer:
                self.supprimer_lien(lien)
            
            self.__equipements.remove(equipement)
            print(f" Équipement '{equipement.nom}' supprimé")
            return True
        print(f" Équipement '{equipement.nom}' non trouvé")
        return False
    
    def trouver_equipement(self, ip):
        """Trouve un équipement par son adresse IP."""
        for equipement in self.__equipements:
            # Utilise l'attribut _adresse_ip existant
            if equipement._adresse_ip.ip == ip:
                return equipement
        return None
    
    # ========== Gestion des liens ==========
    
    def ajouter_lien(self, equipement1, equipement2, bande_passante, latence):
        """
        Ajoute un lien entre deux équipements.
        
        Vérifie que les deux équipements ont des interfaces libres.
        """
        # Vérifier que les équipements existent
        if equipement1 not in self.__equipements:
            print(f" Équipement '{equipement1.nom}' non présent dans la topologie")
            return False
        
        if equipement2 not in self.__equipements:
            print(f" Équipement '{equipement2.nom}' non présent dans la topologie")
            return False
        
        # Vérifier que ce n'est pas un lien vers soi-même
        if equipement1 == equipement2:
            print(" Impossible de créer un lien vers soi-même")
            return False
        
        # Vérifier que les équipements ont des interfaces libres
        if not equipement1.a_interface_libre():
            print(f" {equipement1.nom} n'a plus d'interface libre ({equipement1.interfaces_libres}/{equipement1.nb_interface_equipement})")
            return False
        
        if not equipement2.a_interface_libre():
            print(f" {equipement2.nom} n'a plus d'interface libre ({equipement2.interfaces_libres}/{equipement2.nb_interface_equipement})")
            return False
        
        # Vérifier que le lien n'existe pas déjà
        for lien in self.__liens:
            if (lien.equipement1 == equipement1 and lien.equipement2 == equipement2) or \
               (lien.equipement1 == equipement2 and lien.equipement2 == equipement1):
                print(f"Un lien existe déjà entre {equipement1.nom} et {equipement2.nom}")
                return False
        
        # Créer le lien
        lien = Lien(equipement1, equipement2, bande_passante, latence)
        self.__liens.append(lien)
        
        # Occuper les interfaces (méthodes protégées existantes)
        equipement1._occuper_interface()
        equipement2._occuper_interface()
        
        print(f" Lien créé : {lien}")
        return True
    
    def supprimer_lien(self, lien):
        """Supprime un lien et libère les interfaces."""
        if lien in self.__liens:
            # Libérer les interfaces (méthodes protégées existantes)
            lien.equipement1._liberer_interface()
            lien.equipement2._liberer_interface()
            
            self.__liens.remove(lien)
            print(f" Lien supprimé : {lien}")
            return True
        return False
    
    def trouver_liens_equipement(self, equipement):
        """Retourne tous les liens d'un équipement."""
        liens = []
        for lien in self.__liens:
            if lien.contient(equipement):
                liens.append(lien)
        return liens
    
    def afficher_liens_equipement(self, equipement):
        """Affiche tous les liens d'un équipement."""
        liens = self.trouver_liens_equipement(equipement)
        
        if not liens:
            print(f"  {equipement.nom} n'est connecté à aucun équipement")
            return
        
        # Utilisation des attributs existants
        print(f"\n  Connexions de {equipement.nom} ({equipement._interfaces_occupees}/{equipement.nb_interface_equipement} interfaces utilisées):")
        for i, lien in enumerate(liens, 1):
            autre = lien.autre_extremite(equipement)
            print(f"    {i}. ↔ {autre.nom} ({lien.bande_passante} Mbps, {lien.latence} ms)")
    
    # ========== Algorithme de Routage / Recherche de Chemin ==========
    
    def trouver_chemin(self, source, destination):
        """
        Trouve le chemin le plus court (en nombre de sauts) entre deux équipements ou adresses IP.
        Retourne une liste d'équipements représentant le chemin, ou None s'il n'y a pas de chemin.
        """
        # Résolution des objets équipements si des objets AdresseIP ou chaînes ont été transmis
        eq_source = source
        eq_dest = destination
        
        if not isinstance(eq_source, Equipement):
            ip_str = getattr(eq_source, 'ip', str(eq_source))
            eq_source = self.trouver_equipement(ip_str)
            
        if not isinstance(eq_dest, Equipement):
            ip_str = getattr(eq_dest, 'ip', str(eq_dest))
            eq_dest = self.trouver_equipement(ip_str)
            
        if not eq_source or not eq_dest:
            return None
            
        if eq_source == eq_dest:
            return [eq_source]
            
        # Algorithme BFS (Breadth-First Search) pour trouver le plus court chemin
        queue = [[eq_source]]
        visite = {eq_source}
        
        while queue:
            chemin_actuel = queue.pop(0)
            noeud_actuel = chemin_actuel[-1]
            
            if noeud_actuel == eq_dest:
                return chemin_actuel
                
            # Parcourir tous les voisins via les liens existants
            for lien in self.trouver_liens_equipement(noeud_actuel):
                voisin = lien.autre_extremite(noeud_actuel)
                if voisin and voisin not in visite:
                    visite.add(voisin)
                    nouveau_chemin = list(chemin_actuel)
                    nouveau_chemin.append(voisin)
                    queue.append(nouveau_chemin)
                    
        return None # Aucun chemin trouvé

    # Affichage
    
    def afficher_topologie(self):
        """Affiche toute la topologie."""
        print("\n" + "=" * 50)
        print("TOPOLOGIE DU RÉSEAU")
        print("=" * 50)
        
        print("\n--- Équipements ---")
        if not self.__equipements:
            print("  Aucun équipement")
        else:
            for equipement in self.__equipements:
                # Utilisation de _adresse_ip.ip pour obtenir l'IP
                print(f"  • {equipement.nom} ({equipement.marque}) - {equipement._adresse_ip} - {equipement._interfaces_occupees}/{equipement.nb_interface_equipement} interfaces")
        
        print("\n--- Liens ---")
        if not self.__liens:
            print("  Aucun lien")
        else:
            for lien in self.__liens:
                print(f"  •  {lien}")
        
        print("\n--- Détail des connexions ---")
        for equipement in self.__equipements:
            self.afficher_liens_equipement(equipement)
    def obtenir_lien(self, equipement1, equipement2):
        """Retourne le lien existant entre deux équipements, ou None s'ils ne sont pas connectés."""
        for lien in self.__liens:
            if lien.contient(equipement1) and lien.contient(equipement2):
                return lien
        return None
    @property
    def equipements(self):
        return self.__equipements.copy()
    
    @property
    def liens(self):
        return self.__liens.copy()