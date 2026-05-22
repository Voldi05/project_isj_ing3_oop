from abc import ABC , abstractmethod


class AdresseIP:
    """Gère une adresse IPv4 avec validation et utilitaires."""
    
    def __init__(self, ip_str):
        """
        Initialise une adresse IP.
        
            ip_str: L'adresse IP sous forme de chaîne (ex: "192.168.1.1")
        """
        # On vérifi si l'utilisateur n'a rien entré comme adresse ip
        if ip_str is None:
            raise ValueError("Vous devez entrer une adresse IP")
        
        # Suppréssion des espaces (les espaces peuvent causer des erreurs)
        # Exemple: ip_str = ' 192.168.2.2' → L'espace au début va poser problème
        ip_str = ip_str.strip()
        
        # On verifi si l'utilisateur a seulement entré des espaces
        if not ip_str:
            raise ValueError("Vous avez mal enregistré l'adresse IP")
        
        self._ip = ip_str  # Attribut privé
        self._valider_format()
    
    def _valider_format(self):# C'est  une méthode inaccéssible par l'utilisateur à cause du underscore deveant le  premier mot du nom de la méthode
        """
         Permet de vérifié si une adresse IP est conforme au format IPv4
         qui est: X.X.X.X avec X entre 0 et 255.
        """
        octets = self._ip.split('.')
        
        # On verifi si le nombre d'octet est égal à 4 conformement au format IPv4
        if len(octets) != 4:
            # On ecrit un message  d'erreur si le nombre d'octet est différentde 4
            raise ValueError(f"L'adresse IPv4 doit avoir 4 octets et la vôtre a {len(octets)}")
        i = 0
        for octet in octets:
            i = i + 1
            
            # On verifi si chaque octet est constituer uniquement de chiffres
            if not octet.isdigit():
                raise ValueError( f"Octet {i} invalide: '{octet}' doit etre un nombre" )
                   
               
            
            # Vérifier la plage 0-255
            valeur = int(octet)
            if valeur < 0 or valeur > 255:
                raise ValueError(f"Octet {i} invalide: {valeur} (doit etre entre 0 et 255)" )

    @property #Definition du getter
    def ip(self):
        """" Definition du Getter sur l'adresse ip """
        return self._ip
    
    @ip.setter
    def ip(self, val):
        """Definition du Setter sur l'adresse ip """
        if val is None:
            raise ValueError("Vous devez préciser l'adresse ip à ajouter")
        
        if not isinstance(val, str):
            raise TypeError("L'adresse IP doit être une chaîne de caractères")
        val=val.strip()
        
        if not val:
            raise ValueError("Vous avez mal enregistré l'adresse IP. Le format correct est X.X.X.X avec X entre 0 et 255")
        
        self._ip = val
        self._valider_format()
    
    @property
    def classe_ip(self):
        """Permet d'avoir la classe d'une adresse ip"""
        Octet1= int(self._ip.split('.')[0])
        if 1<=Octet1 <=126:
            return "Classe A"
        elif 128<=Octet1 <=191:
            return "Classe B"
        elif 192<=Octet1 <=223:
            return "Classe C"
        elif 224<=Octet1 <=239:
            return "Classe D"
        else:
            return "Classe E"

    @property
    def est_privee(self):
        """ Permet de verifier si une adresse est privée ou publique"""
        Octet1= int(self._ip.split('.')[0])
        Octet2= int(self._ip.split('.')[1])
        if Octet1 ==10:
            return True
        elif Octet1 ==172 and((Octet2 ==16) or (Octet2 == 31)) :
                return True
        elif Octet1 ==192 and Octet2== 168:
            return True
        
        else :
            return False

    def __str__(self):
        priv = "Privée" if self.est_privee else "Publique"
        return f"{self._ip}-- Type:{priv} (Classe {self.classe_ip})"
    
    
    
    
#Création de la classe Equipement

class Equipement(ABC):
    """Classe destinée aux équipements """
    
    _nb_equipements=0
    def __init__(self, nomE, marqueE, adresse_ip,nb_interfaces=0, statut:bool= False):
        
        """" Definition du Constructeur pour la classe Equipement """
        
        # On vérifi si l'utilisateur n'a rien entré comme nom de l'équipement
        if nomE is None:
            raise ValueError("Vous devez entrer le nom")
        # On vérifi si l'utilisateur n'a rien entré comme marque de l'équipement
        if marqueE is None:
            raise ValueError("Vous devez entrer une adresse IP")
       
        self._nom = nomE
        self._marque = marqueE
        self._statut= statut
        self._adresse_ip =adresse_ip
        self._nb_interfaces = nb_interfaces # Contient le nombre d'interface d'un equipement
        self._interfaces_occupees = 0
        Equipement._nb_equipements+=1
        
    @abstractmethod
    def description_du_materiel(self):
        """" Retourne une description de l'équipement """
        pass
    
    @property
    def nom(self):
            
        """" Definition du Getter sur le nom de l'équipement """
            
        return self._nom
    @property
    def marque(self):
            
        """" Definition du Getter sur de la marque de l'équipement """
            
        return self._marque
    
    def activer(self):
        """Faire passer le statut d'un équipement à ACTIF"""
     
        self._statut= True
       
    def desactiver(self):
        """Faire passer le statut d'un équipement à INACTIF""" 
        self._statut=False
        
    def afficher_infos(self):
        """ Pour afficher les information à prpos d'un équipement """
        statut ="ACTIF" if self._statut else "INACTIF"
        print(f"  Nom     : {self._nom}")
        print(f"  Marque  :{self._marque}")
        print(f"  Ip     : {self._adresse_ip}")
        print(f"  Statut :{statut}")
        print(f" Interfaces(occpés/Total): {self._interfaces_occupees}/{self._nb_interfaces}")
            
    def __del__(self):
        """Permet de supprimer un équipement de la topologie """
        print(f"[DECONNEXION]{self._nom}({self._adresse_ip}) retiré du réseau")
        
    def _liberer_interface(self):
        """C'est une méthode protégée. Permet de liberer une interface. Elle ne peut pas directement être utiliser par l'utilisateur .
              Elle est utiliser dans le fichier topologie par la fonction Supprimer_lien """
        if self._interfaces_occupees > 0:
            self._interfaces_occupees -=1
            return True
        return False
    
    def  _occuper_interface(self):
        """C'est une méthode protégée.
                Elle est utiliser dans le fichier topologie par la fonction Ajouter_lien """
        
        if self._interfaces_occupees < self._nb_interfaces:
            self._interfaces_occupees +=1
            return True
        return False
    
    @property
    def nb_interface_equipement(self):
        """ Donne le nombre total d'interface d'un équipement """
        
        return self._nb_interfaces
    @property
    def interfaces_libres(self):
        """ Nombres d'intefaces libres"""
        
        return self._nb_interfaces- self._interfaces_occupees
    
    def a_interface_libre(self):
    
        return self._interfaces_occupees< self._nb_interfaces
       
         
class Routeur(Equipement):
    def __init__(self,nomE,marqueE,adresse_ip, nb_interfaces, statut:bool=True):
        super().__init__(nomE, marqueE, adresse_ip, nb_interfaces, statut)       
        self.__table_routage={}
        
        
    #a verifier    
    def ajouter_route(self, destination, next_hop) :
        """Ajoute une route vers une destination."""
        # Validation des adresses IP
        AdresseIP(destination)  # Lève une exception si invalide
        AdresseIP(next_hop)
        self.__table_routage[destination] = next_hop
    
    def trouver_prochain_saut(self, destination):
        """Trouve le prochain saut pour une destination donnée."""
        return self.__table_routage.get(destination)
    
    @property
    def table_routage(self) :
        return self.__table_routage.copy()
    
    def description_du_materiel(self) :
        return f"Routeur avec {len(self.__table_routage)} route(s)"


class Switch(Equipement):
    """Switch avec gestion des VLANs."""
    
    def __init__(self, nomE, marqueE,adresse_ip, nb_interfaces,statut: bool = True):
        super().__init__( nomE, marqueE, adresse_ip, nb_interfaces, statut)
        self.__vlans = [1]  # VLAN 1 par défaut
        
    
    def ajouter_vlan(self, vlan_id: int) :
        """Ajoute un VLAN au switch."""
        if vlan_id not in self.__vlans:
            self.__vlans.append(vlan_id)
    
    def retirer_vlan(self, vlan_id: int):
        """Retire un VLAN du switch."""
        if vlan_id in self.__vlans and vlan_id != 1:
            self.__vlans.remove(vlan_id)
    
    @property
    def vlans(self) :
        return self.__vlans.copy()
    
    def description_du_materiel(self) :
        return f"Switch - VLANs: {self.__vlans}"


class Serveur(Equipement):
    """Serveur exposant des services."""
    
    def __init__(self, nomE, marqueE, adresse_ip, nb_interfaces,statut: bool = True):
        super().__init__( nomE, marqueE, adresse_ip, nb_interfaces, statut)
        self.__services= []
        
    
    def ajouter_service(self, service: str) :
        """Ajoute un service au serveur."""
        self.__services.append(service)
    
    @property
    def services(self) :
        return self.__services.copy()
    
    def description_du_materiel(self) :
        services_str = ', '.join(self.__services) if self.__services else 'aucun'
        return f"Serveur - Services: {services_str}"


class Firewall(Equipement):
    """Firewall avec règles de filtrage."""
    
    def __init__(self, nomE, marqueE,adresse_ip, nb_interfaces,statut: bool = True):
        super().__init__( nomE, marqueE, adresse_ip, nb_interfaces, statut)
        self.__regles= []  # Les règles seront détaillées dans le Module 3
        
    
    def ajouter_regle(self, regle: dict) :
        """Ajoute une règle de filtrage."""
        self.__regles.append(regle)
    
    @property
    def regles(self):
        return self.__regles.copy()
    
    def description_du_materiel(self) :
        return f"Firewall - {len(self.__regles)} règle(s)"


class PointAccesWiFi(Equipement):
    """Point d'accès WiFi."""
    
    def __init__(self,  nomE, marqueE, adresse_ip, nb_interfaces,  ssid= "", statut: bool = True):
        super().__init__( nomE, marqueE, adresse_ip, nb_interfaces, statut)
        self.__ssid = ssid
        
    
    @property
    def ssid(self) :
        return self.__ssid
    
    @ssid.setter
    def ssid(self, valeur):
        self.__ssid = valeur
    
    def description_du_materiel(self) :
        ssid_str = self.__ssid if self.__ssid else 'non configuré'
        return f"Point d'accès WiFi - SSID: {ssid_str}"


class TerminalClient(Equipement):
    """Terminal client (ordinateur, smartphone, etc.)."""
    
    def __init__(self, nomE, marqueE, adresse_ip, nb_interfaces,statut: bool = True):
        super().__init__( nomE, marqueE, adresse_ip, nb_interfaces, statut)
        self.__trafic_genere = 0  # Pour les statistiques
        
    
    def envoyer_donnees(self, taille):
        """Simule l'envoi de données."""
        self.__trafic_genere += taille
    
    @property
    def trafic_genere(self) :
        return self.__trafic_genere
    
    def description_du_materiel(self) :
        return "Terminal client"  


            
                  
               
        
    

