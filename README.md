# SIMNet — Simulateur de Réseau Intelligent

> Projet de groupe — Programmation Orientée Objet en Python
> **INGÉNIEUR 3 SRT** · Institut Saint Jean · Année académique 2025-2026

---

## Description

Ce dépôt est le point de départ officiel du projet **SIMNet**, donné aux étudiants
de 3ème année Génie Télécom & Réseaux dans le cadre du cours de Programmation Orientée
Objet en Python.

**SIMNet** est un simulateur de réseau d'entreprise entièrement orienté objet. Il permet
de modéliser une topologie réseau, de faire circuler des paquets entre équipements,
d'en assurer la sécurité via un firewall, et d'en superviser le fonctionnement grâce
à un moniteur réseau.

---

## Structure attendue du projet

Chaque groupe doit organiser son code selon la structure suivante :

```
project_isj_ing3_oop/
│
├── src/
│   ├── equipements.py      # Classes des équipements réseau
│   ├── topologie.py        # Topologie et liens
│   ├── paquets.py          # Paquet et simulation de trafic
│   ├── securite.py         # Firewall, règles, journal
│   ├── moniteur.py         # Moniteur réseau et rapports
│   └── main.py             # Point d'entrée et menu interactif
│
├── rapport.pdf             # Rapport technique du groupe
└── README.md               # Ce fichier (à compléter par le groupe)
```


## EXPLCATION DU LANCEMENT DE L'APPLICATION

Bienvenue dans le dépôt de notre projet de POO, celui du groupe YAMEN. 
Suivez les instructions ci-dessous pour installer et lancer le projet sur votre machine locale.

# Étape 1 : Cloner le dépôt
Ouvrez votre terminal (Git Bash, Terminal de commandes, etc.).
Copiez et collez la commande suivante pour cloner le projet :
git clone https://github.com/Voldi05/project_isj_ing3_oop.git

# Étape 2 : Ouvrir le projet
Lancez votre éditeur de code favori (VS Code, PyCharm, etc.).
Allez dans File > Open Folder (Fichier > Ouvrir le dossier).
Sélectionnez le dossier project_isj_ing3_oop que vous venez de cloner.

# Étape 3 : Lancer l'application
Une fois le projet ouvert dans votre éditeur :
Naviguez vers le dossier src/.
Ouvrez le fichier main.py.
Lancez l'exécution du script.

## DESCRIPTION DES FONCTIONNALITES IMPLEMENTEES

# 1- Création des "équipements", gestion de la topologie: 
    Nous avons crééune classe AdresseIP qui définit notre type adresse en gérant la validité de celle-ci (nombre d'octets, privée ou publique).

    Nous sommes allés sur la base d'une classe abstraite nommée Equipement à partir de laquelle sont nées d'autres classe filles: Switch, Routeur, Parefeu, Serveur, Terminal(qui fait référence au client), Serveur. Chacune de ses classes filles devra obligatoirement hériter des méthodes de leur classe mère Equuipement.
    
# 2- Visualisation des paquets 
    Pour ce cas, deux classes sont crées: Paquet et Simulateur.
    La classe Paquet permet d'identifeir les paquets (les messages) qui transitent dans le réseau. La classe Simulateur permet d'avoir un état sur la transmission des paquets. Ce module est utile pour créer des paquets réseau réalistes avec validation stricte et simuler leur transmission dans une topologie réseau

# 3- Sécurité
    Le parefeu est comme le gardien de notre réseau. C'est lui qui décide de qui entre ou pas, qui envoie quoi à qui ou pas. Et pour cela, il a besoin de règles et à cet effet nous avons créé une classe Regle qui gère ces cas de figures. 

# 4- Rapport et statistiques
    Sous un format accessible qu'est le texte, il sera possible d'avoir sous la main les informations de notre topologie si elle existe. Pour cela, nous avons ecrit une foncion generer_rapport

# 5- Menu principal
    Nous avons fourni un menu principal simple à l'usage et intuitf. dans ce menu, 
    nous avons géré autant que possible les exceptions au niveau des erreur ssur les types, les valeurs. Pour le moment, nous n'avons pas concevoir une interface graphique mais cela fait partie d'une des améliorations futures. Nous l'implémenterons avec les modules python customTkinter et tkinter. 

## NOMS DES MEMBRES DU GROUPE 5 (YAMEN)
   - FOTSO ERYANGE VERDIANE
   - NJOYA ARIEL RYAN
   - SEUMO YANN BERTRAND
   - NTANDZI CLAUDE MANUELLA
   - NINKAM NOEMIE

# Soutenez-nous !
Si vous appréciez ce travail ou s'il vous a été utile, n'hésitez pas à :
Laisser une Star (un like) sur ce dépôt GitHub.
Suivre notre profil pour rester informé de nos prochains projets !