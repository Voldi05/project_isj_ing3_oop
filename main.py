import os

def menu():
    print("*"*5 + " Bienvenue dans le simulateur de réseau du groupe YAMEN" + "*"*5)
    print("1- Equipements et liens")
    print("2- Affichage de la topologie")
    print("3- Paquets")
    print("4- Générer le rapport")
    print("5- Quitter")

Continue=True #qui va permettre de gérer l'arret

while (Continue):
    os.system("cls")
    menu()
    choix = int(input("Faites un choix s'il-vous-plaît: "))
    os.system("cls")
    if choix == 1:
        print("Dans cette rubrique, vous pourrez ajouter/supprimer des liens ou des des équipements")
        print("1- Ajouter un équipement")
        print("2- Ajouter un lien")
        print("3- Supprimer un équipement")
        print("4- Supprimer un lien")
        ch1=int(input("Que soushaitez-vous faire ? "))
        os.system("cls")
        if ch1==1:
            a=0
            #j'appelle la fonction init de la classe Equipement
            #et ajouter l'équipement dans le dictionnaire des équipeemnts
            os.system("pause")
        elif ch1==2:
            a=0
            #je sais pas s'il y aura une fonction d'ajout des liens, mais je vais l'appeler
            os.system("pause")
        elif ch1==3:
            print("Donner le nom de l'équipement")
            # suffit juste de supprimer l'équipement dans le dictionnaire des équipeemnts
            os.system("pause")
        elif ch1==4:
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
