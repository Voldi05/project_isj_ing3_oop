import os
import equipements
import moniteur
import topologie
import securite
import paquets

# Menu principal
def menu():
    print("*"*5 + " Bienvenue dans le SIMNET de réseau du groupe YAMEN" + "*"*5)
    print("1- Equipements et liens")
    print("2- Affichage de la topologie")
    print("3- Envoi de paquets et visualisation")
    print("4- Journal du firewall")
    print("5- Rapport et statistiques")
    print("6- Quitter")

# Déclaration des variables globales de la simulation
Continue = True                       
Topo = topologie.Topologie()          
monitor = moniteur.moniteur()         
simul = paquets.Simulateur(Topo, monitor) 

while Continue:
    os.system("cls" if os.name == "nt" else "clear")
    menu()
    
    while True:
        try:
            choix = int(input("Faites un choix s'il-vous-plaît: "))
            break
        except ValueError:
            print("Erreur : Veuillez entrer un chiffre valide entre 1 et 6.")
            
    os.system("cls" if os.name == "nt" else "clear")
    
    if choix == 1:
        print("Dans cette rubrique, vous pourrez ajouter/supprimer des liens ou des équipements")
        print("1- Ajouter un équipement")
        print("2- Ajouter un lien")
        print("3- Supprimer un équipement")
        print("4- Supprimer un lien")
        
        while True:
            try:
                ch1 = int(input("Que souhaitez-vous faire ? "))
                break
            except ValueError:
                print("Erreur : Veuillez entrer un chiffre valide.")
                
        os.system("cls" if os.name == "nt" else "clear")
        
        if ch1 == 1: 
            print("1- Switch")
            print("2- Routeur")
            print("3- Parefeu")
            print("4- Point d'accès")
            print("5- Terminal")
            print("6- Serveur")
            
            while True:
                try:
                    ch11 = int(input("Quel équipement souhaitez-vous ajouter ? (choix 1 à 6) : "))
                    break
                except ValueError:
                    print("Erreur : Veuillez entrer un chiffre entre 1 et 6.")
                    
            os.system("cls" if os.name == "nt" else "clear")
            
            while True:
                nom = input("Entrer le nom de l'équipement: ").strip()
                if nom: break  
                print("Erreur : Veuillez entrer un nom valide.")
            
            while True:
                marque = input("Entrer la marque de l'équipement: ").strip()
                if marque: break  
                print("Erreur : Veuillez entrer une marque valide.")
            
            while True:
                adresse_str = input("Entrer l'adresse IP de l'équipement: ")
                try:
                    adresse = equipements.AdresseIP(adresse_str)
                    break  
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
            
            while True:
                nb_int_str = input("Entrer le nombre d'interfaces: ")
                if nb_int_str.isdigit():
                    nb_int = int(nb_int_str)
                    break  
                print("Erreur : Veuillez entrer un nombre entier valide.")
            
            if ch11 == 1:
                Eq = equipements.Switch(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq)
            elif ch11 == 2:
                Eq = equipements.Routeur(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq)
            elif ch11 == 3:
                Eq = equipements.Firewall(nom, marque, adresse, nb_int)
                if not hasattr(Eq, 'journal'):
                    Eq.journal = []
                Topo.ajouter_equipement(Eq)
            elif ch11 == 4:
                while True:
                    ss_id = input("Quel est le SSID du point d'accès: ").strip()
                    if ss_id: break  
                    print("Erreur : Veuillez entrer un SSID valide.")
                Eq = equipements.PointAccesWiFi(nom, marque, adresse, nb_int, ss_id)
                Topo.ajouter_equipement(Eq)
            elif ch11 == 5:
                Eq = equipements.TerminalClient(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq)
            elif ch11 == 6:
                Eq = equipements.Serveur(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq)
            else:
                print("Choix d'équipement indisponible !")
                os.system("pause")
                
        elif ch1 == 2: 
            while True:
                ad_eq1 = input("Entrer l'adresse IP du premier équipement: ")
                try:
                    ad_eq1 = equipements.AdresseIP(ad_eq1)
                    break  
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
                    
            while True:
                ad_eq2 = input("Entrer l'adresse IP du deuxième équipement: ")
                try:
                    ad_eq2 = equipements.AdresseIP(ad_eq2)
                    break  
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
                    
            equip1 = Topo.trouver_equipement(ad_eq1.ip)
            equip2 = Topo.trouver_equipement(ad_eq2.ip)
            
            if equip1 is None or equip2 is None:
                print("L'un des équipements entrés n'existe pas ! Impossible de créer un lien.")
            else:
                try:
                    bp = float(input("Entrer la bande passante (en Mbps) : "))
                    latence = float(input("Entrer la latence (en ms) : "))
                    Topo.ajouter_lien(equip1, equip2, bp, latence)
                    print("Lien ajouté avec succès entre les deux équipements.")
                except ValueError:
                    print("Erreur : La bande passante et la latence doivent être des nombres.")
            os.system("pause")
            
        elif ch1 == 3: 
            adresse_str = input("Donner l'adresse IP de l'équipement à supprimer : ")
            equip = Topo.trouver_equipement(adresse_str)
            if isinstance(equip, equipements.Equipement):
                Topo.supprimer_equipement(equip)
                print("Équipement supprimé de la topologie.")
            else:
                print("Il ne s'agit pas d'un équipement valide ou il n'existe pas.")
            os.system("pause")
            
        elif ch1 == 4: 
            while True:
                ad_eq1 = input("Entrer l'adresse IP du premier équipement: ")
                try:
                    ad_eq1 = equipements.AdresseIP(ad_eq1)
                    break  
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
                    
            while True:
                ad_eq2 = input("Entrer l'adresse IP du deuxième équipement: ")
                try:
                    ad_eq2 = equipements.AdresseIP(ad_eq2)
                    break  
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
                    
            equip1 = Topo.trouver_equipement(ad_eq1.ip)
            equip2 = Topo.trouver_equipement(ad_eq2.ip)
            
            if equip1 is None or equip2 is None:
                print("L'un des équipements entrés n'existe pas ! Le lien n'existe pas.")
            else:
                link = Topo.trouver_liens_equipement(equip1)
                lien_supprime = False
                for l in link:
                    if isinstance(l, topologie.Lien) and l.autre_extremite(equip1) == equip2:
                        Topo.supprimer_lien(l)
                        lien_supprime = True
                        print("Le lien a été supprimé avec succès.")
                        break
                if not lien_supprime:
                    print("Aucun lien direct n'existe entre ces deux équipements.")
            os.system("pause")
        else:
            print("Choix invalide !")
            os.system("pause")

    elif choix == 2: 
        print("Dans cette rubrique, vous aurez un aperçu de la topologie")
        Topo.afficher_topologie()
        os.system("pause")
        
    elif choix == 3: 
        print("Dans cette rubrique, vous pourrez envoyer des paquets et visualiser leur parcours")
        while True:
            ad_eq1 = input("Entrer l'adresse IP source: ")
            try:
                ad_eq1 = equipements.AdresseIP(ad_eq1)
                break  
            except ValueError as e:
                print(f"Erreur : {e}. Veuillez réessayer.")
                
        while True:
            ad_eq2 = input("Entrer l'adresse IP de destination: ")
            try:
                ad_eq2 = equipements.AdresseIP(ad_eq2)
                break  
            except ValueError as e:
                print(f"Erreur : {e}. Veuillez réessayer.")
                
        while True:
            protoc = input("Quel protocole souhaitez-vous utiliser ? (ICMP, UDP, TCP): ").strip().upper()       
            if protoc in ['ICMP', 'UDP', 'TCP']:
                break
            print("Erreur : Veuillez écrire explicitement ICMP, UDP ou TCP.")

        size = 0
        while True:
            size_str = input("Entrer la taille du paquet (entier positif): ").strip()
            try:
                size = int(size_str)
                if size > 0: break
                print("Erreur : la taille doit être un entier supérieur à 0.")
            except ValueError:
                print("Erreur : veuillez entrer un entier valide.")
        
        priority = 3
        while True:
            print("Priorité du paquet :")
            print("1- Très Haute/Critique\n2- Haute\n3- Moyenne\n4- Basse\n5- Très basse")
            priority_str = input("Entrer le chiffre de priorité (1 à 5): ").strip()
            if priority_str.isdigit() and priority_str in ['1', '2', '3', '4', '5']:
                priority = int(priority_str)
                break
            print("Erreur : Saisie invalide.")
        
        packet = paquets.Paquet(ad_eq1, ad_eq2, protoc, size, priority)
        if isinstance(packet, paquets.Paquet):
            simul.envoyer_paquet(packet)
        else:
            print("Pas de paquet disponible !")
        os.system("pause")
        
    elif choix == 4: 
        print("*"*5 + " JOURNAL D'ACTIVITÉ DES PARE-FEUX " + "*"*5)
        
        firewalls = [eq for eq in Topo.equipements if eq.__class__.__name__ in ["Firewall", "Parefeu"]]
        
        if not firewalls:
            print("\nAucun pare-feu n'est actuellement déployé dans la topologie.")
        else:
            for fw in firewalls:
                ip_affiche = "Inconnue"
                for attr_name in ['adresse', 'adresse_ip', '_adresse', 'ip']:
                    if hasattr(fw, attr_name):
                        attr = getattr(fw, attr_name)
                        ip_affiche = getattr(attr, 'ip', str(attr))
                        break
                
                print(f"\n--- Registre de sécurité pour : {fw.nom} [{ip_affiche}] ---")
                
                if not hasattr(fw, 'journal'):
                    fw.journal = []
                    
                if not fw.journal:
                    print("Aucun trafic inspecté pour le moment (Journal vide).")
                else:
                    for log in fw.journal:
                        print(log)
                        
        print("\n" + "-"*45)
        os.system("pause")
        
    elif choix == 5: 
        print("Dans cette rubrique, vous aurez la possibilité de générer un rapport.")
        if not isinstance(Topo, topologie.Topologie):
            print("La topologie n'existe pas.")
        else:
            monitor.generer_rapport(Topo)
        os.system("pause")
        
    elif choix == 6: 
        print("Au revoir et à bientôt !!!")
        Continue = False
        os.system("pause")
        
    else: 
        print("Les choix disponibles vont de 1 jusqu'à 6")
        os.system("pause")