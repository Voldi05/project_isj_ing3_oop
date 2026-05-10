from datetime import datetime
from collections import deque

class moniteur:
    """gerer la surveillance du reseau , collecter les statistiques et generer le rapport d'exploitation"""
    def __init__(self):

        self.historique_paquet=deque(maxlen=10)  # Historique des 10 derniers paquets
        #statistiques des equipements  
        self.stat_equipement={}  # un dictionnaire pour enregsitrer les paquets envoyes et perdu par chaque equipement exple {'sw1':{'transmis':0,'perdu':0},'sw2':{'transmis':0,'perdu':0}}
        #donnees pour le taux d'usge des liens
        self.trafic_liens = {}  # Format : {'Lien_A_B': total_octets_transmis}

    def collecter_statistiques(self,paquet,equipemtent,sucess=True):
        """cette methode est appele  par le module 2 a chaque fois qu'un paquet passe par un equipement , elle enregistre les details du paquet et met a jour les statistiques de l'equipement"""
        #on met a jour l'historique des paquets
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_paquet=f"[{date}] {paquet.protocole} de {paquet.source} a {paquet.destination} de taille {paquet.taille} octets"
        self.historique_paquet.append(info_paquet)

        #on met a jour les statistiques de l'equipement
        nom=equipement.nom
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
        with open("rapport_simnet.txt","w",encoding="utf-8") as f:
            f.write("Rapport d'exploitation SIMNET\n")
            f.write("fDate:{datetime.now()}\n\n")

            #etat des equipements
            f.write("Statut des équipements:\n")
            for eq in topologie.equipements:
                f.write(f"Equipement:{eq.nom}| statut:{eq.statut}\n")
            
            #historique de trafic
            f.write("\nHistorique de trafic:\n")
            for nom , data in self.stat_equipement.items():
                f.write(f"{nom}:{data['transmis']} transmis, {data['perdu']} perdu\n")

            #ajouter les details du trafic sur les liens
            f.write("\nTrafic sur les liens:\n")
            for lien in topologie.liens:
               nom=f"{lien.equipement1.nom}_{lien.equipement2.nom}"
               octet_totaux=self.trafic_liens.get(nom,0)
               #usage=(bit_transmis/capacit_bit) *100
               bit_transmis=octet_totaux*8
               capacite_bit=lien.capacite*1e6  # convertir Mbps en bps
               f.write(f"lien{nom}:{usage:.2f}% (bande passante utilisée: {lien.bande_passante_utilisee} Mbps)\n")

               
            #historque 10 derniers paquets
            f.write("\nHistorique des derniers paquets:\n")
            for p in self.historique_paquet:
                f.write(f"{p}\n")
            

                