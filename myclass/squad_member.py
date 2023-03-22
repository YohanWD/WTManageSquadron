from datetime import datetime
from json import JSONEncoder


# Each 3 day a player can have a max number of 360 activity
# Activity is cap at 3600 (360 x 30day) ???
#
class Squad_member():

    #  def __init__(self, number, name, activity, role, enter_date):
    #     self.name = name
    #     self.number = imagpart
    #     self.current_activity = activity
    #     self.role = role
    #     self.enter_date = enter_date
    #     self.update = datetime.now()
    
    def __init__(self, list):
        # self.id = -1
        self.number = list[0]
        self.name = list[1]
        self.class_perso_esca = list[2] # Classement personnel dans l'escadron
        self.current_activity = list[3]
        self.role = list[4]
        self.enter_date = list[5]
        self.last_update = None # is automaticly update on database side
        self.activity_hist = []

    def update_previous_activity(self,activity):
        self.prev_activity = activity
    
    def setName(self,name):
        self.name = name
        
    def __iter__(self):
        return iter([self.number,
        self.name,
        self.class_perso_esca,
        self.current_activity,
        self.role,
        self.enter_date])

# subclass JSONEncoder
class squad_member_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__