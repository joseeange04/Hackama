from ampalibe import Model
class Requete (Model):
    def __init__(self, conf):
        """
            Connexion à notre base de donnée
        """
        Model.__init__(self, conf)

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

    @Model.verif_db
    def Get_Vaccin_details(self, id_vaccin):
        """
            Explication sur les vaccins
        """
        req = """
                SELECT pdf FROM vaccins WHERE id_vaccin = %s 
        """

        self.cursor.execute(req, (id_vaccin,))
        result = self.cursor.fetchone()
        self.db.commit()
        return result[0]