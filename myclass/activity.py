from json import JSONEncoder


class Activity(object):
    def __init__(self, id=-1, activity=None, squad_member_id=None, last_update=None):
        self.id = id
        self.activity = activity  # Member activity
        self.squad_member_id = squad_member_id
        self.last_update = last_update  # Classement personnel dans l'escadron

    @classmethod
    def from_db(cls, list):
        return cls(
            id=list["id"],
            activity=list["activity"],
            squad_member_id=list["squad_member_id"],
            last_update=list["last_update"],
        )

    def get_activity(self):
        return self.activity
