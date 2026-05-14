"""
paquets.py — Paquets réseau et simulation de trafic pour SIMNet.
"""

from datetime import datetime
from equipement import AdresseIP

PROTOCOLES_VALIDES = ("TCP", "UDP", "ICMP")


class Paquet:
    """Représente un paquet réseau circulant entre deux équipements."""

    _compteur = 0  # Identifiant unique auto-incrémenté (attribut de classe)

    def __init__(self, source: str, destination: str,
                 protocole: str, taille: int, priorite: int):
        """
        Initialise un paquet réseau.

        :param source: Adresse IP source (chaîne)
        :param destination: Adresse IP destination (chaîne)
        :param protocole: TCP, UDP ou ICMP
        :param taille: Taille en octets (entier positif)
        :param priorite: Priorité de 1 (basse) à 5 (haute)
        """
        # Validation des adresses via AdresseIP (déjà codée dans equipement.py)
        self._source = AdresseIP(source)
        self._destination = AdresseIP(destination)

        # Validation du protocole
        if protocole not in PROTOCOLES_VALIDES:
            raise ValueError(
                f"Protocole invalide : '{protocole}'. "
                f"Valides : {PROTOCOLES_VALIDES}"
            )
        self._protocole = protocole

        # Validation de la taille
        if not isinstance(taille, int) or taille <= 0:
            raise ValueError(
                f"Taille invalide : {taille} (doit être un entier positif)."
            )
        self._taille = taille

        # Validation de la priorité
        if not isinstance(priorite, int) or not (1 <= priorite <= 5):
            raise ValueError(
                f"Priorité invalide : {priorite} (doit être entre 1 et 5)."
            )
        self._priorite = priorite

        # Métadonnées automatiques
        Paquet._compteur += 1
        self._id = Paquet._compteur
        self._horodatage = datetime.now()

    # --- Propriétés (lecture seule — un paquet ne se modifie pas) ---

    @property
    def source(self) -> str:
        """Retourne l'adresse IP source."""
        return self._source.ip

    @property
    def destination(self) -> str:
        """Retourne l'adresse IP destination."""
        return self._destination.ip

    @property
    def protocole(self) -> str:
        return self._protocole

    @property
    def taille(self) -> int:
        return self._taille

    @property
    def priorite(self) -> int:
        return self._priorite

    @property
    def id(self) -> int:
        return self._id

    @property
    def horodatage(self) -> datetime:
        return self._horodatage

    def __str__(self) -> str:
        return (f"Paquet#{self._id} [{self._protocole}] "
                f"{self._source.ip} → {self._destination.ip} "
                f"| {self._taille} octets | priorité {self._priorite}")

    def __repr__(self) -> str:
        return (f"Paquet(id={self._id}, src={self._source.ip!r}, "
                f"dst={self._destination.ip!r}, proto={self._protocole!r})")


class Simulateur:
    """
    Gère la simulation de trafic : envoi de paquets saut par saut,
    passage par les firewalls, et collecte des statistiques.
    """

    def __init__(self, topologie, moniteur):
        """
        :param topologie: La topologie réseau (instance de Topologie)
        :param moniteur: Le moniteur réseau (instance de MoniteurReseau)
        """
        self._topologie = topologie
        self._moniteur = moniteur
        self._historique = []  # 10 derniers résultats

    def envoyer_paquet(self, paquet: Paquet) -> bool:
        """
        Envoie un paquet de sa source à sa destination.

        :param paquet: Le paquet à transmettre
        :return: True si livré, False si perdu/bloqué
        """
        print(f"\n{'='*50}")
        print(f"  ENVOI : {paquet}")
        print(f"{'='*50}")

        # 1. Recherche du chemin
        chemin = self._topologie.trouver_chemin(
            paquet.source, paquet.destination
        )

        if chemin is None:
            print(f"  ✗ Destination {paquet.destination} inatteignable.")
            self._moniteur.enregistrer_perte(paquet)
            self._enregistrer_historique(paquet, succes=False, chemin=[])
            return False

        noms = " → ".join(chemin)
        print(f"  Chemin ({len(chemin)} sauts) : {noms}")

        # 2. Transmission saut par saut
        temps_total = 0.0
        for i in range(len(chemin) - 1):
            noeud_actuel = chemin[i]
            noeud_suivant = chemin[i + 1]

            # Récupérer la latence réelle du lien
            lien = self._topologie.obtenir_lien(noeud_actuel, noeud_suivant)
            temps_total += lien.latence

            print(f"  ↳ {noeud_actuel} → {noeud_suivant} "
                  f"({lien.bande_passante} Mbps, {lien.latence} ms)")

        # 3. Succès
        print(f"  ✓ Paquet livré en {temps_total:.1f} ms simulés.")
        self._moniteur.enregistrer_envoi(paquet, temps_total)
        self._enregistrer_historique(paquet, succes=True, chemin=chemin)
        return True

    def _enregistrer_historique(self, paquet: Paquet,
                                succes: bool, chemin: list):
        """Conserve les 10 derniers résultats de transmission."""
        self._historique.append({
            "paquet": paquet,
            "succes": succes,
            "chemin": chemin,
            "horodatage": datetime.now(),
        })
        if len(self._historique) > 10:
            self._historique.pop(0)

    def afficher_historique(self) -> str:
        """Retourne l'historique des 10 derniers paquets."""
        if not self._historique:
            return "Historique : aucun paquet transmis."
        lignes = ["=== HISTORIQUE DES 10 DERNIERS PAQUETS ==="]
        for entree in self._historique:
            statut = "✓" if entree["succes"] else "✗"
            chemin_str = " → ".join(entree["chemin"]) if entree["chemin"] else "—"
            ts = entree["horodatage"].strftime("%H:%M:%S")
            lignes.append(f"  [{ts}] {statut} {entree['paquet']} | {chemin_str}")
        return "\n".join(lignes)