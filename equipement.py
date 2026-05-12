"""Module de gestion des adresses IP pour SIMNet."""


class AdresseIP:
    """Gère une adresse IPv4 avec validation et utilitaires."""
    
    def __init__(self, ip_str):
        """
        Initialise une adresse IP.
        
            ip_str: L'adresse IP sous forme de chaîne (ex: "192.168.1.1")
        """
        # Vérifier si l'utilisateur n'a rien entré
        if ip_str is None:
            raise ValueError("Vous devez entrer une adresse IP")
        
        # Nettoyer les espaces (les espaces peuvent causer des erreurs)
        # Exemple: ip_str = ' 192.168.2.2' → L'espace au début pose problème
        ip_str = ip_str.strip()
        
        # Vérifier si l'utilisateur a seulement entré des espaces
        if not ip_str:
            raise ValueError("Vous avez mal enregistré l'adresse IP")
        
        self._ip = ip_str  # Attribut privé
        self._valider_format()
    
    def _valider_format(self):
        """
        Vérifie si une adresse IP est conforme au format IPv4.
        
        Format attendu: X.X.X.X avec X entre 0 et 255.
        """
        octets = self._ip.split('.')
        
        # Vérifier le nombre d'octets
        if len(octets) != 4:
            raise ValueError(
                f"L'adresse IPv4 doit avoir 4 octets et la votre a {len(octets)}"
            )
        
        i = 0
        for octet in octets:
            i = i + 1
            
            # Vérifier que l'octet contient uniquement des chiffres
            if not octet.isdigit():
                raise ValueError(
                    f"Octet {i} invalide: '{octet}' doit etre un nombre"
                )
            
            # Vérifier la plage 0-255
            valeur = int(octet)
            if valeur < 0 or valeur > 255:
                raise ValueError(
                    f"Octet {i} invalide: {valeur} (doit etre entre 0 et 255)"
                )
    

