from datetime import datetime
from collections import deque

class Moniteur:
    """gerer la surveillance du reseau , collecter les statistiques et generer le rapport d'exploitation"""
    def __init__(self):

        self.historique_paquet=deque(maxlen=10)  # Historique des 10 derniers paquets
        #statistiques des equipements  
        self.stat_equipement={}  # un dictionnaire pour enregsitrer les paquets envoyes et perdu par chaque equipement exple {'sw1':{'transmis':0,'perdu':0},'sw2':{'transmis':0,'perdu':0}}
        #donnees pour le taux d'usge des liens
        self.trafic_liens = {}  # Format : {'Lien_A_B': total_octets_transmis}

    
    def collecter_statistiques(self,paquet,Equipement,sucess=True):
        """cette methode est appele  par le module 2 a chaque fois qu'un paquet passe par un equipement , elle enregistre les details du paquet et met a jour les statistiques de l'equipement"""
        #on met a jour l'historique des paquets
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_paquet=f"[{date}] {paquet.protocole} de {paquet.source} a {paquet.destination} de taille {paquet.taille} octets"
        self.historique_paquet.append(info_paquet)

        #on met a jour les statistiques de l'equipement
        nom=Equipement.nom
        if nom not in self.stat_equipement:
            self.stat_equipement[nom]={'transmis':0,'perdu':0}
        if sucess:
            self.stat_equipement[nom]['transmis']+=1
        else:
            self.stat_equipement[nom]['perdu']+=1


    
    def collecter_trafic_lien(self,lien,paquet):
        """cette methode est appele  par le module 2 a chaque fois qu'un paquet traverse un lien , elle enregistre le trafic total sur ce lien pour calculer le taux d'usage"""
        #creer un id unique pour le lien
        id_lien=f"{lien.equipement1.nom}_{lien.equipement2.nom}"
        if id_lien not in self.trafic_liens:
            self.trafic_liens[id_lien]=0
        
        #on ajoute la taille du paquet au trafic total du lien
        self.trafic_liens[id_lien]+=paquet.taille

       
    
    def generer_rapport(self,topologie):
        """cette methode est appele a la fin de la simulation pour generer un rapport d'exploitation  rapport_simnet.txt"""
        #ouvrir le fichier en mode ecriture et enregister les details de la simulation
        try:
            with open("rapport_simnet.txt","w",encoding="utf-8") as f:
                f.write("-------Rapport d'exploitation SIMNET-----\n")
                f.write(f"Date de generation : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n")

                #etat des equipements(actif ou inactif)
                f.write("-----Statut des équipements-----:\n")
                for eq in topologie.equipements:
                    # On accède directement à l'attribut _statut initialisé dans le constructeur
                    statut_str = "ACTIF" if eq._statut else "INACTIF"
                    f.write(f"Equipement:{eq.nom:<12}| statut:{statut_str}\n")
                    
                #historique de trafic par equipement
                f.write("\n-----Historique de trafic-----\n")
                for nom , data in self.stat_equipement.items():
                    f.write(f"{nom:<12} -> Transmis : {data['transmis']:<5} | perdus: {data['perdu']}\n")

                #ajouter les details du trafic sur le taux d'utilisarion  des liens
                f.write("\n-----Taux d'usage des liens----\n")
                for lien in topologie.liens:
                    nom_lien =f"{lien.equipement1.nom}_{lien.equipement2.nom}"# nom du lien entre duex equipements
                    octet_totaux= self.trafic_liens.get(nom_lien ,0)
                    
                    #calcul du taux d'usage=(bit_transmis/capacit_bit) *100
                    bit_transmis = octet_totaux*8 
                    capacite_bit = lien.bande_passante*1e6  # convertir Mbps en bps
                    usage = (bit_transmis/capacite_bit)*100 if capacite_bit > 0 else 0
                    f.write(f"lien {nom_lien:<25}: {usage:.2f}% d'utilisation ({octet_totaux} octets transmis)\n")
                
                #historque 10 derniers paquets
                f.write("\n -----Historique des 10 derniers paquets-----\n")
                if not self.historique_paquet:
                    f.write("aucun trafic enregistre.\n")
                for p in self.historique_paquet:
                    f.write(f"{p}\n")
                
                f.write("\n-----Fin du rapport d'exploitation-----\n")
            print("Rapport d'exploitation généré: rapport_simnet.txt")
        except Exception as e:
            print(f"Erreur lors de la generation du rapport d'exploitation: {e}")       