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
    chat.send_quick_reply(sender_id, langage, "Français:Pour commencez choisissez votre langue./ Malagasy: Safidio aary ny fiteny ampiasainao./ English: Please choose your language.")
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
    

