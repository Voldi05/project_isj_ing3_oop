"""
paquets.py — Paquets réseau et simulation de trafic pour SIMNet.
"""

from datetime import datetime
from equipements import AdresseIP

PROTOCOLES_VALIDES = ("TCP", "UDP", "ICMP")

class Paquet:
    """Représente un paquet réseau circulant entre deux équipements."""

    _compteur = 0  # Identifiant unique auto-incrémenté

    def __init__(self, source: str, destination: str, 
                 protocole: str, taille: int, priorite: int):
        
        # Validation des adresses via la classe AdresseIP du module equipement
        self._source = source
        self._destination = destination

        # Validation du protocole
        if protocole not in PROTOCOLES_VALIDES:
            raise ValueError(f"Protocole invalide : {protocole}")
        self._protocole = protocole

        # Validation de la taille
        if not isinstance(taille, int) or taille <= 0:
            raise ValueError("La taille doit être un entier positif")
        self._taille = taille

        # Validation de la priorité
        if not isinstance(priorite, int) or not (1 <= priorite <= 5):
            raise ValueError("La priorité doit être comprise entre 1 et 5")
        self._priorite = priorite

        # Métadonnées
        Paquet._compteur += 1
        self._id = Paquet._compteur
        self._horodatage = datetime.now()

    @property
    def source(self) -> str:
        return self._source.ip

    @property
    def destination(self) -> str:
        return self._destination.ip

    @property
    def protocole(self) -> str:
        return self._protocole

    @property
    def taille(self) -> int:
        return self._taille

    def __str__(self) -> str:
        return (f"Paquet#{self._id} [{self._protocole}] "
                f"{self.source} -> {self.destination} "
                f"({self._taille} octets)")


class Simulateur:
    """Gère la simulation de trafic et l'acheminement."""

    def __init__(self, topologie, moniteur):
        self._topologie = topologie
        self._moniteur = moniteur
        self._historique = []

    def envoyer_paquet(self, paquet: Paquet) -> bool:
        print(f"\n--- Simulation d'envoi du paquet {paquet._id} ---")
        
        # Recherche du chemin via la topologie
        chemin = self._topologie.trouver_chemin(paquet.source, paquet.destination)

        if not chemin:
            print(f"Erreur : Destination {paquet.destination} inatteignable.")
            self._moniteur.enregistrer_perte(paquet)
            self._enregistrer_historique(paquet, False, [])
            return False

        print(f"Chemin trouvé : {' -> '.join(eq.nom for eq in chemin)}")

        # Calcul de la performance (latence cumulée)
        temps_total = 0.0
        for i in range(len(chemin) - 1):
            lien = self._topologie.obtenir_lien(chemin[i], chemin[i+1])
            temps_total += lien.latence
            print(f" Passage par {chemin[i]} -> {chemin[i+1]} ({lien.latence} ms)")

        print(f"Paquet livre avec succes en {temps_total:.2f} ms.")
        self._moniteur.enregistrer_envoi(paquet, temps_total)
        self._enregistrer_historique(paquet, True, chemin)
        return True

    def _enregistrer_historique(self, paquet, succes, chemin):
        if len(self._historique) >= 10:
            self._historique.pop(0)
        self._historique.append({
            "paquet": paquet,
            "succes": succes,
            "chemin": chemin,
            "heure": datetime.now().strftime("%H:%M:%S")
        })

    def afficher_historique(self):
        print("\n--- Historique des 10 derniers paquets ---")
        for ent in self._historique:
            statut = "OK" if ent["succes"] else "ECHEC"
            print(f"[{ent['heure']}] {statut} - {ent['paquet']}")


