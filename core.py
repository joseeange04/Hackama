import ampalibe
from ampalibe import Messenger, Payload, translate, Model
from ampalibe.ui import QuickReply, Button, Type, Element
from conf import Configuration as config
from requete import Requete
from ampalibe.messenger import Filetype

chat = Messenger()
query = Model()
req = Requete(config())

print(config.APP_URL)
@ampalibe.command('/')
def main(sender_id, lang, cmd, **extends):
    chat.get_started()

    chat.send_text(sender_id, translate("Bonjour, bienvenu sur le chatbot de Vaccination et tourisme à Madagascar👩‍⚕️🏄‍♀️", lang))
#-------------Menu persistant ne doit contenir que deux paramètre-----------------------#
    persistent_menu = [
        Button(
            type = Type.postback,
            title = "Menu 📑",
            payload = Payload("/menu")
        ),
        Button(
            type = Type.postback,
            title = "Langue 📢",
            payload = Payload("/langue")
        )

    ]
    chat.persistent_menu(sender_id, persistent_menu)
    query.set_action(sender_id, None)


@ampalibe.command("/menu")
def Get_menu(sender_id, cmd, lang, **ext):
    all_menu= [
        Button(
            type = Type.postback,
            title = translate("Information des vaccins", lang),
            payload = Payload("/information")
        ),
        Button(
            type = Type.postback,
            title = translate("Festivales vaccinés", lang),
            payload = Payload('/festival')
        ),
        Button(
            type = Type.postback,
            title = "Statistique de vaccination",
            payload = Payload('/statistique')
        ),
    ]
    chat.send_button(sender_id, all_menu, translate("Que souhaitez-vous faire?", lang))
    query.set_action(sender_id, None)

@ampalibe.command("/langue")
def SetLangage(sender_id, cmd, **ext):
    langage = [
        QuickReply(
            title = 'Malagasy 🇲🇬 ',
            payload = Payload('/mg')
        ),
        QuickReply(
            title = 'Français 🇫🇷',
            payload = Payload('/fr')
        ),
        QuickReply(
            title = 'Anglais 🇬🇧',
            payload = Payload('/en')
        )
    ]
    chat.send_quick_reply(sender_id, langage, "Français:Veuillez choisir votre langue./ Malagasy: Safidio ary ny fiteny ampiasainao./ English: Please choose your language.")
    query.set_action(sender_id, None)


@ampalibe.command("/information")
def GetInfo(sender_id, cmd, **ext):
    """
    Afficher la liste des vaccins venant de notre base
    """
    vaccins = req.Get_Vaccination_list()
    data = []
    i = 0
    while i < len(vaccins):
        image = vaccins[i][2]
        print(vaccins[i][2])
        button = [
            Button(
                type = Type.postback,
                title = "Details",
                payload = Payload("/details", id_vacc= str(vaccins[i][0]))
            )
        ]
        data.append(
            Element(
                title = str(i+1) + "-" + vaccins[i][1],
                subtitle = vaccins[i][3],
                image_url = config.APP_URL + f"/asset/{image}",
                buttons = button,
            )
        )
        i = i+1
        
    chat.send_template(sender_id, data, next=True )


@ampalibe.command("/details")
def Get_Vaccin_Details(sender_id, id_vacc, **ext):
    vaccin_detail = req.Get_Vaccin_details(id_vacc)
    print(vaccin_detail)

    chat.send_text(sender_id, "Dans le pdf ci-dessous toutes les informations")
    chat.send_file(sender_id,f"assets/public/{vaccin_detail}", reusable=True)
    
@ampalibe.command("/festival")
def Get_festival(sender_id, cmd, **ext):
    annee = [
        QuickReply(
            title = "2022",
            payload = Payload("/2022")
        ),
        QuickReply(
            title = "Les prochaines",
            payload = Payload("/next")
        ),
    ]
    chat.send_quick_reply(sender_id, annee, "En quele année souhaitez-vous vérifier?")
    query.set_action(sender_id, None)

@ampalibe.command("/2022")
def Get_festival_2022(sender_id, cmd, **ext):
    festival_2022 = req.Get_festival()

    data= []
    i = 0
    while i< len(festival_2022):
        image = festival_2022[i][3]
        button = [
            Button(
                type = Type.postback,
                title= "Visiter",
                payload = Payload("/visiter")
            )
        ]
        data.append(
            Element(
                title = str(i+1) + "-" + festival_2022[i][1],
                subtitle = festival_2022[i][1] + "Affecté par la COVID-19, le secteur du tourisme à Madagascar promeut la vaccination ",
                image_url = config.APP_URL + f"/asset/{image}",
                buttons = button
            )
        )
        i= i+1
    chat.send_template(sender_id, data, next=True)
    query.set_action(sender_id, None)


@ampalibe.command("/next")
def Next_Festival(sender_id, cmd, **ext):
    chat.send_text(sender_id, "Suivez toujours notre page pour connaître les festivales vaccinés à venir!")

@ampalibe.command("/statistique")
def statistique(sender_id, cmd, **ext):
    choix_stat = [
        QuickReply(
            title = "Par vaccin",
            payload = Payload("/stat_vaccin")
        ),
        QuickReply(
            title = "Par région",
            payload = Payload("/region")
        )
    ]
    chat.send_quick_reply(sender_id, choix_stat, "Comment souhaitez-vous voir les données?")

@ampalibe.command("/stat_vaccin")
def Get_Stat_Vaccin(sender_id, cmd, **ext):
    vacc_stat = req.Get_Vaccination_stat()
    print(vacc_stat)
    chat.send_text(sender_id, "Voici donc les statistiques des personnes vaccinées à Madagascar selon les type de vaccin")
    chat.send_message(sender_id, vacc_stat[0][0] + " = " + vacc_stat[0][1])
    chat.send_message(sender_id, vacc_stat[1][0] + " = " + vacc_stat[1][1])
    chat.send_message(sender_id, vacc_stat[2][0]+ " = " + vacc_stat[2][1])
    chat.send_message(sender_id, vacc_stat[3][0] + " = " + vacc_stat[3][1])
    chat.send_message(sender_id, vacc_stat[4][0] + " = " + vacc_stat[4][1])
    
@ampalibe.command("/region")
def Get_vaccins_by_region(sender_id, cmd, **ext):
    list_region = req.Get_stat_region()
    data = []
    i = 0
    while i < len(list_region):
        image = list_region[i][3]
        button = [
            Button(
                type = Type.postback,
                title= "Plus de details",
                 payload = Payload("/details_region", id_region =str(list_region[i][0]) )
            )
        ]
        data.append(
            Element(
                title = str(i+1) + "-" + list_region[i][1],
                subtitle =list_region[i][5] + "Total des vaccinées",
                image_url = config.APP_URL + f"/asset/{image}",
                buttons = button
            )
        )
        i= i+1
    chat.send_template(sender_id, data, next=True)
    query.set_action(sender_id, None) 

    rechercher = [
        Button(
            type = Type.postback,
            title = "RECHERCHER 🔎",
            payload = Payload("/recherche")
        )
    ]
    chat.send_button(sender_id, rechercher, "Voulez_vous rechercher une region?")
    query.set_action(sender_id, None)

@ampalibe.command("/recherche")
def Search_Region(sender_id, cmd, **extend):
    chat.send_message(sender_id, "Tapez la région que vous voulez rechercher")
    query.set_action(sender_id, '/get_region')

@ampalibe.action("/get_region")
def Region(sender_id, cmd, **ext):
    query.set_action(sender_id, None)
    region = req.Search_region(cmd)
   
    data = []
    i = 0
    while i < len(region):
        image = region[i][3]
        button = [
            Button(
                type = Type.postback,
                title= "Plus de details",
                 payload = Payload("/Visiter")
            )
        ]
        data.append(
            Element(
                title = str(i+1) + "-" + region[i][1],
                subtitle =region[i][5] + "Total des vaccinées",
                image_url = config.APP_URL + f"/asset/{image}",
                buttons = button
            )
        )
        i= i+1
    chat.send_template(sender_id, data, next=True)
    query.set_action(sender_id, None) 


@ampalibe.command("/details_region")
def Get_Statistique_details(sender_id, id_region, **ext):
    detail_region = req.Details_region(id_region)
    print(detail_region)
    
    chat.send_text(sender_id, "Nombre de population = " + detail_region[0][0])
    chat.send_text(sender_id, "Objectifs de vaccination = " + detail_region[0][1])
    chat.send_text(sender_id, "Totale vaccinées = " + detail_region[0][2])

