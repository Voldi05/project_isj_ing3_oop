from datetime import datetime
from collections import deque

class moniteur:
    """Gérer la surveillance du réseau, collecter les statistiques et générer le rapport d'exploitation."""
    
    def __init__(self):
        self.historique_paquet = deque(maxlen=10)  # Historique des 10 derniers paquets
        # Statistiques des équipements  
        self.stat_equipement = {}  # Format : {'sw1': {'transmis': 0, 'perdu': 0}, 'sw2': {'transmis': 0, 'perdu': 0}}
        # Données pour le taux d'usage des liens
        self.trafic_liens = {}  # Format : {'Lien_A_B': total_octets_transmis}

    def collecter_statistiques(self, paquet, Equipement, sucess=True):
        """Cette méthode est appelée à chaque fois qu'un paquet passe par un équipement, 
        elle enregistre les détails du paquet et met à jour les statistiques de l'équipement."""
        # On met à jour l'historique des paquets
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_paquet = f"[{date}] {paquet.protocole} de {paquet.source} a {paquet.destination} de taille {paquet.taille} octets"
        self.historique_paquet.append(info_paquet)

        # On met à jour les statistiques de l'équipement
        nom = Equipement.nom
        if nom not in self.stat_equipement:
            self.stat_equipement[nom] = {'transmis': 0, 'perdu': 0}
        if sucess:
            self.stat_equipement[nom]['transmis'] += 1
        else:
            self.stat_equipement[nom]['perdu'] += 1

    def collecter_trafic_lien(self, lien, paquet):
        """Cette méthode est appelée à chaque fois qu'un paquet traverse un lien, 
        elle enregistre le trafic total sur ce lien pour calculer le taux d'usage."""
        # Créer un id unique pour le lien
        id_lien = f"{lien.equipement1.nom}_{lien.equipement2.nom}"
        if id_lien not in self.trafic_liens:
            self.trafic_liens[id_lien] = 0
        
        # On ajoute la taille du paquet au trafic total du lien
        self.trafic_liens[id_lien] += paquet.taille

    def enregistrer_envoi(self, paquet, temps_total):
        """Méthode passerelle requise par paquets.py pour archiver la fin de la simulation d'envoi."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_paquet = f"[{date}] {paquet.protocole} de {paquet.source} a {paquet.destination} de taille {paquet.taille} octets (Livre en {temps_total:.2f} ms)"
        self.historique_paquet.append(info_paquet)

    def generer_rapport(self, topologie):
        """Cette méthode est appelée à la fin de la simulation pour générer un rapport d'exploitation rapport_simnet.txt."""
        try:
            with open("rapport_simnet.txt", "w", encoding="utf-8") as f:
                f.write("-------Rapport d'exploitation SIMNET-----\n")
                f.write(f"Date de generation : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # État des équipements (actif ou inactif)
                f.write("-----Statut des équipements-----:\n")
                for eq in topologie.equipements:
                    # On accède directement à l'attribut _statut initialisé dans le constructeur
                    statut_str = "ACTIF" if eq._statut else "INACTIF"
                    f.write(f"Equipement:{eq.nom:<12}| statut:{statut_str}\n")
                    
                # Historique de trafic par équipement
                f.write("\n-----Historique de trafic-----\n")
                for nom, data in self.stat_equipement.items():
                    f.write(f"{nom:<12} -> Transmis : {data['transmis']:<5} | perdus: {data['perdu']}\n")

                # Ajouter les détails du trafic sur le taux d'utilisation des liens
                f.write("\n-----Taux d'usage des liens----\n")
                for lien in topologie.liens:
                    nom_lien = f"{lien.equipement1.nom}_{lien.equipement2.nom}"  # nom du lien entre deux équipements
                    octet_totaux = self.trafic_liens.get(nom_lien, 0)
                    
                    # Calcul du taux d'usage = (bit_transmis / capacite_bit) * 100
                    bit_transmis = octet_totaux * 8 
                    capacite_bit = lien.bande_passante * 1e6  # convertir Mbps en bps
                    usage = (bit_transmis / capacite_bit) * 100 if capacite_bit > 0 else 0
                    f.write(f"lien {nom_lien:<25}: {usage:.2f}% d'utilisation ({octet_totaux} octets transmis)\n")
                
                # Historique 10 derniers paquets
                f.write("\n -----Historique des 10 derniers paquets-----\n")
                if not self.historique_paquet:
                    f.write("aucun trafic enregistre.\n")
                for p in self.historique_paquet:
                    f.write(f"{p}\n")
                
                f.write("\n-----Fin du rapport d'exploitation-----\n")
            print("Rapport d'exploitation généré: rapport_simnet.txt")
        except Exception as e:
            print(f"Erreur lors de la generation du rapport d'exploitation: {e}")