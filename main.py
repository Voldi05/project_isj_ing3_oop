import os
import equipements
import moniteur
import topologie
import securite
import paquets

#menu principal (bon le premier menu)
def menu():
    print("*"*5 + " Bienvenue dans le simulateur de réseau du groupe YAMEN" + "*"*5)
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
                continue11=True #pour gérer la boucle d'en bas
                nom=input("Entrer le nom du switch: ")
                marque=input("Enter la marque du switch: ")
                adresse=input("Entrer l'adresse du switch: ")
                # pour gérer le cas où quelqu'un entre une adresse IP invalide, on peut faire une boucle qui continue tant que l'adresse n'est pas valide
                # while continue11:
                #     try:
                #         adresse=equipements.AdresseIP(adresse) #pour vérifier la validité de l'adresse IP
                #         continue11=False
                #     except ValueError as e:
                #         print(f"✗ {adresse} → ERREUR INATTENDUE : {e}")
                
                #il faut gérer le fait que nb_int doit etre un digit
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                Eq_Switch=equipements.Switch(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Switch)
                
            elif ch11==2: #ajout d'un routeur
                nom=input("Entrer le nom du routeur: ")
                marque=input("Enter la marque du routeur: ")
                adresse=input("Entrer l'adresse du routeur: ")
                #il faut gérer le fait que nb_int doit etre un digit
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                Eq_Routeur=equipements.Routeur(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Routeur)
                
            elif ch11==3: #ajout d'un parefeu
                nom=input("Entrer le nom du parefeu: ")
                marque=input("Enter la marque du parefeu: ")
                adresse=input("Entrer l'adresse du parefeu: ")
                
                #il faut gérer le fait que nb_int doit etre un digit
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                Eq_parefeu=equipements.Firewall(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_parefeu)
                
            elif ch11==4: #ajout d'un point d'accès
                nom=input("Entrer le nom du point d'accès: ")
                marque=input("Enter la marque du point d'accès: ")
                adresse=input("Entrer l'adresse du point d'accès: ")
                #il faut gérer le fait que nb_int doit etre un digit
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                ss_id=input("Quel est le ssid du point d'accès: ")
                Eq_AP=equipements.PointAccesWiFi(nom, marque, adresse, nb_int, ss_id)
                Topo.ajouter_equipement(Eq_AP)

            elif ch11==5: #ajout d'un terminal
                nom=input("Entrer le nom du terminal: ")
                marque=input("Enter la marque du terminal: ")
                adresse=input("Entrer l'adresse du terminal: ")
                #il faut gérer le fait que nb_int doit etre un digit
                nb_int=int(input("Entrer le nombre d'interfaces du terminal: "))
                Eq_Terminal=equipements.TerminalClient(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Terminal)

            elif ch11==6: #ajour d'un serveur
                nom=input("Entrer le nom du serveur: ")
                marque=input("Enter la marque du serveur: ")
                adresse=input("Entrer l'adresse du serveur: ")
                #il faut gérer le fait que nb_int doit etre un digit
                nb_int=int(input("Entrer le nombre d'interfaces du serveur: "))
                Eq_Serveur=equipements.Serveur(nom, marque, adresse, nb_int)
                Topo.ajouter_equipement(Eq_Serveur)
            else:
                print("Choix indisponible !")
                os.system("pause")
                
        elif ch1==2: # ajout d'un lien
            ad_eq1=input("Entrer l'adresse IP du premier équipement: ")
            ad_eq2=input("Entrer l'adresse IP du deuxième équipement: ")
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
            ad_eq1=input("Entrer l'adresse IP du premier équipement: ")
            ad_eq2=input("Entrer l'adresse IP du deuxième équipement: ")
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
        adresse=input("Avec qui souhaitez-vous communiquer ?")
        #apès j'appelle la focntion d'envoi des paquets avec toutes les vérifcations utiles: validité de l'adresse IP, si elle appartient à un hote du réseau, publique ou privée
        os.system("pause")
        
    elif choix==4: #journal du firewall
        print("Dans cette rubrique, le journal du parefeu sera affiché")
        #
        os.system("pause")
        
    elif choix==5: #rapport et stats
        print("Dans cette rubrique, aurez la possibilité de générer un rapport texte, dans lequel seront présentées les statistiques ")
        monitor.generer_rapport(Topo)
        os.system("pause")
        
    elif choix==6: #quitter
        print("Aurevoir et à bientôt !!!")
        Continue=False
        os.system("pause")
        
    else: 
        print("Les choix disponibles vont de 1 jusqu'à 6")
        os.system("pause")
