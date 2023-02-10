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
    def Get_Vaccination_stat(self):
        """
        Recupérer la liste des vaccins existants
        """
        req = """
                SELECT nom_vaccin, vaccinees
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

    @Model.verif_db
    def Get_festival(self):
        
        req = """
                Select id_festival, titre, date, image
                FROM festivales
        """
        self.cursor.execute(req)
        result = self.cursor.fetchall()
        self.db.commit()
        return result

    @Model.verif_db
    def Get_stat_region(self):
        """
            Récupérer les statistiques par région
        """
        req = """
                Select id_region, nom_region, population, image_region, vaccines, pourcentage
                FROM stat_vaccin_region
        """
        self.cursor.execute(req)
        result = self.cursor.fetchall()
        self.db.commit()
        return result

    @Model.verif_db
    def Search_region(self, nom_region):
        """
        Fonction pour trouver la musique recherhé par l'utilisateur
        """
        req="""
            SELECT id_region, nom_region,  image_region, pourcentage
            FROM stat_vaccin_region
            WHERE UPPER(nom_region) LIKE %s
            OR SOUNDEX(nom_region)=SOUNDEX(%s)
            """
        self.cursor.execute(req, (f"%{nom_region.upper()}%", nom_region))
        result = self.cursor.fetchall()
        self.db.commit()
        return result    


    @Model.verif_db
    def Details_region(self, id_region):
        """
            Get details
        
        """
        req = """
                SELECT population, objectifs, vaccines
                FROM stat_vaccin_region
                WHERE id_region = %s
        """
        self.cursor.execute(req, (id_region,))
        result = self.cursor.fetchall()
        self.db.commit()
        return result

