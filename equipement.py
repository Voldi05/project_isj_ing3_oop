


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
            raise ValueError(f"L'adresse IPv4 doit avoir 4 octets et la votre a {len(octets)}"  )
                
          
        
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
    def ip(self, val=str):
        """Definition du Setter sur l'adresse ip """
        if val is None:
            raise ValueError("Vous devez préciser l'adresse ip a ajouté")
        val=val.strip()
        
        if not isinstance(val, str):
            raise TypeError("Vous avez mal enregistré l'adresse ip. Le format correct est X.X.X.X avec X entre 0 et 255")
        
        self._ip = val
        self._valider_format()
    
    @property
    def classe_ip(self):
        """Permet d'avoir la classe d'une adresse ip"""
        Octet1= int(self._ip.split('.')[0])
        if Octet1 <127:
            return "Classe A"
        elif Octet1 <191:
            return "Classe B"
        elif Octet1 <223:
            return "Classe C"
        elif Octet1 <239:
            return "Classe D"
        else:
            return "Class E"

    @property
    def est_privee(self):
        """ Permet de verifier si une adresse est privée ou publique"""
        Octet1= int(self._ip.split('.')[0])
        Octet2= int(self._ip.split('.')[1])
        if Octet1 ==10:
            return "Adresse Privée"
        elif Octet1 ==172 ((Octet2 ==16) or (Octet2 == 31)) :
                return "Adresse Privée"
        elif Octet1 ==192 & Octet2== 168:
            return "Adresse Privée"
        
        else :
            return "Adresse Public"
        
     
        
            
                    
               
        
    

