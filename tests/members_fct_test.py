import unittest
from utils import members_fct
from myclass.squad_member import Squad_member


class TestInactivityFunction(unittest.TestCase):
    mydic = {
        "id": 1,
        "squad_num": 1,
        "pseudo": "billy",
        "class_perso_esca": 2,
        "current_activity": 0,
        "squad_role": "dummy",
        "enter_date": "0/0/0",
        "last_update": "0/0/0",
    }
    test_member = Squad_member.from_db(mydic)
    test_member2 = Squad_member.from_db(mydic)
    test_member3 = Squad_member.from_db(mydic)
    test_member4 = Squad_member.from_db(mydic)
    test_member5 = Squad_member.from_db(mydic)
    test_member6 = Squad_member.from_db(mydic)

    # activity = [0,0,0]
    # consecutive_day : 7 , min_activity = 200
    # inactive ? False
    def test_new_player(self):
        cpt = 0
        while cpt < 3:
            test_act = {
                "id": 1,
                "activity": 0,
                "squad_member_id": 1,
                "last_update": "0/0/0",
            }
            self.test_member.appendActivity(test_act)
            cpt += 1
        self.assertEqual(
            members_fct.check_if_members_is_inactive(self.test_member, 7, 200), False
        )

    # activity = [0,0,0,360]
    # consecutive_day : 4 , min_activity = 200
    # inactive ? False
    def test_active_player1(self):
        cpt = 0
        while cpt < 3:
            test_act = {
                "id": 1,
                "activity": 0,
                "squad_member_id": 1,
                "last_update": "0/0/0",
            }
            self.test_member2.appendActivity(test_act)
            cpt += 1
        self.test_member2.appendActivity(
            {"id": 1, "activity": 360, "squad_member_id": 1, "last_update": "0/0/0"}
        )
        self.assertEqual(
            members_fct.check_if_members_is_inactive(self.test_member2, 200), False
        )

    # activity = [0,0,0,0,...,0]
    # consecutive_day : 21 , min_activity = 0
    # inactive ? True
    def test_inactive_player(self):
        cpt = 0
        while cpt < 23:
            test_act = {
                "id": 1,
                "activity": 0,
                "squad_member_id": 1,
                "last_update": "0/0/0",
            }
            self.test_member3.appendActivity(test_act)
            cpt += 1
        self.assertEqual(
            members_fct.check_if_members_is_inactive(self.test_member3), True
        )

    # activity = [360,360,360]
    # consecutive_day : 3 , min_activity = 1000
    # inactive ? True
    def test_inactive_player2(self):
        cpt = 0
        while cpt < 3:
            test_act = {
                "id": 1,
                "activity": 360,
                "squad_member_id": 1,
                "last_update": "0/0/0",
            }
            self.test_member3.appendActivity(test_act)
            cpt += 1
        self.assertEqual(
            members_fct.check_if_members_is_inactive(self.test_member3, 3, 1000), True
        )


if __name__ == "__main__":
    unittest.main()
