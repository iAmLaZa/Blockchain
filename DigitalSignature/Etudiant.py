class Etudiant():
    
    def __init__(self,familyname,lastname, matricule, email ,date,place,major):
        self.familyname = familyname
        self.lastname = lastname
        self.matricule = matricule
        self.email = email
        self.date=date
        self.place = place
        self.major = major
        

    def __str__(self):
        return str("Etudiant: %s\nnom: %s\nprenom: %s\nmatricule: %s\nmajor: %s\n" %(
            self.familyname,
            self.lastname,
            self.matricule,
            self.major

            )
        )
        