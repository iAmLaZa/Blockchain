class Etudiant():
    def __init__(self,nom,prenom, matricule, specialite, universite):
        self.nom = nom
        self.prenom = prenom
        self.matricule = matricule
        self.specialite = specialite
        self.universite = universite

    def __str__(self):
        return str("Etudiant: %s\nnom: %s\nprenom: %s\nmatricule: %s\nspecialite: %s\n" %(
            self.nom,
            self.prenom,
            self.matricule,
            self.specialite

            )
        )

    def rechercheEtudiant(self, matricule):
        print('recherche par matricule dans data base ....')
        self.nom='wail'
        self.prenom='wail'
        self.matricule='11111'
        self.specialite='info'
        self.universite='usthb'
        return self