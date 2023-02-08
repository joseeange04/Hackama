import ampalibe
from ampalibe import Messenger, Payload, translate, Model
from ampalibe.ui import QuickReply, Button, Type

chat = Messenger()
query = Model()

@ampalibe.command('/')
def main(sender_id, lang, cmd, **extends):
    chat.get_started()
    langage = [
        QuickReply(
            title = 'Malagasy',
            payload = Payload('/mg')
        ),
        QuickReply(
            title = 'Français',
            payload = Payload('/fr')
        ),
        QuickReply(
            title = 'Anglais',
            payload = Payload('/en')
        )
    ]
    chat.send_quick_reply(sender_id, langage, "Français:Pour commencez choisissez votre langue./ Malagasy: Safidio aary ny fiteny ampiasainao./ English: Please choose your language.")
    query.set_action(sender_id, None)
#-------------Menu persistant ne doit contenir que deux paramètre-----------------------#
    persistent_menu = [
        Button(
            type = Type.postback,
            title = translate("Information sur les vaccins", lang),
            payload = Payload('/information')
        ),
        Button(
            type = Type.postback,
            title = translate("Prochaine festival vacciné", lang),
            payload = Payload('/festival')
        )

    ]
    chat.persistent_menu(sender_id, persistent_menu)



""" ,
        Button(
            type = Type.postback,
            title = "Statistique de vaccination contre covid-19",
            payload = Payload('/statistique')
        ),
        Button(
            type = Type.postback,
            title = "Destination touristique sécurisé",
            payload = Payload('/destination')
        ) 
"""