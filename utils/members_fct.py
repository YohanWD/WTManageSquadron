# Info : Function to check if a members is inactive for more than X day and if he has the require activity number
# Pre : member:Squad_member : a list has exactly the last nb_of_day_inactive day loaded
# Post : Return false if inactity day = x and activity_treshold not respected
def check_if_members_is_inactive(
    member, consecutive_day_of_inactivty=21, min_activiy_required=0
):
    if len(member.activity_hist) < consecutive_day_of_inactivty:
        return False
    for activity_obj in member.activity_hist:
        if (min_activiy_required == 0 and activity_obj.activity > 0) or (
            activity_obj.activity >= min_activiy_required and min_activiy_required != 0
        ):
            return False
    return True


# Function to compare 2 list of squad members
# POST : return a tuple of 3 list of squad_members
# toCreate = list of new user that need to be added to database
# toUpdate = list of user to update activity in database
# squadleaver = list of user to delete from the database
# Maybe redo the function there is a better method
def compare_squads_members(list1, list2):
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

    return toCreate, toUpdate, squadLeaver
