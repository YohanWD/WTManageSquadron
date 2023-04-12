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

# Fonction to compare 2 list of squad members
# POST : return a tuple of 3 list of squad_members
# toCreate = list of new user that need to be added to database
# toUpdate = list of user to update activity in database
# squadleaver = list of user to delete from the database
# Maybe redo the function there is a better method
def compare_squads_members(list1,list2):
    # EX : list1 = [1,2,3,4,5]
    # list2 = [1,2,3,4,6]
    # output:  toCreate=[6], toUpdate = [1,2,3,4], squadLeaver = [5]

    squadLeaver = []
    for element in list1:
        if element not in list2:
            squadLeaver.append(element)

    toCreate = []
    for element in list2:
        if element not in list1:
            toCreate.append(element)
    
    toUpdate = list(set(list2) - set(toCreate))
    
    return toCreate,toUpdate,squadLeaver
