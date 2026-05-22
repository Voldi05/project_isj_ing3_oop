import os
import equipements
import moniteur
import topologie
import securite
import paquets

#menu principal (bon le premier menu)
def menu():
    print("*"*5 + " Bienvenue dans le  SIMNET de réseau du groupe YAMEN" + "*"*5)
    print("1- Equipements et liens")
    print("2- Affichage de la topologie")
    print("3- Envoi de paquets et visualisation")
    print("4- Journal du firewall")
    print("5- Rapport et statistiques")
    print("6- Quitter")

#déclaration de variables
Continue=True #qui va permettre de gérer l'arret
Topo=topologie.Topologie() #définition de notre topologie
monitor=moniteur.moniteur() #definition d'un moniteur qui servira à afficher le rapport
simul=paquets.Simulateur(Topo, monitor) #définition du simulateur

while (Continue):
    os.system("cls")
    menu()
    choix = int(input("Faites un choix s'il-vous-plaît: "))
    # pour gérer le cas où quelqu'un entre une lettre à la place d'un chiffre
    # if not choix.isdigit():
    #     print("Le choix est un chiffre")
    # else:
    os.system("cls")
    
    if choix == 1:
        print("Dans cette rubrique, vous pourrez ajouter/supprimer des liens ou des des équipements")
        print("1- Ajouter un équipement")
        print("2- Ajouter un lien")
        print("3- Supprimer un équipement")
        print("4- Supprimer un lien")
        ch1=int(input("Que souhaitez-vous faire ? "))
        os.system("cls")
        if ch1==1: #ajout d'un équipement
            print("1- Switch")
            print("2- Routeur")
            print("3- Parefeu")
            print("4- Point d'accès")
            print("5- Terminal")
            print("6- Serveur")
            ch11=int(input("Quel équipement souhaitez-vous ajouter ? (faites un choix situé entre 1 et 4)"))
            os.system("cls")
            if ch11==1: #ajout d'un switch
                #pour le nom
                while True:
                    nom=input("Entrer le nom du switch: ")
                    nom=nom.strip() #pour enlever les espaces au début et à la fin du nom
                    if nom:    
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nom valide.")
                
                #pour la marque
                while True:
                    marque=input("Enter la marque du switch: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if marque:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                #pour l'adresse
                while True:
                    adresse = input("Entrer l'adresse du switch: ")
                    try:
                        adresse = equipements.AdresseIP(adresse) # Vérification via ta classe
                        break  # On sort de la boucle si aucune erreur n'est levée
                    except ValueError as e:
                        print(f"Erreur : {e}. Veuillez réessayer.")
                
                #il faut gérer le fait que nb_int doit etre un digit
                while True:
                    nb_int_str = input("Entrer le nombre d'interfaces: ")
                    if nb_int_str.isdigit():
                        nb_int = int(nb_int_str)
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nombre entier valide.")
            
                Eq_Switch=equipements.Switch(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Switch)
                
            elif ch11==2: #ajout d'un routeur
                #pour le nom
                while True:
                    nom=input("Entrer le nom du routeur: ")
                    nom=nom.strip() #pour enlever les espaces au début et à la fin du nom
                    if nom:    
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nom valide.")
                
                #pour la marque
                while True:
                    marque=input("Enter la marque du routeur: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if marque:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                #pour l'adresse
                while True:
                    adresse = input("Entrer l'adresse du routeur: ")
                    try:
                        adresse = equipements.AdresseIP(adresse) # Vérification via ta classe
                        break  # On sort de la boucle si aucune erreur n'est levée
                    except ValueError as e:
                        print(f"Erreur : {e}. Veuillez réessayer.")
                
                #il faut gérer le fait que nb_int doit etre un digit
                while True:
                    nb_int_str = input("Entrer le nombre d'interfaces: ")
                    if nb_int_str.isdigit():
                        nb_int = int(nb_int_str)
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nombre entier valide.")
                 
                Eq_Routeur=equipements.Routeur(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Routeur)
                
            elif ch11==3: #ajout d'un parefeu
                #pour le nom
                while True:
                    nom=input("Entrer le nom du parefeu: ")
                    nom=nom.strip() #pour enlever les espaces au début et à la fin du nom
                    if nom:    
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nom valide.")
                
                #pour la marque
                while True:
                    marque=input("Entrer la marque du parefeu: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if marque:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                #pour l'adresse
                while True:
                    adresse = input("Entrer l'adresse du parefeu: ")
                    try:
                        adresse = equipements.AdresseIP(adresse) # Vérification via ta classe
                        break  # On sort de la boucle si aucune erreur n'est levée
                    except ValueError as e:
                        print(f"Erreur : {e}. Veuillez réessayer.")
                
                #il faut gérer le fait que nb_int doit etre un digit
                while True:
                    nb_int_str = input("Entrer le nombre d'interfaces: ")
                    if nb_int_str.isdigit():
                        nb_int = int(nb_int_str)
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nombre entier valide.")    
                
                
                Eq_parefeu=equipements.Firewall(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_parefeu)
                
            elif ch11==4: #ajout d'un point d'accès
                #pour le nom
                while True:
                    nom=input("Entrer le nom du point d'accès: ")
                    nom=nom.strip() #pour enlever les espaces au début et à la fin du nom
                    if nom:    
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nom valide.")
                
                #pour la marque
                while True:
                    marque=input("Entrer le marque du point d'accès: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if marque:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                #pour l'adresse
                while True:
                    adresse = input("Entrer l'adresse du point d'accès: ")
                    try:
                        adresse = equipements.AdresseIP(adresse) # Vérification via ta classe
                        break  # On sort de la boucle si aucune erreur n'est levée
                    except ValueError as e:
                        print(f"Erreur : {e}. Veuillez réessayer.")
                
                #il faut gérer le fait que nb_int doit etre un digit
                while True:
                    nb_int_str = input("Entrer le nombre d'interfaces: ")
                    if nb_int_str.isdigit():
                        nb_int = int(nb_int_str)
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nombre entier valide.")
                
                while True:
                    ss_id=input("Quel est le ssid du point d'accès: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if ss_id:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                Eq_AP=equipements.PointAccesWiFi(nom, marque, adresse, nb_int, ss_id)
                Topo.ajouter_equipement(Eq_AP)

            elif ch11==5: #ajout d'un terminal
                while True:
                    nom=input("Entrer le nom du terminal: ")
                    nom=nom.strip() #pour enlever les espaces au début et à la fin du nom
                    if nom:    
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nom valide.")
                
                #pour la marque
                while True:
                    marque=input("Entrer le marque du terminal: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if marque:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                #pour l'adresse
                while True:
                    adresse = input("Entrer l'adresse du terminal: ")
                    try:
                        adresse = equipements.AdresseIP(adresse) # Vérification via ta classe
                        break  # On sort de la boucle si aucune erreur n'est levée
                    except ValueError as e:
                        print(f"Erreur : {e}. Veuillez réessayer.")
                
                #il faut gérer le fait que nb_int doit etre un digit
                while True:
                    nb_int_str = input("Entrer le nombre d'interfaces: ")
                    if nb_int_str.isdigit():
                        nb_int = int(nb_int_str)
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nombre entier valide.")
                   
                Eq_Terminal=equipements.TerminalClient(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Terminal)

            elif ch11==6: #ajour d'un serveur
                
                while True:
                    nom=input("Entrer le nom du serveur: ")
                    nom=nom.strip() #pour enlever les espaces au début et à la fin du nom
                    if nom:    
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nom valide.")
                
                #pour la marque
                while True:
                    marque=input("Entrer la marque du serveur: ")
                    marque=marque.strip() #pour enlever les espaces au début et à la fin du nom
                    if marque:    
                        break  
                    else:
                        print("Erreur : Veuillez entrer une marque valide.")
                
                #pour l'adresse
                while True:
                    adresse = input("Entrer l'adresse du serveur: ")
                    try:
                        adresse = equipements.AdresseIP(adresse) # Vérification via ta classe
                        break  # On sort de la boucle si aucune erreur n'est levée
                    except ValueError as e:
                        print(f"Erreur : {e}. Veuillez réessayer.")
                
                #il faut gérer le fait que nb_int doit etre un digit
                while True:
                    nb_int_str = input("Entrer le nombre d'interfaces: ")
                    if nb_int_str.isdigit():
                        nb_int = int(nb_int_str)
                        break  # On sort si la conversion en entier est possible
                    else:
                        print("Erreur : Veuillez entrer un nombre entier valide.")
                
                Eq_Serveur=equipements.Serveur(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Serveur)
            else:
                print("Choix indisponible !")
                os.system("pause")
                
        elif ch1==2: # ajout d'un lien #verifier l'adresse
            while True:
                ad_eq1 = input("Entrer l'adresse IP du premier équipement: ")
                try:
                    ad_eq1 = equipements.AdresseIP(ad_eq1) # Vérification via ta classe
                    break  # On sort de la boucle si aucune erreur n'est levée
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
            while True:
                ad_eq2 = input("Entrer l'adresse IP du deuxième équipement: ")
                try:
                    ad_eq2= equipements.AdresseIP(ad_eq2) # Vérification via ta classe
                    break  # On sort de la boucle si aucune erreur n'est levée
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
            equip1=Topo.trouver_equipement(ad_eq1)
            equip2=Topo.trouver_equipement(ad_eq2)
            if equip1==None or equip2==None:
                print("L'un des équipements que vous avez entré n'existe pas ! Impossible de créer un lien ! ")
            else:
                bp=float (input("Entrer la bande passante: "))
                latence=float (input("Entrer la latence: "))
                link=topologie.Lien(equip1, equip2, bp, latence)
                Topo.ajouter_lien(equip1, equip2, bp, latence)
            os.system("pause")
            
        elif ch1==3: # suppression d'un équipement
            adresse=input("Donner l'adresse IP de l'équipement: ")
            equip=Topo.trouver_equipement(adresse)
            if isinstance(equip, equipements.Equipement):
                Topo.supprimer_equipement(equip)
            else:
                print("Il ne s'agit pas d'un équipement")
            os.system("pause")
            
        elif ch1==4: #suppression d'un lien
            while True:
                ad_eq1 = input("Entrer l'adresse IP du premier équipement: ")
                try:
                    ad_eq1 = equipements.AdresseIP(ad_eq1) # Vérification via ta classe
                    break  # On sort de la boucle si aucune erreur n'est levée
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
            while True:
                ad_eq2 = input("Entrer l'adresse IP du deuxième équipement: ")
                try:
                    ad_eq2= equipements.AdresseIP(ad_eq2) # Vérification via ta classe
                    break  # On sort de la boucle si aucune erreur n'est levée
                except ValueError as e:
                    print(f"Erreur : {e}. Veuillez réessayer.")
            equip1=Topo.trouver_equipement(ad_eq1)
            equip2=Topo.trouver_equipement(ad_eq2)
            if equip1==None or equip2==None:
                print("L'un des équipements que vous avez entré n'existe pas ! Le lien n'existe pas ! ")
            else:
                link=Topo.trouver_liens_equipement(equip1)
                for l in link:
                    if isinstance(l, topologie.Lien) and l.autre_extremite(equip1)==equip2:
                        Topo.supprimer_lien(l)                 
            
            os.system("pause")
        else:
            print("Choix invalide !")
            os.system("pause")

    elif choix==2: #afficher la topologie
        print("Dans cette rubrique, vous aurez un aperçu de la topolgie")
        Topo.afficher_topologie()
        os.system("pause")
        
    elif choix==3: #envoi des paquets et vsiualisation de leur parcours, on va utiliser le fichier paquets.py
        print("Dans cette rubrique, vous pourrez envoyer des paquets et visualiser leur parcours")
        #on se rassure toujours que l'adresse du premier équipement a le bon format
        while True:
            ad_eq1 = input("Entrer l'adresse IP du premier équipement: ")
            try:
                ad_eq1 = equipements.AdresseIP(ad_eq1) # Vérification via ta classe
                break  # On sort de la boucle si aucune erreur n'est levée
            except ValueError as e:
                print(f"Erreur : {e}. Veuillez réessayer.")
        #on se rassure toujours que l'adresse du deuxièmeéquipement a le bon format
        while True:
            ad_eq2 = input("Entrer l'adresse IP du deuxième équipement: ")
            try:
                ad_eq2= equipements.AdresseIP(ad_eq2) # Vérification via ta classe
                break  # On sort de la boucle si aucune erreur n'est levée
            except ValueError as e:
                print(f"Erreur : {e}. Veuillez réessayer.")
         #protocole     
        while True:
            protoc = input("Quel protocole souhaitez-vous utiliser ? (ICMP, UDP, TCP): ").strip().upper()       
            if protoc in ['ICMP', 'UDP', 'TCP']:
                break
            print("Erreur : Veuillez écrire explicitement ICMP, UDP ou TCP (pas de chiffre).")

            
        size=float(input("Entrer la taille du paquet: ")) #verification à faire, positivité
        
        while True:
            print("Priorité du paquet :")
            print("1- Très Haute/Critique")
            print("2- Haute")
            print("3- Moyenne")
            print("4- Basse")
            print("5- Très basse")
            
            priority_str = input("Entrer le chiffre de priorité (1, 2, 3, 4 ou 5): ").strip()
            if priority_str.isdigit() and priority_str in ['1', '2', '3', '4', '5']:
                priority = int(priority_str)
                break
            print("Erreur : Veuillez entrer un chiffre valide (1, 2, 3, 4 ou 5).")
        
        packet=paquets.Paquet(ad_eq1, ad_eq2, protoc, size, priority)
        if isinstance(packet, paquets.Paquet):
            simul.envoyer_paquet(packet)
        else:
            print("Pas de paquet disponible !")
        os.system("pause")
        
        
    elif choix==4: #journal du firewall
        print("Dans cette rubrique, le journal du parefeu sera affiché")
        #
        os.system("pause")
        
    elif choix==5: #rapport et stats
        print("Dans cette rubrique, aurez la possibilité de générer un rapport texte, dans lequel seront présentées les statistiques ")
        if not isinstance(Topo, topologie.Topologie):
            print("La topologie n'existe pas.")
        else:
            monitor.generer_rapport(Topo)
        os.system("pause")
        
    elif choix==6: #quitter
        print("Aurevoir et à bientôt !!!")
        Continue=False
        os.system("pause")
        
    else: 
        print("Les choix disponibles vont de 1 jusqu'à 6")
        os.system("pause")
