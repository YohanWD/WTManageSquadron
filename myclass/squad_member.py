from json import JSONEncoder
from myclass.activity import Activity


# Each 3 day a player can have a max number of 360 activity
# Activity is cap at 3600 (360 x 30day) ???
#
class Squad_member(object):
    def __init__(
        self,
        id=-1,
        squad_num=None,
        pseudo=None,
        class_perso_esca=None,
        current_activity=None,
        squad_role=None,
        enter_date=None,
        last_update=None,
        activity_hist=[],
    ):
        self.id = id
        self.squad_num = squad_num
        self.pseudo = pseudo
        self.class_perso_esca = class_perso_esca  # Classement personnel dans l'escadron
        self.current_activity = current_activity
        self.squad_role = squad_role
        self.enter_date = enter_date
        #  ------
        self.last_update = last_update  # is automaticly update on database side
        self.activity_hist = []

    @classmethod
    def from_db(cls, dic):
        return cls(
            id=dic["id"],
            squad_num=dic["squad_num"],
            pseudo=dic["pseudo"],
            class_perso_esca=dic["class_perso_esca"],
            current_activity=dic["current_activity"],
            squad_role=dic["squad_role"],
            enter_date=dic["enter_date"],
            last_update=dic["last_update"],
        )

    @classmethod
    def from_web_page(cls, list):
        return cls(
            squad_num=list[0],
            pseudo=list[1],
            class_perso_esca=list[2],
            current_activity=list[3],
            squad_role=list[4],
            enter_date=list[5],
        )

    def update_previous_activity(self, activity):
        self.prev_activity = activity

    def setPseudo(self, pseudo):
        self.pseudo = pseudo

    def appendActivity(self, el):
        self.activity_hist.append(Activity.from_db(el))

    def __iter__(self):
        return iter(
            [
                self.squad_num,
                self.pseudo,
                self.class_perso_esca,
                self.current_activity,
                self.squad_role,
                self.enter_date,
            ]
        )

    def __eq__(self, other):
        return self.pseudo == other.pseudo

    def __hash__(self):
        return hash(tuple(self))


# subclass JSONEncoder
class squad_member_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
