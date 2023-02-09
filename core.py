import ampalibe
from ampalibe import Messenger, Payload, translate, Model
from ampalibe.ui import QuickReply, Button, Type

chat = Messenger()
query = Model()

@ampalibe.command('/')
def main(sender_id, lang, cmd, **extends):
    chat.get_started()
    chat.send_text(sender_id, translate("Bonjour, bienvenu sur le chatbot de Vaccination et tourisme 👩‍⚕️🏄‍♀️", lang))
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
        QuickReply(
            title = translate("Information sur les vaccins", lang),
            payload = Payload("/information")
        ),
        QuickReply(
            title = translate("Prochaine festival vacciné", lang),
            payload = Payload('/festival')
        ),
        QuickReply(
            title = "Statistique de vaccination contre covid-19",
            payload = Payload('/statistique')
        ),
    ]
    chat.send_quick_reply(sender_id, all_menu, translate("Que souhaitez-vous vister?", lang))
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
    pass