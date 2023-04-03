from discord import SyncWebhook

# Revoir la fonction surement
# Info : Fonction qui renvoie
# Post : renvoie True si le joueur est inactif depuis 3 semaines, False sinon
def check_if_members_is_inactive(members):
    isInactive = False

    # ex : 0 - 100 - 150 - 100 - 0 - 0 - 0 - 0  
    # Par période de 3 jours avec un max de 360 pts
    # Check par rapport a la date d'entrée dans l'escadron
    # Joueur inactif si une période de 0 de plus de 1 semaines (7jours)
    # Après 3 semaines inactif on dégage le membre

    sevenDayCounter = 0
    weekInactive = 0

    for activity in members.activity_hist:
        if weekInactive == 3:
            isInactive = True
        if sevenDayCounter == 7:
            # Le joueuer est inactif depuis 1 semaine
            # Envoie d'une alerte
            weekInactive +=1

        if activity == 0:
            sevenDayCounter += 1
        else:
            sevenDayCounter = 0
            weekInactive = 0

    return isInactive

def send_discord_notif(webhook_url, message):
    webhook = SyncWebhook.from_url(webhook_url)
    try:
        webhook.send(message)
    except Exception as e:
        print("Error during message sending to discord : ", e)