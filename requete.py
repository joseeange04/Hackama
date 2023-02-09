from ampalibe import Model
class Requete (Model):
    def __init__(self, conf):
        """
            Connexion à notre base de donnée
        """
        Model(self, conf)

    @Model.verif_db
    def Get_Vaccination_list(self):
        """
        Recupérer la liste des vaccins existants
        """
        req = """
                SELECT id_vaccin, nom_vaccin, illustration, description 
                FROM vaccins
        """
        self.cursor.execute(req)
        result = self.cursor.fetchall()
        self.db.commit()
        return result