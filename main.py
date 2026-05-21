import os
import equipements
import moniteur
import topologie
import securite

def menu():
    print("*"*5 + " Bienvenue dans le simulateur de réseau du groupe YAMEN" + "*"*5)
    print("1- Equipements et liens")
    print("2- Affichage de la topologie")
    print("3- Paquets")
    print("4- Générer le rapport")
    print("5- Quitter")

Continue=True #qui va permettre de gérer l'arret
table_equip=[] #liste des equipements

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
            if ch11==1: #ajout d'un switch
                nom=input("Entrer le nom du switch: ")
                marque=input("Enter la marque du switch ")
                adresse=input("Entrer l'adresse du switch: ")
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                Eq_Switch=equipements.Switch(nom, marque, adresse, nb_int)
                # equip={"nom": nom, "marque": marque, "adresse": adresse, "nombre interfaces": nb_int, "statut": equipements.Switch.statut}
                # table_equip.append(equip)
            elif ch11==2: #ajout d'un routeur
                nom=input("Entrer le nom du routeur: ")
                marque=input("Enter la marque de l'équipement: ")
                adresse=input("Entrer l'adresse de l'équipement: ")
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                Eq_Routeur=equipements.Routeur(nom, marque, adresse, nb_int)
                # equip={"nom": nom, "marque": marque, "adresse": adresse, "nombre interfaces": nb_int, "statut": equipements.Routeur.statut}
                # table_equip.append(equip)
            elif ch11==3: #ajout d'un parefeu
                nom=input("Entrer le nom du parefeu: ")
                marque=input("Enter la marque du parefeu: ")
                adresse=input("Entrer l'adresse du parefeu: ")
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                Eq_AP=equipements.Firewall(nom, marque, adresse, nb_int)
                # equip={"nom": nom, "marque": marque, "adresse": adresse, "nombre interfaces": nb_int, "statut": equipements.Firewall.statut}
                # table_equip.append(equip)
            elif ch11==4: #ajout d'un point d'accès
                nom=input("Entrer le nom du point d'accès: ")
                marque=input("Enter la marque du point d'accès: ")
                adresse=input("Entrer l'adresse du point d'accès: ")
                nb_int=int(input("Entrer le nombre d'interfaces: "))
                ss_id=input("Quel est le ssid du point d'accès: ")
                Eq_parefeu=equipements.PointAccesWiFi(nom, marque, adresse, nb_int, ss_id)
                # equip={"nom": nom, "marque": marque, "adresse": adresse, "nombre interfaces": nb_int, "SSID":ss_id ,"statut": equipements.PointAccesWiFi.statut}
                # table_equip.append(equip)

            elif ch11==5:
                nom=input("Entrer le nom du terminal: ")
                marque=input("Enter la marque du terminal: ")
                adresse=input("Entrer l'adresse du terminal: ")
                nb_int=int(input("Entrer le nombre d'interfaces du terminal: "))
                Eq_Terminal=equipements.TerminalClient(nom, marque, adresse, nb_int)
                # equip={"nom": nom, "marque": marque, "adresse": adresse, "nombre interfaces": nb_int, "statut": equipements.TerminalClient.statut}
                # table_equip.append(equip)

            elif ch11==6:
                nom=input("Entrer le nom du serveur: ")
                marque=input("Enter la marque du serveur: ")
                adresse=input("Entrer l'adresse du serveur: ")
                nb_int=int(input("Entrer le nombre d'interfaces du serveur: "))
                Eq_Serveur=equipements.Serveur(nom, marque, adresse, nb_int)
                # equip={"nom": nom, "marque": marque, "adresse": adresse, "nombre interfaces": nb_int, "statut": equipements.Serveur.statut}
                # table_equip.append(equip)

            else:
                print("Choix indisponible !")
            
            os.system("pause")
        elif ch1==2: # ajout d'un lien
            a=0
            #je sais pas s'il y aura une fonction d'ajout des liens, mais je vais l'appeler
            os.system("pause")
        elif ch1==3: # suppression d'un équipement
            print("Donner le nom de l'équipement")
            # suffit juste de supprimer l'équipement dans le dictionnaire des équipeemnts
            os.system("pause")
        elif ch1==4: #suppression d'un lien
            a=0
            #je sais pas encore quoi choisir pour identifier le lien à supprimer
            os.system("pause")
        else:
            print("Choix invalide !")
            os.system("pause")

    elif choix==2:
        a=0
    elif choix==3:
        print("Dans cette rubrique, vous pourrez envoyer des paquets et visualiser leur parcours")
        adresse=input("Avec qui souhaitez-vous communiquer ?")
        #apès j'appelle la focntion d'envoi des paquets avec toutes les vérifcations utiles: validité de l'adresse IP, si elle appartient à un hote du réseau, publique ou privée
        os.system("pause")
    elif choix==4:
        #ici je vais appeler la fonction de génération d'un rapport qui aura été écrite dans le module 4
        os.system("pause")
    elif choix==5:
        print("Aurevoir et à bientôt !!!")
        Continue=False
        os.system("pause")
    else:
        print("Les choix disponibles vont de 1 jusqu'à 5")
        os.system("pause")
